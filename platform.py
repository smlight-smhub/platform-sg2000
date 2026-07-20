#
# Copyright (c) 2026 SMLIGHT. All rights reserved.
#

import platform as sys_platform
import os
from platformio.managers.platform import PlatformBase

class Sg2000Platform(PlatformBase):
    def configure_default_packages(self, variables, targets):
        system = sys_platform.system().lower()
        machine = sys_platform.machine().lower()
        
        toolchain_pkg = self.packages.get("toolchain-riscv-xpack")
        if toolchain_pkg:
            if system == "linux" and (machine == "aarch64" or machine.startswith("arm64")):
                toolchain_pkg["version"] = "https://orion.feathertop.ovh/static/archive/xpack-riscv-none-elf-gcc-15.2.0-1-linux-aarch64-pio-rv64gc.tar.gz"
            else:
                toolchain_pkg["version"] = "https://orion.feathertop.ovh/static/archive/xpack-riscv-none-elf-gcc-15.2.0-1-linux-x64-pio-rv64gc.tar.gz"

        return super().configure_default_packages(variables, targets)
