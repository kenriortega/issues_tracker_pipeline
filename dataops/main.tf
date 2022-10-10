

# Creating namespace with the Kubernetes provider is better than auto-creation in the helm_release.
# You can reuse the namespace and customize it with quotas and labels.
resource "kubernetes_namespace" "playground" {
  metadata {
    name = var.namespace
  }
}


module "airflow" {
  source = "./modules/airflow"
}

module "kafka" {
  source = "./modules/kafka"
}

