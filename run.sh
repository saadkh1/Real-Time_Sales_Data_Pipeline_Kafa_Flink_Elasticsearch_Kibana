docker-compose build

docker-compose up -d

sleep 10

docker-compose exec jobmanager ./bin/flink run -py /opt/pyflink/main.py -d
