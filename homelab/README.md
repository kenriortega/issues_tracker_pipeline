# Deployments on k8s


> Create all resources

```shell
cd kustomize  
kubectl kustomize --enable-helm | kubectl apply -f -
```

> Delete all resources


```shell
cd kustomize  
kubectl kustomize --enable-helm | kubectl delete -f -
```