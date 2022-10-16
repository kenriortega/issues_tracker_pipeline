from datetime import timedelta
# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.decorators import task
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

secret_all_keys = Secret('env', None, 'airflow-twitter-token-secret')
env_var_secret = Secret(
    deploy_type='env',
    deploy_target='TWITTER_BEARER_TOKEN',
    secret='airflow-twitter-token-secret',
    key='TWITTER_BEARER_TOKEN',
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
        'k8s_pod_op_for_fetch_tweets',
        default_args=default_args,
        description='kubernetes_workflow',
        schedule_interval=timedelta(days=1),
        start_date=days_ago(1),
        tags=['k8s', 'twitter'],
) as dag:
    fetch_gh = KubernetesPodOperator(
        namespace='data-processing',
        name="fetch-tweets-run",
        image="kenriortega/tweet_tracker:v0.0.1",
        cmds=["python", "./main.py"],
        # arguments=["github apache/superset console"],
        labels={"app": "fetch-tweets"},
        task_id="dry_run_fetch_tweets",
        secrets=[env_var_secret, secret_all_keys],
        resources=pod_resources,
        # push the contents from xcom.json to Xcoms. Remember to only set this
        # argument to True if you have created the `airflow/xcom/return.json`
        # file within the Docker container run by the KubernetesPodOperator.
        do_xcom_push=True
    )


    @task
    def load_data(**context):
        # pull the XCom value that has been pushed by the KubernetesPodOperator
        data = context['ti'].xcom_pull(
            task_ids='dry_run_fetch_tweets',
            key='return_value')
        print(data)

    t3 = BashOperator(
        task_id='notifier',
        bash_command='printf "Completed {{ execution_date.strftime("%d-%m-%Y") }}"',
        dag=dag,
    )

    fetch_gh >> load_data() >> t3
