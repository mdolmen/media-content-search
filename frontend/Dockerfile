FROM node:lts-alpine

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

RUN npm install @vue/cli

COPY *.json *.ts index.html .
COPY src/ ./src
COPY public/ ./public
RUN npm install

EXPOSE 5173
