FROM python:3.6-alpine3.6
#RUN wget -q -O - http://mozilla.debian.net/archive.asc | apt-key add - && \
#    echo "deb http://mozilla.debian.net/ jessie-backports firefox-release" > /etc/apt/sources.list.d/mozilla-firefox.list && \
RUN apk --update --no-cache add alpine-sdk gcc firefox-esr libffi-dev libxml2 libxml2-dev libxslt libxslt-dev \
        openssl-dev wget && \
    rm  -rf /tmp/* /var/cache/apk/*

ENV GECKODRIVER_VERSION v0.19.1

RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz" && \
    tar -xvzf geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz -C /usr/local/bin/ && \
    rm geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz

RUN pip install lxml cryptography
