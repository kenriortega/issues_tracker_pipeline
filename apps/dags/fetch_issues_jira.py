from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

from airflow.utils.dates import days_ago

from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from airflow.kubernetes.secret import Secret

secret_all_keys  = Secret('env', None, 'airflow-gh-token-secret')
env_var_secret = Secret(
    deploy_type='env',
    deploy_target='GITHUB_TOKEN',
    secret='airflow-gh-token-secret',
    key='GITHUB_TOKEN',
)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),

}
with DAG(
        'k8s_pod_op_for_fetch_issues_gh',
        default_args=default_args,
        description='kubernetes_workflow',
        schedule_interval=timedelta(days=1),
        start_date=days_ago(1),
        tags=['kubernetes_workflow'],
) as dag:
    fetch = KubernetesPodOperator(
        namespace='playground',
        name="fetch-jira-run",
        image="kenriortega/issue_tracker:v0.0.2",
        cmds=["python", "./main.py", "jira", "superset", "console"],
        # arguments=["jira superset console"],
        labels={"app": "fetch-jira"},
        task_id="dry_run_fetch_run",
        secrets=[env_var_secret, secret_all_keys],
    )

    fetch
