PACKAGES=libc libcompiler_rt libbase libfatfs liblitespi liblitedram libliteeth liblitesdcard liblitesata bios
PACKAGE_DIRS=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/libc /home/joao/AppsUser/Litex/components/litex/litex/soc/software/libcompiler_rt /home/joao/AppsUser/Litex/components/litex/litex/soc/software/libbase /home/joao/AppsUser/Litex/components/litex/litex/soc/software/libfatfs /home/joao/AppsUser/Litex/components/litex/litex/soc/software/liblitespi /home/joao/AppsUser/Litex/components/litex/litex/soc/software/liblitedram /home/joao/AppsUser/Litex/components/litex/litex/soc/software/libliteeth /home/joao/AppsUser/Litex/components/litex/litex/soc/software/liblitesdcard /home/joao/AppsUser/Litex/components/litex/litex/soc/software/liblitesata /home/joao/AppsUser/Litex/components/litex/litex/soc/software/bios
LIBS=libc libcompiler_rt libbase libfatfs liblitespi liblitedram libliteeth liblitesdcard liblitesata
TRIPLE=riscv-none-elf
CPU=vexriscv
CPUFAMILY=riscv
CPUFLAGS=-march=rv32i2p0_m     -mabi=ilp32 -D__vexriscv__
CPUENDIANNESS=little
CLANG=0
CPU_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/cores/cpu/vexriscv
SOC_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc
PICOLIBC_DIRECTORY=/home/joao/AppsUser/Litex/components/pythondata-software-picolibc/pythondata_software_picolibc/data
PICOLIBC_FORMAT=integer
COMPILER_RT_DIRECTORY=/home/joao/AppsUser/Litex/components/pythondata-software-compiler_rt/pythondata_software_compiler_rt/data
export BUILDINC_DIRECTORY
BUILDINC_DIRECTORY=/home/joao/Documentos/Embarcatech/FPGA/Embarcatech-Tarefa-7-FPGA/litex/build/colorlight_i5/software/include
LIBC_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/libc
LIBCOMPILER_RT_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/libcompiler_rt
LIBBASE_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/libbase
LIBFATFS_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/libfatfs
LIBLITESPI_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/liblitespi
LIBLITEDRAM_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/liblitedram
LIBLITEETH_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/libliteeth
LIBLITESDCARD_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/liblitesdcard
LIBLITESATA_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/liblitesata
BIOS_DIRECTORY=/home/joao/AppsUser/Litex/components/litex/litex/soc/software/bios
LTO=0
BIOS_CONSOLE_FULL=1