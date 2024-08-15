FROM postgres:16.4-alpine3.20

ENV POSTGRES_PASSWORD=socioclub
ENV POSTGRES_USER=socioclub
ENV POSTGRES_DB=socioclub

EXPOSE 30000

COPY ./init.sql /docker-entrypoint-initdb.d/

