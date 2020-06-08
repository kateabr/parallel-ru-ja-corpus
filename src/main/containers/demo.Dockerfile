# syntax=docker/dockerfile:experimental
FROM node:lts AS frontend-cache
WORKDIR cache
COPY package.json yarn.lock ./
RUN yarn --frozen-lockfile

FROM node:lts AS frontend-builder
WORKDIR build
COPY --from=frontend-cache /cache .

COPY src/main/typescript src/main/typescript
COPY public public
COPY .browserslistrc .browserslistrc
COPY .eslintrc.js .eslintrc.js
COPY tsconfig.json tsconfig.json
COPY vue.config.js vue.config.js
RUN yarn run build:prod
COPY src/main/nginx src/main/nginx

FROM maven:3.6.3-jdk-14 as backend-builder
WORKDIR build

COPY checkstyle.xml checkstyle.xml

COPY pom.xml pom.xml
RUN --mount=type=cache,target=/root/.m2 mvn dependency:go-offline

COPY src/main/java src/main/java
COPY src/main/resources src/main/resources
RUN --mount=type=cache,target=/root/.m2 mvn package


FROM debian:buster
WORKDIR demo

RUN apt update && apt install software-properties-common gnupg wget gettext-base -y && \
    wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add - && \
    add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ && \
    apt update && apt-get install adoptopenjdk-11-hotspot nginx nginx-extras -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# copy local basex installation
COPY basex basex

COPY --from=backend-builder /build/target/*-runner.jar backend.jar
COPY --from=backend-builder /build/target/lib/* lib/
COPY --from=frontend-builder /build/src/main/nginx/nginx-demo.conf nginx.template
COPY --from=frontend-builder /build/src/main/nginx/mime.types /etc/nginx/conf/mime.types
COPY --from=frontend-builder /build/target/spa /var/www/application

ENV PORT=8081

EXPOSE $PORT
CMD (nohup ./basex/bin/basexhttp &) && \
    (nohup java -Dbasex.host=localhost -cp "backend.jar:lib/*" io.quarkus.runner.GeneratedMain &)&& \
    (envsubst '${PORT}' < nginx.template > /etc/nginx/nginx.conf) && \
    nginx -g 'daemon off;'
