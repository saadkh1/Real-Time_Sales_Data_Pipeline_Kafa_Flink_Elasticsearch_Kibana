@echo off
echo Building Docker containers...
docker-compose build
docker-compose up -d

echo Waiting for services to initialize (sleeping for 10 seconds)...
timeout /t 10 > nul

echo Create Kafka topic...
docker-compose exec kafka /bin/bash -c "sleep 10 && /kafka-setup.sh"

echo Executing Flink job...
docker-compose exec jobmanager ./bin/flink run -py /opt/pyflink/main.py -d

echo Script execution completed.
