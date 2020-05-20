FROM node:lts AS cache
WORKDIR cache
COPY package.json yarn.lock ./
RUN yarn --frozen-lockfile

FROM node:lts AS builder
WORKDIR build
COPY --from=cache /cache .
COPY . .
RUN yarn run build:prod

FROM nginx:mainline
COPY --from=builder /build/src/main/nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=builder /build/src/main/nginx/mime.types /etc/nginx/conf/mime.types
COPY --from=builder /build/target/spa /var/www/application
EXPOSE 8081
CMD ["nginx", "-g", "daemon off;"]
