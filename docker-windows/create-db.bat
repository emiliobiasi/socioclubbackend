:: Executar esse arquivo apenas quando não tiver o container criado 
docker build ./ -t socioclubdb:latest
docker run --name socioclubdb -e POSTGRES_PASSWORD=socioclub -e POSTGRES_USER=socioclub -e POSTGRES_DB=socioclub -p 5431:5432 socioclubdb

