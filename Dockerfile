FROM jfloff/alpine-python:2.7-slim
MAINTAINER clma <claus.matzinger+kb@gmail.com>

RUN apk add --no-cache git musl-dev linux-headers g++ python-dev
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
RUN mkdir /faker /out && git clone https://github.com/kiritbasu/Fake-Apache-Log-Generator.git /faker
RUN cd /faker && pip install -r requirements.txt
WORKDIR /faker
CMD ["python","apache-fake-log-gen.py", "-o LOG", "-p /out/web", "-n 0"]
