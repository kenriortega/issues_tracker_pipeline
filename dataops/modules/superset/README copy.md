# superset


```bash

helm upgrade --install --values dataops/superset/values.yaml superset superset/superset --namespace playground --create-namespace
```


```bash

helm delete superset --purge --namespace playground
```

```bash


kubectl patch svc superset-tf-release \
-p '{"spec":{"ports":[{"port":8088,"targetPort":8088,"name":"https"}],"type":"NodePort"}}' -n playground
```