FROM --platform=linux/amd64 locustio/locust

USER root
RUN apt-get update && apt-get -y install gcc && apt-get install libkrb5-dev -y

ENV WORKDIR /locust
WORKDIR ${WORKDIR}

ADD ./requirements.txt .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/bin/sh", "-c"]

USER locust