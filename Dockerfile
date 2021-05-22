FROM python:3.8-alpine
LABEL author=pk13055, version=1.0

ENV OUTPUT_DIR="/app/results"
RUN mkdir -p /usr/local $OUTPUT_DIR

RUN apk add --update --no-cache curl bash npm \
 && curl https://smartpy.io/cli/install.sh > install.sh \
 && yes | sh install.sh \
 && rm -rf install.sh \
 && cd /root/smartpy-cli/ \
 && mv SmartPy.sh smartpy

WORKDIR /app

ENV PATH="/root/smartpy-cli:$PATH"
COPY . .

CMD ["./entrypoint.sh"]

