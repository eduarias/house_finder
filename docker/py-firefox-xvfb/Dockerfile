FROM python:3.6

#RUN wget -q -O - http://mozilla.debian.net/archive.asc | apt-key add - && \
#    echo "deb http://mozilla.debian.net/ jessie-backports firefox-release" > /etc/apt/sources.list.d/mozilla-firefox.list && \
RUN apt update && apt install -y firefox-esr xvfb libxml2-dev \
    libxslt-dev \
    libssl-dev \
    zlib1g-dev \
    libyaml-dev \
    libffi-dev \ \
    libdbus-glib-1-2 libxcomposite1 && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV GECKODRIVER_VERSION v0.19.1

RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz"
RUN tar -xvzf geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz -C /usr/local/bin/
RUN rm geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz
