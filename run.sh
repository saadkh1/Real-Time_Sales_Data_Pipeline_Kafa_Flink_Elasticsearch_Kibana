docker-compose build

docker-compose up -d

sleep 10

docker-compose exec jobmanager ./bin/flink run -py /opt/pyflink/main.py -d

sleep 10

docker-compose exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh --create --if-not-exists --topic $TOPIC_NAME --replication-factor 1 --partitions 1 --bootstrap-server 172.18.0.5:9092
echo "topic $TOPIC_NAME was created"