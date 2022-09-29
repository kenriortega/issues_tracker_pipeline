-- Create the destination table
CREATE TABLE default.issues
(
    key_id      String,
    summary     String,
    priority    String,
    issue_type  String,
    status      String,
    project     String,
    created     DateTime,
    source_type String
) ENGINE = MergeTree ORDER BY (created);

-- Create the Kafka table engine
CREATE TABLE default.issues_queue
(
    key_id      String,
    summary     String,
    priority    String,
    issue_type  String,
    status      String,
    project     String,
    created     DateTime,
    source_type String
)
    ENGINE = Kafka('kafka-kafka-1:9092', 'issues', 'clickhouse',
             'JSONEachRow') settings kafka_thread_per_consumer = 0, kafka_num_consumers = 1;

--  Create the materialized view
CREATE MATERIALIZED VIEW default.issues_mv TO default.issues AS
SELECT *
FROM default.issues_queue;

-- Confirm rows have been inserted
SELECT count()
FROM default.issues;


-- Stopping & restarting message consumption
DETACH TABLE issues_queue;
--
ATTACH TABLE issues_queue;

-- Adding Kafka Metadata
DETACH TABLE issues_queue;

ALTER TABLE issues
    ADD COLUMN topic     String,
    ADD COLUMN partition UInt64;

DROP VIEW default.issues_mv;

CREATE MATERIALIZED VIEW default.issues_mv TO default.issues AS
SELECT *, _topic as topic, _partition as partition
FROM default.issues_queue;

ATTACH TABLE issues_queue;

SELECT *
FROM default.issues;