#!/usr/bin/env python3

from migen import *
from litex.gen import *
from litex.build.io import DDROutput
from litex_boards.platforms import colorlight_i5

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
# Importante: Precisamos do PHY de video
from litex.soc.cores.video import VideoHDMIPHY 
from litex.build.generic_platform import Subsignal, Pins, IOStandard, Misc

from litedram.modules import M12L64322A
from litedram.phy import GENSDRPHY, HalfRateGENSDRPHY

# --- DEFINIÇÃO DA EXTENSÃO HDMI (CN2) ---
_hdmi_infos = [
    ("hdmi", 0,
        # Importante: O HDMI usa lógica 3.3V simulando diferencial
        # Par 0 (Geralmente Azul) - Pinos 9 e 10
        Subsignal("data0_p", Pins("N17")),
        Subsignal("data0_n", Pins("L20")),
        
        # Par 1 (Geralmente Verde) - Pinos 6 e 8
        Subsignal("data1_p", Pins("P18")),
        Subsignal("data1_n", Pins("N18")),
        
        # Par 2 (Geralmente Vermelho) - Pinos 4 e 5
        Subsignal("data2_p", Pins("P17")),
        Subsignal("data2_n", Pins("T17")),
        
        # Clock (Sincronia) - Pinos 11 e 12
        Subsignal("clk_p",   Pins("L18")),
        Subsignal("clk_n",   Pins("M18")),
        
        # O padrão LVCMOS33 é usado porque o ECP5 emula HDMI via GPIO
        IOStandard("LVCMOS33"),
    ),
]

# CRG ----------------------------------------------------------------------------------------------
class _CRG(LiteXModule):
    def __init__(self, platform, sys_clk_freq, use_internal_osc=False, with_usb_pll=False, with_video_pll=False, sdram_rate="1:1"):
        self.rst    = Signal()
        self.cd_sys = ClockDomain()
        if sdram_rate == "1:2":
            self.cd_sys2x    = ClockDomain()
            self.cd_sys2x_ps = ClockDomain()
        else:
            self.cd_sys_ps = ClockDomain()

        # Clk / Rst
        if not use_internal_osc:
            clk = platform.request("clk25")
            clk_freq = 25e6
        else:
            clk = Signal()
            div = 5
            self.specials += Instance("OSCG", p_DIV = div, o_OSC = clk)
            clk_freq = 310e6/div

        rst_n = platform.request("cpu_reset_n")

        # PLL Principal
        self.pll = pll = ECP5PLL()
        self.comb += pll.reset.eq(~rst_n | self.rst)
        pll.register_clkin(clk, clk_freq)
        pll.create_clkout(self.cd_sys,    sys_clk_freq)
        if sdram_rate == "1:2":
            pll.create_clkout(self.cd_sys2x,    2*sys_clk_freq)
            pll.create_clkout(self.cd_sys2x_ps, 2*sys_clk_freq, phase=180)
        else:
           pll.create_clkout(self.cd_sys_ps, sys_clk_freq, phase=180)

        # Video PLL (40MHz para 800x600@60Hz)
        if with_video_pll:
            self.video_pll = video_pll = ECP5PLL()
            self.comb += video_pll.reset.eq(~rst_n | self.rst)
            video_pll.register_clkin(clk, clk_freq)
            self.cd_hdmi   = ClockDomain()
            self.cd_hdmi5x = ClockDomain()
            video_pll.create_clkout(self.cd_hdmi,    40e6, margin=0)
            video_pll.create_clkout(self.cd_hdmi5x, 200e6, margin=0)

# BaseSoC ------------------------------------------------------------------------------------------
class BaseSoC(SoCCore):
    def __init__(self, board="i5", revision="7.0", toolchain="trellis", sys_clk_freq=60e6,
        use_internal_osc       = False,
        sdram_rate             = "1:1",
        with_video_terminal    = False,
        with_video_framebuffer = False,
        **kwargs):
        
        board = board.lower()
        platform = colorlight_i5.Platform(board=board, revision=revision, toolchain=toolchain)
        
        # --- AQUI ESTÁ A MÁGICA ---
        # Adicionamos os pinos do HDMI à plataforma manualmente
        platform.add_extension(_hdmi_infos)

        # CRG
        with_video_pll = with_video_terminal or with_video_framebuffer
        self.crg = _CRG(platform, sys_clk_freq,
            use_internal_osc = use_internal_osc,
            with_video_pll   = with_video_pll,
            sdram_rate       = sdram_rate
        )

        # SoCCore
        SoCCore.__init__(self, platform, int(sys_clk_freq), ident = "LiteX SoC on Colorlight " + board.upper(), **kwargs)

        # SPI Flash
        if board == "i5": from litespi.modules import GD25Q16 as SpiFlashModule
        if board == "i9": from litespi.modules import W25Q64 as SpiFlashModule
        from litespi.opcodes import SpiNorFlashOpCodes as Codes
        self.add_spi_flash(mode="1x", module=SpiFlashModule(Codes.READ_1_1_1))

        # SDRAM
        if not self.integrated_main_ram_size:
            sdrphy_cls = HalfRateGENSDRPHY if sdram_rate == "1:2" else GENSDRPHY
            self.sdrphy = sdrphy_cls(platform.request("sdram"))
            self.add_sdram("sdram",
                phy           = self.sdrphy,
                module        = M12L64322A(sys_clk_freq, sdram_rate),
                l2_cache_size = kwargs.get("l2_size", 8192),
                l2_cache_reverse = False
            )
        
        # --- VIDEO PHY ---
        # Se pedirmos vídeo, criamos o PHY (o driver físico do HDMI)
        if with_video_terminal or with_video_framebuffer:
            self.videophy = VideoHDMIPHY(platform.request("hdmi"), clock_domain="hdmi")
            # Adicionamos o PHY ao SoC e o LiteX cuida de criar o Framebuffer/Terminal
            self.add_video_terminal(phy=self.videophy, timings="800x600@60Hz", clock_domain="hdmi")

# Build --------------------------------------------------------------------------------------------
def main():
    from litex.build.parser import LiteXArgumentParser
    parser = LiteXArgumentParser(platform=colorlight_i5.Platform, description="LiteX SoC on Colorlight I9 HDMI.")
    parser.add_target_argument("--board",            default="i5",             help="Board type (i5/i9).")
    parser.add_target_argument("--revision",         default="7.0",            help="Board revision.")
    parser.add_target_argument("--sys-clk-freq",     default=60e6, type=float, help="System clock frequency.")
    parser.add_target_argument("--sdram-rate",       default="1:1",            help="SDRAM Rate.")
    
    # Argumentos de Vídeo
    viopts = parser.target_group.add_mutually_exclusive_group()
    viopts.add_argument("--with-video-terminal",    action="store_true", help="Enable Video Terminal (HDMI).")
    viopts.add_argument("--with-video-framebuffer", action="store_true", help="Enable Video Framebuffer (HDMI).")
    
    args = parser.parse_args()

    soc = BaseSoC(board=args.board, revision=args.revision,
        toolchain              = args.toolchain,
        sys_clk_freq           = args.sys_clk_freq,
        sdram_rate             = args.sdram_rate,
        with_video_terminal    = args.with_video_terminal,
        with_video_framebuffer = args.with_video_framebuffer,
        **parser.soc_argdict
    )

    builder = Builder(soc, **parser.builder_argdict)
    if args.build:
        builder.build(**parser.toolchain_argdict)

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(builder.get_bitstream_filename(mode="sram"))

if __name__ == "__main__":
    main()