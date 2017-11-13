FROM python:3.6

RUN apt-get update && apt-get install -y xvfb unzip && \
    curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt update && apt install -y google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV CHROMEDRIVER_VERSION 2.33
ENV CHROMEDRIVER_SHA256 87d0059ab1579ec9c10ef34ab9817feea59e19a96c029d78349a57c36db5bb74

RUN curl -SLO "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" && \
    echo "$CHROMEDRIVER_SHA256  chromedriver_linux64.zip" | sha256sum -c - && \
    unzip "chromedriver_linux64.zip" -d /usr/local/bin && \
    rm "chromedriver_linux64.zip"
