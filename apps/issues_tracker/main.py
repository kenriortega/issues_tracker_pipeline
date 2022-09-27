#!/usr/bin/env python

import logging
import sys
from config import config
import json
from confluent_kafka import Producer
from github import Github
import os
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


def send_data_to_kafka(producer: Producer, data: dict):
    """
    Sen data to apache kafka.
    Args:
        producer (Producer): The producer object.
        data (dict): The data dict.
    """
    producer.produce(
        topic="issues",
        key=data.get("key"),
        value=json.dumps(data),
        on_delivery=delivery_report
    )
    print("\nFlushing records...")
    producer.flush()


def fetch_issues_by_project_from_jira(project: str = "KAFKA", max_result: int = 1_000, start_at=0):
    """
    Fetch issues form jira by a specific project name
    Args:
        project (str): The  Name project to get issues.
        max_result (int): The max number to get result data.
        start_at (int): The index to start to fetch data.
    """
    jira = JIRA(server="https://issues.apache.org/jira/")
    issues = jira.search_issues(jql_str=f"project = {project} ORDER BY created DESC",
                                maxResults=max_result,
                                fields='priority,summary,status,project,created,key,issuetype',
                                startAt=start_at)
    yield from issues
    if len(issues.iterable) != 0:
        yield from fetch_issues_by_project_from_jira(project, max_result, start_at + max_result)


def extract_details_data_jira(issue: Issue) -> dict:
    """
    Extract details from an issue
    Args:
        issue (Issue): The Issue type by jira api.
    Returns:
        dict
    """
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


def extract_details_data_github(issue, project) -> dict:
    """
    Extract details from an issue
    Args:
        issue (GithubIssue): The Issue.
        project (str): The project name.
    Returns:
        dict
    """
    labels_kind = filter(lambda label: "kind:" in label.name, issue.labels)
    kinds = list(map(lambda x: x.name, list(labels_kind)))
    labels_priority = filter(lambda label: "priority:" in label.name, issue.labels)
    priorities = list(map(lambda x: x.name, list(labels_priority)))
    priority = priorities[0] if len(priorities) > 0 else "undefined"
    kind = kinds[0] if len(kinds) > 0 else "undefined"
    result = {
        "key": f"{issue.id}_{issue.number}",
        "summary": issue.title,
        "priority": priority,
        "issue_type": kind,
        "status": issue.state,
        "project": project,
        "created": issue.created_at,
        "source": "github"
    }

    return result


def fetch_issues_by_project_from_github(project: str):
    """
    Fetch issues form GitHub by a specific repo name
    Args:
        project (str): The repo name from GitHub.
    Returns:
        dict
    """
    token = os.getenv('GITHUB_TOKEN')
    g = Github(token)
    repo = g.get_repo(project)
    issues = repo.get_issues()
    yield from issues


def main():
    logging.info("START")
    kafka_config = config.get("kafka")
    producer = Producer(kafka_config)

    for issue in fetch_issues_by_project_from_jira(project="KAFKA"):
        result = extract_details_data_jira(issue)
        send_data_to_kafka(producer, result)

    for issue in fetch_issues_by_project_from_github(project="apache/airflow"):
        result = extract_details_data_github(issue, project="apache/airflow")
        send_data_to_kafka(producer, result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
