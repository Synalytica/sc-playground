# syntax=docker/dockerfile:1

FROM node:12-alpine

RUN apk add --no-cache python3
RUN apk add --no-cache curl
RUN apk add --no-cache bash

RUN curl -s https://smartpy.io/cli/install.sh > installSmartPy.sh
RUN chmod +x installSmartPy.sh
RUN yes | ./installSmartPy.sh

WORKDIR /app

COPY . .

CMD ["bash"]