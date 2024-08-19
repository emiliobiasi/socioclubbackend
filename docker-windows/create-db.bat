:: Executar esse arquivo apenas quando não tiver o container criado 
docker build ../ -t socioclubdb
docker run --name socioclubdb -p 5432:5432 socioclubdb
