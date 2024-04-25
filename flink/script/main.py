from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_processing():
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(stream_execution_environment=env)
    t_env.get_config().get_configuration().set_boolean("python.fn-execution.memory.managed", True)

    create_kafka_source_ddl = """
        CREATE TABLE `Order`(
            sale_time STRING,
            pos_id INT,
            pos_name STRING,
            article STRING,
            quantity DOUBLE,
            unit_price DOUBLE,
            total DOUBLE,
            sale_type STRING,
            payment_mode STRING
        ) WITH (
          'connector' = 'kafka',
          'topic' = 'Order',
          'properties.bootstrap.servers' = '172.18.0.5:9092',
          'properties.group.id' = 'my_flink_consumer_group',
          'scan.startup.mode' = 'latest-offset',
          'format' = 'json'
        )
    """

    create_es_sink_ddl = """
        CREATE TABLE es_sink(
            sale_time STRING,
            `year` INT,
            `month` INT,
            `week` INT,
            `day_name` STRING,
            pos_id INT,
            pos_name STRING,
            article STRING,
            quantity DOUBLE,
            unit_price DOUBLE,
            total DOUBLE,
            sale_type STRING,
            payment_mode STRING
        ) WITH (
            'connector' = 'elasticsearch-7',
            'hosts' = 'http://172.18.0.8:9200',
            'index' = 'platform_order',  -- Use lowercase index name
            'document-id.key-delimiter' = '$',
            'sink.bulk-flush.max-size' = '42mb',
            'sink.bulk-flush.max-actions' = '32',
            'sink.bulk-flush.interval' = '1000',
            'sink.bulk-flush.backoff.delay' = '1000',
            'format' = 'json'
        )
    """

    insert_into_es_sink_sql = """
        INSERT INTO es_sink (sale_time, `year`, `month`, `week`, `day_name`, pos_id, pos_name, article, quantity, unit_price, total, sale_type, payment_mode)
        SELECT 
            sale_time,
            CAST(EXTRACT(YEAR FROM CAST(sale_time AS TIMESTAMP)) AS INT),
            CAST(EXTRACT(MONTH FROM CAST(sale_time AS TIMESTAMP)) AS INT),
            CAST(EXTRACT(WEEK FROM CAST(sale_time AS TIMESTAMP)) AS INT),
            DATE_FORMAT(CAST(sale_time AS TIMESTAMP), 'EEEE'),
            pos_id,
            pos_name,
            article,
            quantity,
            unit_price,
            total,
            sale_type,
            payment_mode
        FROM `Order`
    """

    try:
        logger.info("Creating Kafka source table...")
        t_env.execute_sql(create_kafka_source_ddl)

        logger.info("Creating Elasticsearch sink table...")
        t_env.execute_sql(create_es_sink_ddl)

        logger.info("Inserting data into Elasticsearch sink...")
        t_env.execute_sql(insert_into_es_sink_sql)

        logger.info("Job executed successfully.")
    except Exception as e:
        logger.error(f"Job failed with error: {str(e)}")

if __name__ == '__main__':
    log_processing()
