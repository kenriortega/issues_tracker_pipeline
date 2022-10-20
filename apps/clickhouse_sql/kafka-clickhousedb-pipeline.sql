
-------------------------------------------

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
    source_type String,
    topic     String,
    partition UInt64,
    offset UInt256,
) ENGINE = MergeTree -- ReplacingMergeTree
PARTITION BY (toYYYYMM(created),project)
ORDER BY (key_id);

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
    source_type String,
)
ENGINE = Kafka('kafka-tf-release.data-ingestion.svc:9092', 'issues', 'clickhouse-issues-gp',
             'JSONEachRow') settings kafka_thread_per_consumer = 0, kafka_num_consumers = 1;

-- TODO create MV for analytic process. (summary)
-- TODO: check if upsert is here?
--  Create the materialized view
CREATE MATERIALIZED VIEW default.issues_mv TO default.issues AS
SELECT *, _topic as topic, _partition as partition, _offset as offset
FROM default.issues_queue;

-----

SELECT project,count(*) as issues_count from issues GROUP BY project;

OPTIMIZE TABLE issues DEDUPLICATE;

SELECT
    partition,
    name,
    active
FROM system.parts
WHERE table = 'issues'
