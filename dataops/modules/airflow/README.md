# airflow


 create a  kind cluster

 ```bash
 kind create cluster --image kindest/node:v1.21.1
 ```

Confirm installation
```bash
 kubectl cluster-info --context kind-kind
 ```

Add Airflow Helm Stable Repo

```bash

helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

Install the chart

```bash
helm install private-airflow-dev apache-airflow/airflow --namespace airflow-dev
```

```bash
kubectl port-forward svc/$RELEASE_NAME-webserver 8080:8080 --namespace $NAMESPACE
```
Mounting DAGs from a private Github repo using Git-Sync sidecar

Then create your ssh keys:

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Add the public key to your private repo (under Settings > Deploy keys).

You have to convert the private ssh key to a base64 string. You can convert the private ssh key file like so:
```bash
base64 <my-private-ssh-key> -w 0 > temp.txt
```
Then copy the string from the temp.txt file. You’ll add it to your override-values.yaml next.
In this example, you will create a yaml file called override-values.yaml to override values in the values.yaml file, instead of using --set:

```yaml
dags:
  gitSync:
    enabled: true
    repo: ssh://git@github.com/<username>/<private-repo-name>.git
    branch: <branch-name>
    subPath: ""
    sshKeySecret: airflow-ssh-secret
extraSecrets:
  airflow-ssh-secret:
    data: |
      gitSshKey: '<base64-converted-ssh-private-key>'
```

Don’t forget to copy in your private key base64 string.

Finally, from the context of your Airflow Helm chart directory, you can install Airflow:

```bash
helm upgrade --install private-airflow-dev apache-airflow/airflow -f values.yaml --namespace airflow-dev
```

If you have done everything correctly, Git-Sync will pick up the changes you make to the DAGs in your private Github repo
You should take this a step further and set dags.gitSync.knownHosts so you are not susceptible to man-in-the-middle attacks. This process is documented in the production guide.


```bash

kubectl  -n data-processing patch svc airflow-tf-release-webserver \
-p '{"spec":{"ports":[{"port":8080,"targetPort":8080,"name":"https"}],"type":"NodePort"}}'
```


```bash

kubectl -n playground patch svc airflow-tf-release-webserver \
-p '{"spec":{"ports":[{"port":8080,"targetPort":8080,"name":"https"}],"type":"NodePort"}}'
```