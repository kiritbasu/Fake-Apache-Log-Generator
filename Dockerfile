FROM alpine:3.7 as buildenv

ADD apache-fake-log-gen.py /apache-fake-log-gen.py

RUN apk add --update --no-cache python py-numpy py-tz py-pip && \
    pip install fake-factory==0.7.2 && \
    pip install Faker==0.7.3 && \
    pip install tzlocal==1.3.0 && \
    apk del py-pip && \
    chmod 0755 /apache-fake-log-gen.py

USER nobody

ENV NUM_LINES=0 DELAY_SECONDS=1.0

CMD ["/bin/sh","-c","/apache-fake-log-gen.py --num ${NUM_LINES} --sleep ${DELAY_SECONDS}"]
