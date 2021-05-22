FROM python:3.8-alpine
LABEL author=pk13055, version=1.0

RUN mkdir -p /usr/local /app/results

RUN apk add --update --no-cache curl bash npm \
 && curl https://smartpy.io/cli/install.sh > install.sh \
 && yes | sh install.sh \
 && rm -rf install.sh \
 && cd /root/smartpy-cli/ \
 && mv SmartPy.sh smartpy

WORKDIR /app

ENV PATH="/root/smartpy-cli:$PATH"
ENV PORT=8080
COPY . .

RUN npm i -g serve
ENTRYPOINT ["./entrypoint.sh"]

