# syntax=docker/dockerfile:experimental
FROM quay.io/quarkus/centos-quarkus-maven:20.0.0-java11 AS builder
WORKDIR build
COPY pom.xml pom.xml
RUN --mount=type=cache,target=/root/.m2 mvn dependency:go-offline
COPY src src
RUN --mount=type=cache,target=/root/.m2 mvn -Dnative -Dquarkus.native.container-build=true package

FROM cescoffier/native-base:latest
WORKDIR work
COPY --from=builder /build/target/*-runner /work/application
EXPOSE 8080
CMD ["./application", "-Dquarkus.http.host=0.0.0.0"]
