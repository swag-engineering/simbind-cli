FROM mathworks/matlab-deps:r2023b AS builder

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install --no-install-recommends --yes \
    wget unzip ca-certificates adduser \
    python3 libpython3.10 python3-dev python-is-python3 python3-pip python3-venv build-essential cmake swig \
    && apt-get clean \
    && apt-get autoremove

RUN wget -q https://www.mathworks.com/mpm/glnxa64/mpm \
    && chmod +x mpm && ./mpm install \
    --release=r2023b \
    --destination=/opt/matlab/R2023b \
    --products MATLAB Simulink MATLAB_Coder Simulink_Coder Embedded_Coder \
    || (echo "MPM Installation Failure. See below for more information:" && cat /tmp/mathworks_root.log && false) \
    && rm -f mpm /tmp/mathworks_root.log \
    && ln -s /opt/matlab/R2023b/bin/matlab /usr/local/bin/matlab

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/matlab/R2023b/bin/glnxa64

FROM builder

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install simbind

# License options:

# Option 1 [https://github.com/mathworks-ref-arch/matlab-dockerfile/blob/main/Dockerfile#L71]:
# ENV MLM_LICENSE_FILE=27000@MyServerName

# Option 2 [https://github.com/mathworks-ref-arch/matlab-dockerfile/blob/main/Dockerfile#L78]:
# COPY network.lic /opt/matlab/R2023b/licenses/

# Option 3 [https://github.com/swag-engineering/simbind-cli?tab=readme-ov-file#docker-usage]
COPY license_info.xml /opt/matlab/R2023b/licenses/license_info.xml

########### to view prints #############
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
########################################