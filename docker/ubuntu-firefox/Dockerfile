FROM ubuntu:16.04
#RUN wget -q -O - http://mozilla.debian.net/archive.asc | apt-key add - && \
#    echo "deb http://mozilla.debian.net/ jessie-backports firefox-release" > /etc/apt/sources.list.d/mozilla-firefox.list && \
RUN apt-get update && apt-get install -y firefox python3-pip python3-dev wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV GECKODRIVER_VERSION v0.19.1

RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz"
RUN tar -xvzf geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz -C /usr/local/bin/
RUN rm geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz
