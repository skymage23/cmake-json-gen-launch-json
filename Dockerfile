FROM fedora:41
LABEL name="skymage23/cmake-json-gen-launch-json-dev-container"
LABEL maintainer="skymage23@gmail.com"
LABEL version="1.0"
RUN dnf install -y which python3 python3-jsonschema python3-referencing cmake
RUN dnf install -y libicu krb5-libs openssl-libs zlib clang gcc gcc-c++
ADD https://github.com/PowerShell/PowerShell/releases/download/v7.5.1/powershell-7.5.1-1.rh.x86_64.rpm /powershell-7.5.1-1.rh.x86_64.rpm
RUN rpm -i powershell-7.5.1-1.rh.x86_64.rpm
RUN dnf install -y git