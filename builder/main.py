#
# Copyright (c) 2026 SMLIGHT. All rights reserved.
#

import os
from os.path import join
from SCons.Script import AlwaysBuild, Builder, Default, DefaultEnvironment

env = DefaultEnvironment()
platform = env.PioPlatform()

TOOLCHAIN_DIR = env.PioPlatform().get_package_dir("toolchain-riscv-xpack")

if TOOLCHAIN_DIR and os.path.exists(join(TOOLCHAIN_DIR, "bin")):
    compiler_bin = join(TOOLCHAIN_DIR, "bin")
else:
    print("Warning: toolchain-riscv-xpack bin not found. Falling back to system path.")
    compiler_bin = ""

env.PrependENVPath("PATH", compiler_bin)

env.Replace(
    AR=join(compiler_bin, "riscv-none-elf-ar"),
    AS=join(compiler_bin, "riscv-none-elf-as"),
    CC=join(compiler_bin, "riscv-none-elf-gcc"),
    CXX=join(compiler_bin, "riscv-none-elf-g++"),
    GDB=join(compiler_bin, "riscv-none-elf-gdb"),
    OBJCOPY=join(compiler_bin, "riscv-none-elf-objcopy"),
    RANLIB=join(compiler_bin, "riscv-none-elf-ranlib"),
    SIZETOOL=join(compiler_bin, "riscv-none-elf-size"),

    ARFLAGS=["rc"],
    SIZEPRINTCMD='$SIZETOOL -d $SOURCES',
    PROGSUFFIX="_debug.elf",
    STRIP=join(compiler_bin, "riscv-none-elf-strip")
)

def strip_elf_action(target, source, env):
    import shutil
    import subprocess
    shutil.copy(str(source[0]), str(target[0]))
    strip_tool = env.subst("$STRIP")
    subprocess.run([strip_tool, "--strip-debug", str(target[0])], check=True)
    return None

env.Append(
    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".bin"
        ),
        StripElf=Builder(
            action=env.Action(strip_elf_action, "Generating stripped ELF: $TARGET"),
            suffix=".elf"
        )
    )
)

env.Append(
    ASFLAGS=[
        "-mcpu=thead-c906",
        "-march=rv64gc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_zicsr_zifencei",
        "-mabi=lp64d",
        "-DCONFIG_64BIT"
    ],
    CCFLAGS=[
        "-mcpu=thead-c906",
        "-march=rv64gc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_zicsr_zifencei",
        "-mno-fence-tso",
        "-mabi=lp64d",
        "-mcmodel=medany",
        "-DCONFIG_64BIT",
        "-msmall-data-limit=0",
        "-D__riscv_xtheadc",
        "-fno-strict-aliasing",
        "-O2",
        "-ffunction-sections",
        "-fdata-sections"
    ],
    LINKFLAGS=[
        "-mcpu=thead-c906",
        "-march=rv64gc_xtheadba_xtheadbb_xtheadbs_xtheadcmo_xtheadcondmov_xtheadfmemidx_xtheadmac_xtheadmemidx_xtheadmempair_xtheadsync_zicsr_zifencei",
        "-mabi=lp64d",
        "-nostartfiles",
        "-u",
        "_start",
        "-static",
        "--specs=nosys.specs",
        "-Wl,--gc-sections",
        "-Wl,--no-warn-rwx-segments"
    ]
)

# Force C++ linker to ensure libstdc++ and C++ exception personalities are correctly linked
# when the main project files are evaluated or compiled as C.
env.Replace(LINK="$CXX")

FRAMEWORK_DIR = platform.get_package_dir("framework-sg2000-rtos")
if FRAMEWORK_DIR:
    env.Append(LINKFLAGS=[f"-L{FRAMEWORK_DIR}"])

target_elf = env.BuildProgram()
target_stripped_elf = env.StripElf(join("$BUILD_DIR", "${PROGNAME}"), target_elf)
target_bin = env.ElfToBin(join("$BUILD_DIR", "${PROGNAME}"), target_stripped_elf)

upload_cmd = env.GetProjectOption("upload_command", "")
if upload_cmd:
    env.Replace(UPLOADCMD=upload_cmd)
    upload = env.Alias("upload", target_bin, env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE"))
    AlwaysBuild(upload)

AlwaysBuild(env.Alias("nobuild", target_bin))
Default([target_bin, target_stripped_elf, target_elf])
