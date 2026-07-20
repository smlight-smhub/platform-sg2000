#
# Copyright (c) 2026 SMLIGHT. All rights reserved.
#

from os.path import join

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-sg2000-rtos")
assert FRAMEWORK_DIR

env.SConscript(join(FRAMEWORK_DIR, "tools", "platformio-build.py"), exports="env")
