FROM ktbr/knp-juman AS builder

RUN wget http://download.cdn.yandex.net/mystem/mystem-3.1-linux-64bit.tar.gz && \
    tar xf mystem-3.1-linux-64bit.tar.gz &&\
    cp mystem /usr/local/bin/mystem &&\
    rm -rf mystem-3.1-linux-64bit.tar.gz

FROM amd64/python:3.7.7
WORKDIR /root

COPY --from=builder /usr/local /usr/local

RUN apt-get update --fix-missing && apt-get upgrade -y --fix-missing &&\
    apt-get install -y --fix-missing libjuman4 &&\
    apt-get clean

ADD requrements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt
RUN pip --no-cache-dir install git+https://github.com/nlpub/pymystem3
RUN pip --no-cache-dir install jupyter jupyterlab
