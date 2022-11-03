# Issues Tracker OSS project


### Data engineer oss project

![](assets/issues_tracker_oss.jpg)

![](assets/issues-tracker-2022-10-14T15-03-36.448Z.jpg)

### Tech

- apache kafka
- ClickHouse
- Superset
- python
- airflow
- k8s


### Resource 

- [https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#howto-operator-kubernetespodoperator](https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#howto-operator-kubernetespodoperator)
- [https://splunktool.com/failed-to-extract-xcom-from-airflow-pod-kubernetes-pod-operator](https://splunktool.com/failed-to-extract-xcom-from-airflow-pod-kubernetes-pod-operator)

> Tips

```bash
python3 -c "namespace='<my-namespace>';import atexit,subprocess,json,requests,sys;proxy_process = subprocess.Popen(['kubectl', 'proxy']);atexit.register(proxy_process.kill);p = subprocess.Popen(['kubectl', 'get', 'namespace', namespace, '-o', 'json'], stdout=subprocess.PIPE);p.wait();data = json.load(p.stdout);data['spec']['finalizers'] = [];requests.put('http://127.0.0.1:8001/api/v1/namespaces/{}/finalize'.format(namespace), json=data).raise_for_status()"

```
