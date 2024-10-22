#Executar quando não tiver o container criado
docker build ./ -t socioclubdb
docker run --name socioclubdb -e POSTGRES_PASSWORD=socioclub -e POSTGRES_USER=socioclub -e POSTGRES_DB=socioclub -p 5431:5432 socioclubdb
