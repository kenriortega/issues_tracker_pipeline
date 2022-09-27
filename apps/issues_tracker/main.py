#!/usr/bin/env python

import logging
import sys
from config import config
import json
from confluent_kafka import Producer

from jira import JIRA, Issue


def delivery_report(err, msg):
    """
    Reports the success or failure of a message delivery.
    Args:
        err (KafkaError): The error that occurred on None on success.
        msg (Message): The message that was produced or failed.
    """

    if err is not None:
        print("Delivery failed for User record {}: {}".format(msg.key(), err))
        return


def fetch_issues_from_project_name(project: str = "AIRFLOW", max_result: int = 1_000, start_at=0):
    jira = JIRA(server="https://issues.apache.org/jira/")
    issues = jira.search_issues(jql_str=f"project = {project} ORDER BY created DESC",
                                maxResults=max_result,
                                fields='priority,summary,status,project,created,key,issuetype',
                                startAt=start_at)
    yield from issues
    if len(issues.iterable) != 0:
        yield from fetch_issues_from_project_name(project, max_result, start_at + max_result)


def extract_details_data_jira(issue: Issue) -> dict:
    result = {
        "key": issue.key,
        "summary": issue.fields.summary,
        "priority": issue.fields.priority.raw.get("name"),
        "issue_type": issue.fields.issuetype.raw.get("name"),
        "status": issue.fields.status.raw.get("name"),
        "project": issue.fields.project.raw.get("name"),
        "created": issue.fields.created,
        "source": "jira"
    }
    return result


def main():
    logging.info("START")
    kafka_config = config.get("kafka")
    producer = Producer(kafka_config)

    for issue in fetch_issues_from_project_name():
        result = extract_details_data_jira(issue)
        producer.produce(
            topic="issues",
            key=result.get("key"),
            value=json.dumps(result),
            on_delivery=delivery_report
        )
        print("\nFlushing records...")
        producer.flush()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
