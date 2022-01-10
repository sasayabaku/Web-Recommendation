FROM python:3.10.0-slim-buster

SHELL [ "/bin/bash", "-c" ]
USER root

COPY ./requirements.txt requirements.txt
RUN pip install -r /requirements.txt

# Juman++ Install
RUN apt update
RUN apt install -y libboost-dev build-essential cmake
RUN wget https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc2/jumanpp-2.0.0-rc2.tar.xz
RUN tar xJvf jumanpp-2.00-rc2.tar.xz
WORKDIR /jumanpp-2.00-rc2
RUN mkdir build
WORKDIR /jumanpp-2.00-rc2/build
RUN cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr/local && \
    make && \
    make install

WORKDIR /
RUN rm -rf /jumanpp-2.00-rc2

# Install PyTorch
RUN pip3 install torch==1.10.0+cpu torchvision==0.11.1+cpu torchaudio==0.10.0+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html

# COPY ./src /src
# WORKDIR /src