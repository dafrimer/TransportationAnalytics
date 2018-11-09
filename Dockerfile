FROM jfloff/alpine-python

RUN apk add --update jq curl make bash \
  libc6-compat gcc musl-dev libffi-dev openssl-dev git
RUN pip install --upgrade pip pipenv
RUN pip install awscli
# Twilio Client
RUN pip install twilio


#ENV DOCKER_VERSION "18.03.0-ce"
#RUN wget -q -P /tmp https://download.docker.com/linux/static/stable/x86_64/docker-$DOCKER_VERSION.tgz \
#    && tar -xz -C /tmp -f /tmp/docker-$DOCKER_VERSION.tgz \
#    && mv /tmp/docker/docker /usr/bin \
#    && rm -rf /tmp/docker /tmp/docker-$DOCKER_VERSION.tgz