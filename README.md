# Simbind CLI

Generate Python Wheel package from Simulink model! Please refer
to [Wiki](https://github.com/swag-engineering/simbind-cli/wiki/Motivation)
and [Examples](https://github.com/swag-engineering/simbind-cli/tree/master/examples) to explore the project's
capabilities and limitations.

![Single Loop Feedback](https://raw.githubusercontent.com/swag-engineering/simbind-cli/master/examples/SingleLoopFeedback/SingleLoopFeedback.png)

## Requirements

To use the tool you need:

- Linux x86-64 machine with installed Matlab R2023b or older.
- Python 3.10 or 3.11: [Simbind Architect](https://github.com/swag-engineering/simbind-architect#Requirements) requires
  Python 3.10+ and [Simulink Exporter](https://github.com/swag-engineering/simulink-exporter#Requirements) needs Python
  3.9, 3.10 or 3.11
- From Matlab side you need Simulink suite with Simulink Coder.
- You also need pip, gcc, cmake, make and swig. Under Debian-based distros you can install it with
  ```bash
  sudo apt-get install python3-pip build-essential cmake swig
  ```

To run output model you need only Linux x86-64 machine and Python 3.8+. We're open to extending support to Linux ARM and
Windows x86-64 if there's sufficient interest!

## Installation

To install from PyPi run

```bash
$ pip install simbind 
```

To clone project you will also need to pull submodules with:

```bash
$ git clone --recurse-submodules https://github.com/swag-engineering/simbind-cli.git
```

## Usage

Simbind CLI is a wrapper around [Simulink Exporter](https://github.com/swag-engineering/simulink-exporter)
and [Simbind Architect](https://github.com/swag-engineering/simbind-architect) projects and intended to be used as a
standalone tool, not as an importable module. If you want to use its functionality programmatically, please refer to
subprojects.

```bash
$ simbind --help
usage: simbind [-h] --slx-path SLX_PATH [--pkg-name PKG_NAME] [--wheel-out-dir WHEEL_OUT_DIR]
               [--solver {ode1,ode2,ode3,ode4,ode5,ode8,ode14x,ode1be}] [--step STEP_SIZE]
               [--license-text LICENSE_TEXT] [-v]

Tool to generate Python wheel package from Simulink model.

options:
  -h, --help            show this help message and exit
  --slx-path SLX_PATH   Path to Simulink .slx file.
  --pkg-name PKG_NAME   Name of the output Python package. (default: 'model')
  --wheel-out-dir WHEEL_OUT_DIR
                        Path to folder where wheel package will be stored. (default: '.')
  --solver {ode1,ode2,ode3,ode4,ode5,ode8,ode14x,ode1be}
                        Fixed-step solver. (default: 'ode5')
  --step STEP_SIZE      Fixed step size in seconds. (default: '0.001')
  --license-text LICENSE_TEXT
                        License text that will be included in output Python wheel package. (default: '')
  -v                    Specifies the level of verbosity. Example: -vvv
```

## Issues

If you run into any issues or believe additional functionality is needed, please don't hesitate to open an issue or
email us at contact@swag-engineering.io. We're always ready to assist!