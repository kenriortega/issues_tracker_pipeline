from datetime import timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from airflow.kubernetes.secret import Secret
from airflow.kubernetes.pod import Resources

pod_resources = Resources()
pod_resources.request_cpu = '500m'
pod_resources.request_memory = '256Mi'
pod_resources.limit_cpu = '1000m'
pod_resources.limit_memory = '500Mi'

secret_all_keys = Secret('env', None, 'airflow-gh-token-secret')
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
        'k8s_pod_op_for_fetch_issues_superset_gh',
        default_args=default_args,
        description='kubernetes_workflow',
        schedule_interval=timedelta(days=1),
        start_date=days_ago(1),
        tags=['k8s', 'gh'],
) as dag:
    fetch_gh = KubernetesPodOperator(
        namespace='default',
        name="fetch-github-run",
        image="kenriortega/issue_tracker:v0.0.4",
        cmds=["python", "./main.py", "github", "apache/superset", "kafka"],
        # arguments=["github apache/superset console"],
        labels={"app": "fetch-github"},
        task_id="dry_run_fetch_issues_superset_gh",
        secrets=[env_var_secret, secret_all_keys],
        # pass your name as an environment var
        env_vars={
            "BOOSTRAP_SERVERS": "kafka-tf-release.default.svc:9092"
        },
        resources=pod_resources
    )
    t3 = BashOperator(
        task_id='notifier',
        bash_command='printf "Completed {{ execution_date.strftime("%d-%m-%Y") }}"',
        dag=dag,
    )

    fetch_gh >> t3
