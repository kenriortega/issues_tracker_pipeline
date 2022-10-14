resource "helm_release" "elastic-operator" {
  name       = var.name
  repository = var.repository
  chart      = var.chart
  version    = var.semver
  namespace  = var.namespace
  timeout    = var.timeout
  wait       = false
}


resource "kubernetes_manifest" "elasticsearch" {
  manifest = yamldecode(<<-EOF
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elastic-tf
  namespace: ${var.namespace}
spec:
  version: 8.3.3
  nodeSets:
    - name: default
      count: 1
      config:
        node.store.allow_mmap: false
  EOF
  )
}


resource "kubernetes_manifest" "kibana" {
  manifest = yamldecode(<<-EOF
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-tf
  namespace: ${var.namespace}
spec:
  version: 8.3.3
  count: 1
  elasticsearchRef:
    name: elastic-tf
  EOF
  )
}
