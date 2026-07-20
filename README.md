# PlatformIO Platform for SMLIGHT SMHUB

This repository provides the native [PlatformIO](https://platformio.org/) platform for the **SMLIGHT SMHUB** hardware, which is powered by the SG2000 SoC.

Specifically, this platform targets the **RISC-V C906L** "little core" (RTOS core) of the SG2000, enabling bare-metal and FreeRTOS development. It was purpose-built to support the native integration of [ESPHome](https://esphome.io/) onto the SMHUB hardware.

## Features

- **Architecture:** RISC-V (C906L)
- **Frameworks:** FreeRTOS (bundled with OpenAMP, libmetal, and nanopb for IPC with the main Linux cores)
- **Toolchain:** Pre-configured RISC-V GCC Toolchain via xPack
- **Boards:** SMLIGHT SMHUB

## Usage

To compile projects for the SMHUB little core using PlatformIO, configure your `platformio.ini` environment as follows:

```ini
[env:smhub]
platform = https://github.com/smlight-smhub/platform-sg2000.git
framework = freertos
board = smhub
```

## Architecture & IPC

The SG2000 is a heterogeneous SoC. While the primary cores run Linux, this PlatformIO package targets the dedicated RISC-V C906L core.

To facilitate communication between the Linux host and this RISC-V core, the bundled FreeRTOS framework (`framework-sg2000-rtos`) includes integrated support for **OpenAMP** and **libmetal**. This allows developers (and ESPHome) to seamlessly exchange messages across the processor boundaries via shared memory and RPMsg.

## Local Development (Advanced)

If you are modifying the underlying `framework-sg2000-rtos` source code and need to test it against this platform, you can point PlatformIO to your local framework directory using `platform_packages`. 

In your `platformio.ini`:

```ini
[env:smhub]
platform = https://github.com/smlight-smhub/platform-sg2000.git
framework = freertos
board = smhub
platform_packages =
    framework-sg2000-rtos @ symlink:///path/to/your/local/framework-sg2000-rtos
```

---
*(C) 2026 SMLIGHT All rights reserved.*
