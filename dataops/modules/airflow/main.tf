


resource "helm_release" "airflow" {
  name       = var.name
  repository = var.repository
  chart      = var.chart
  version    = var.semver
  namespace  = var.namespace
  timeout    = var.timeout
  wait       = false

  values = [
    "${file("${path.module}/values.yaml")}"
  ]

}


