# Parallel Russian-Japanese Corpus
This is a repository for Parallel Russian-Japanese Corpus.

Project URL: `TBD`

Project consists of 3 modules:
* XML Database (powered by [`BaseX`](http://basex.org))
* Backend API (powered by [`Quarkus`](https://quarkus.io))
* Frontend SPA (powered by [`Vue.js`](https://vuejs.org))

## Building and running
Requirements:
* JDK 11+
* Maven
* Yarn
* Docker

All described commands must be launched from project root.

### Running
Project comes with `docker-compose` file. Use it to spin-up all modules:
```shell script
docker-compose -f src/main/containers/docker-compose.yaml up -d
``` 
and for turning everything off:
```shell script
docker-compose -f src/main/containers/docker-compose.yaml down
``` 

Then you can access services with the following URLs:
* `localhost:8081` - frontend application
* `localhost:8080` - backend API
* `localhost:1984` - database
* `localhost:8984` - database admin panel

### Building
All dockerfiles require `Build Kit` support, which can be activated with:
```shell script
```shell script
set DOCKER_BUILDKIT=1 # or export DOCKER_BUILDKIT=1
```

Backend:
```shell script
docker build -f src/main/containers/backend-jvm.Dockerfile -t ktbr/parallel-ru-ja-corpus-backend:<version> .
```
Alternatively, you can build a memory efficient native image:
```shell script
docker build -f src/main/containers/backend-native.Dockerfile -t ktbr/parallel-ru-ja-corpus-backend:<version> .
```
**WARNING!** Building backend as native image requires a huge amount of CPU and RAM and may take up to 5-10 minutes. 
Recommended system requirements are 4 cores and 16GiB RAM. You should probably close your web browser, IDE etc as well.

Frontend:
```shell script
docker build -f src/main/containers/frontend.Dockerfile -t ktbr/parallel-ru-ja-corpus-frontend:<version> .
```

## Database
Before you can start querying the service, you'll need to upload database along with `XQuery` module:

1. Connect to `BaseX` and create database with the name `parallel-ru-ja-corpus` and upload XML files.
2. Add [xquery module](src/main/xquery) to `/repo` in your `BaseX` home directory.

If you want to support a project and contribute data to corpus, please refer to `XSD schema` [here](src/main/texts/entry-schema-1.0.xsd). You can find `Python` generators inside `src/main/python`.
