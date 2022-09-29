#!/usr/bin/env python

import logging
import sys
from config import config
import json
from datetime import datetime
from kafka import KafkaProducer
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


def send_data_to_kafka(producer: KafkaProducer, data: dict):
    """
    Sen data to apache kafka.
    Args:
        producer (Producer): The producer object.
        data (dict): The data dict.
    """
    producer.send(topic="issues", key=data.get("key_id"), value=data, )


def fetch_issues_by_project_from_jira(project: str = "KAFKA", max_result: int = 1_000, start_at=0):
    """
    Fetch issues form jira by a specific project name
    Args:
        project (str): The  Name project to get issues.
        max_result (int): The max number to get result data.
        start_at (int): The index to start to fetch data.
    """
    config_jira = config.get("jira")
    jira = JIRA(server=config_jira.get("url_base"))
    issues = jira.search_issues(jql_str=f"project = {project} ORDER BY created DESC",
                                maxResults=max_result,
                                fields=config_jira.get("fields"),
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
        "key_id": issue.key,
        "summary": issue.fields.summary,
        "priority": issue.fields.priority.raw.get("name", "undefined"),
        "issue_type": issue.fields.issuetype.raw.get("name", "undefined"),
        "status": issue.fields.status.raw.get("name", "undefined"),
        "project": issue.fields.project.raw.get("name", "undefined"),
        "created": issue.fields.created.split(".")[0],
        "source_type": "jira"
    }
    return result


def get_priority_and_kind_from_labels_gh(issue):
    """
    Extract priority & kind from labels
    Args:
        issue (GithubIssue): The Issue.
    Returns:
        Tuple[str,str]
    """
    labels_kind = filter(lambda label: "kind:" in label.name, issue.labels)
    kinds = list(map(lambda x: x.name, list(labels_kind)))
    labels_priority = filter(lambda label: "priority:" in label.name, issue.labels)
    priorities = list(map(lambda x: x.name, list(labels_priority)))
    priority = priorities[0] if len(priorities) > 0 else "undefined"
    kind = kinds[0] if len(kinds) > 0 else "undefined"
    return priority, kind


def extract_details_data_github(issue, project) -> dict:
    """
    Extract details from an issue
    Args:
        issue (GithubIssue): The Issue.
        project (str): The project name.
    Returns:
        dict
    """
    priority, kind = get_priority_and_kind_from_labels_gh(issue)
    result = {
        "key_id": f"{issue.id}_{issue.number}",
        "summary": issue.title,
        "priority": priority,
        "issue_type": kind,
        "status": issue.state,
        "project": project,
        "created": issue.created_at,
        "source_type": "github"
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
    producer = KafkaProducer(
        bootstrap_servers=kafka_config.get("bootstrap.servers"),
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=str.encode
    )

    for issue in fetch_issues_by_project_from_jira(project="BEAM"):
        result = extract_details_data_jira(issue)
        send_data_to_kafka(producer, result)
    producer.close()
    # for issue in fetch_issues_by_project_from_github(project="apache/airflow"):
    #     result = extract_details_data_github(issue, project="apache/airflow")
    #     send_data_to_kafka(producer, result)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
