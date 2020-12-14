FROM python:2
RUN pip install pip install faker \
                            numpy \
                            pytz \
                            tzlocal
COPY apache-fake-log-gen.py /
COPY requirements.txt /
COPY LICENSE /
ENTRYPOINT ["python","/apache-fake-log-gen.py"]