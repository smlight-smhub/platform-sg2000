#
# Copyright (c) 2026 SMLIGHT. All rights reserved.
#

from os.path import join
import sys
import subprocess

try:
    import grpc_tools.protoc
except ImportError:
    print("Installing grpcio-tools for nanopb generation...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "grpcio-tools"])

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-sg2000-rtos")
assert FRAMEWORK_DIR

# ESPHome may pull googletest which forcibly injects -pthread into global LINKFLAGS
# on Linux. Our bare-metal toolchain riscv-none-elf-g++ compiler does not support threads
def strip_pthread_hook(source, target, env):
    if "-pthread" in env.get("LINKFLAGS", []):
        env["LINKFLAGS"].remove("-pthread")
    if "-pthread" in env.get("CCFLAGS", []):
        env["CCFLAGS"].remove("-pthread")

    globalenv = DefaultEnvironment()
    if "-pthread" in globalenv.get("LINKFLAGS", []):
        globalenv["LINKFLAGS"].remove("-pthread")
    if "-pthread" in globalenv.get("CCFLAGS", []):
        globalenv["CCFLAGS"].remove("-pthread")

env.AddPreAction("$BUILD_DIR/${PROGNAME}.elf", strip_pthread_hook)

env.SConscript(join(FRAMEWORK_DIR, "tools", "platformio-build.py"), exports="env")
