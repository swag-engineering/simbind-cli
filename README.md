# Simbind CLI

Generate Python Wheel package from Simulink model to enhance
your [Software-in-Loop](https://de.wikipedia.org/wiki/Software_in_the_Loop) tests development workflow!
Please refer to [Wiki](https://github.com/swag-engineering/simbind-cli/wiki)
and [Examples](https://github.com/swag-engineering/simbind-cli/tree/master/examples) to explore the project's
capabilities and limitations.  
You also might be interested into [pytest-simbind](https://github.com/swag-engineering/pytest-simbind) plugin that
allows to test Simbind models with pytest!

![Single Loop Feedback](https://raw.githubusercontent.com/swag-engineering/simbind-cli/master/examples/SingleLoopFeedback/SingleLoopFeedback.png)

## Requirements

We highly recommend to use [Dockerized](https://github.com/swag-engineering/simbind-cli#Docker-Usage) version of
Simbind, since collecting the correct versions of the necessary requirements can be challenging. If you opt for local
installation, the following is required:

- Linux x86-64 machine with installed Matlab R2023b.
- Python 3.10 or 3.11: [Simbind Architect](https://github.com/swag-engineering/simbind-architect#Requirements) requires
  Python 3.10+ and [Simulink Exporter](https://github.com/swag-engineering/simulink-exporter#Requirements) needs Python
  3.9, 3.10 or 3.11.
- From Matlab side you need Simulink suite with Embedded Coder.
- You also need pip, gcc, cmake, make and swig. Under Debian-based distros you can install it with
  ```bash
  sudo apt-get install python3-pip build-essential cmake swig
  ```

To run output model you need Python 3.8+; Mock model can be used under any OS, SiL model requires Linux x86-64 machine.
To learn more about Mock and SiL packages structure and usage, refer
to [Wiki](https://github.com/swag-engineering/simbind-cli/wiki/Python-Package-Structure).

## Installation

To install from PyPi run

```bash
$ pip install simbind 
```

Please, notice that you will need to satisfy [requirements](#requirements) before running pip!

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
               [--license-text LICENSE_TEXT] [--matlab-include SIMULINK_PATHS] [--use-ansi-c]
               [--preprocessor-def PREPROCESSOR_DEFS] [-v]

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
  --matlab-include MATLAB_PATH
                        Path to the folder that will be included into Matlab path. Can be used multiple
                        times.Example: --matlab-include /some/path --matlab-include /another/path
  --use-ansi-c          During build Matlab/Simulink will use C89/90 (ANSI) instead of C99
  --preprocessor-def PREPROCESSOR_DEF
                        Predefine name as a macro that will be passed to preprocessor. Can be used multiple
                        times.Example: --preprocessor-def "__attribute__(x)=" --preprocessor-def "DEBUG=1"
  -v                    Specifies the level of verbosity. Example: -vvv

```

For detailed instructions on the structure of the output Python package, please refer to
our [Wiki](https://github.com/swag-engineering/simbind-cli/wiki/Python-Package-Structure).

### Docker Usage

> Disclaimer  
> Before utilizing Docker containers to run MathWorks products, it is crucial to verify that your licensing agreement
> with MathWorks explicitly permits such usage. Licensing terms can vary, and it is the responsibility of the user to
> ensure compliance with these terms to avoid potential violations.

The primary challenge in using MathWorks products within Docker containers lies in the licencing the application.
MathWorks offers various license types, detailed
further [here](https://www.mathworks.com/matlabcentral/answers/116637-what-are-the-differences-between-the-license-lic-license-dat-network-lic-and-license_info-xml-lic?s_tid=srchtitle).
If you have access to a network license or your organization utilizes
a [License Manager](https://www.mathworks.com/help/install/administer-network-licenses.html) through their organization,
you can uncomment the corresponding option in
the [Dockerfile](https://github.com/swag-engineering/simbind-cli/blob/master/Dockerfile#L27). This section demonstrates
how to apply your Individual License for using Simbind in a Docker container.  
Since _R2023b_ MathWorks does not generate dedicated Individual license file that could be utilized inside Docker
container. Instead, it uses online license that requires you to login on a first use of newly installed Matlab:

- Log in into docker container and provide your credentials:
  ```bash
  $ docker run -it --ulimit nofile=65535:65535 ghcr.io/swag-engineering/simbind-cli/simbind-cli:latest matlab
  MATLAB is selecting SOFTWARE OPENGL rendering.
  Please enter your MathWorks Account email address and press Enter: your@email.com
  Please enter your MathWorks Account password and press Enter:
  ```
- Without terminating Docker session, in new
  terminal [commit changes](https://www.mathworks.com/help/cloudcenter/ug/save-changes-in-containers.html):
  ```bash
  $ docker ps
  CONTAINER ID   IMAGE                                                     COMMAND    CREATED         STATUS         PORTS     NAMES
  aef878e19c3f   ghcr.io/swag-engineering/simbind-cli/simbind-cli:latest   "matlab"   2 minutes ago   Up 2 minutes             focused_satoshi
  $ docker commit aef878e19c3f simbind-cli:licensed
  ```
- Terminate docker session in the first terminal with:
  ```
  >> exit()
  ```

Now that you have configured your license, you're all set to utilize the _simbind-cli:licensed_ image to use Simbind:

```bash
$ docker run --rm --ulimit nofile=65535:65535 \
  -v /path/to/model.slx:/tmp/model.slx \
  -v /path/to/output/dir:/tmp/output \
  simbind-cli:licensed \
  simbind \
  --slx-path /tmp/model.slx \
  --wheel-out-dir /tmp/output \
  --pkg-name fancypackage \
  --solver ode8 \
  --step 0.005
```

## Issues

If you run into any issues or believe additional functionality is needed, please don't hesitate to open an issue or
email us at contact@swag-engineering.io. We're always ready to assist!