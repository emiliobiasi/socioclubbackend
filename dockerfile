FROM postgres:16.4-alpine3.20

EXPOSE 30000

COPY ./init.sql /docker-entrypoint-initdb.d/