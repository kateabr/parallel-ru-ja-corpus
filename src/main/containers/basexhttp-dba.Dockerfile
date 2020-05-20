FROM garthk/unzip:latest AS downloader
ADD "http://files.basex.org/releases/9.3.2/BaseX932.zip" .
RUN unzip "BaseX932.zip"

FROM basex/basexhttp:9.3.2
COPY --from=downloader unzip/basex/webapp /srv/basex/webapp
