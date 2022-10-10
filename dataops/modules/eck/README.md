# ECK


1- create namespace

```bash
kubectl apply -f namespace.yaml
```

2- instalar el operador

```bash

kubectl create -f crds.yaml

kubectl apply -f operator.yaml -n elk

```

3- install elasticsearch view [https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-managing-compute-resources.html](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-managing-compute-resources.html)


```bash
kubectl apply -f elastic.yaml
kubectl apply -f kibana.yaml
kubectl apply -f beats-k8s-metric.yaml

```

```bash

kubectl patch svc elk-demo-es-http \
-p '{"spec":{"ports":[{"port":9200,"targetPort":9200,"name":"https"}],"type":"LoadBalancer"}}'
```

```bash

kubectl patch svc elk-demo-es-http \
-p '{"spec":{"ports":[{"port":9200,"targetPort":9200,"name":"https"}],"type":"NodePort"}}'
```

```bash
export PASSWORD=$(kubectl get secret elk-demo-es-elastic-user -o go-template='{{.data.elastic | base64decode}}')
```
```bash
kubectl get secret elk-demo-es-elastic-user -o=jsonpath='{.data.elastic}' -n elk-home | base64 --decode; echo
```
```bash

curl -u "elastic:$PASSWORD" -k "https:xxx.lb:9200"
```