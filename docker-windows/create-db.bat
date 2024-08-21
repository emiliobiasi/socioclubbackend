:: Executar esse arquivo apenas quando não tiver o container criado 
docker build ./ -t socioclubdb:latest
docker run --name socioclubdb -p 5432:5432 socioclubdb
