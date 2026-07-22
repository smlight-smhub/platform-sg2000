#
# Copyright (c) 2026 SMLIGHT. All rights reserved.
#

from os.path import join

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-sg2000-rtos")
assert FRAMEWORK_DIR

# ESPHome may pull googletest which forcibly injects -pthread into global LINKFLAGS
# on Linux. Our bare-metal toolchain riscv-none-elf-g++ compiler does not support threads
if "-pthread" in env.get("LINKFLAGS", []):
    env["LINKFLAGS"].remove("-pthread")
if "-pthread" in env.get("CCFLAGS", []):
    env["CCFLAGS"].remove("-pthread")

env.SConscript(join(FRAMEWORK_DIR, "tools", "platformio-build.py"), exports="env")
