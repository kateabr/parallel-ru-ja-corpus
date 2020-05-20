FROM debian:buster
WORKDIR /root

RUN apt update --fix-missing && apt-get upgrade -y --fix-missing &&\
    apt install -y --fix-missing wget gcc g++ make bzip2 cmake xz-utils cmake xz-utils zlib1g-dev &&\
    apt install -y --fix-missing libjuman4

RUN wget https://github.com/ku-nlp/jumanpp/releases/download/v2.0.0-rc3/jumanpp-2.0.0-rc3.tar.xz &&\
    tar xf jumanpp-2.0.0-rc3.tar.xz &&\
    cd jumanpp-2.0.0-rc3 && mkdir build && cd build &&\
    cmake .. -DCMAKE_BUILD_TYPE=Release && make -j4 install &&\
    cd ../../ && rm -rf jumanpp-2.0.0-rc3.tar.xz jumanpp-2.0.0-rc3

RUN wget http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/juman/juman-7.01.tar.bz2 &&\ 
    tar xf juman-7.01.tar.bz2 &&\
    cd juman-7.01 && ./configure && make && make -j4 install &&\
    cd .. && rm juman-7.01.tar.bz2 && rm -rf juman-7.01

# original mirror (too slow): http://nlp.ist.i.kyoto-u.ac.jp/nl-resource/knp/knp-4.19.tar.bz2
RUN wget https://distfiles.macports.org/knp/knp-4.19.tar.bz2 &&\
    tar xf knp-4.19.tar.bz2 &&\
    cd knp-4.19 && ./configure && make && make -j4 install &&\
    cd .. && rm knp-4.19.tar.bz2 && rm -rf knp-4.19
