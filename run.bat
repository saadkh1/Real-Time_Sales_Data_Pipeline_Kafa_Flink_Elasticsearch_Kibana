@echo off
echo Building Docker containers...
docker-compose build
docker-compose up -d

echo Waiting for services to initialize (sleeping for 10 seconds)...
timeout /t 10 > nul

echo Executing Flink job...
docker-compose exec jobmanager ./bin/flink run -py /opt/pyflink/main.py -d

echo Create Kafka topic...
docker-compose exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh --create --if-not-exists --topic %TOPIC_NAME% --replication-factor 1 --partitions 1 --bootstrap-server 172.18.0.5:9092
echo "topic %TOPIC_NAME% was created"

echo Script execution completed.
