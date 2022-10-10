

# Creating namespace with the Kubernetes provider is better than auto-creation in the helm_release.
# You can reuse the namespace and customize it with quotas and labels.
resource "kubernetes_namespace" "playground" {
  metadata {
    name = var.namespace
  }
}

resource "kubernetes_namespace" "data_serving" {
  metadata {
    name = "data-serving"
  }
}

resource "kubernetes_namespace" "data_ingestion" {
  metadata {
    name = "data-ingestion"
  }
}
resource "kubernetes_namespace" "data_processing" {
  metadata {
    name = "data-processing"
  }
}


resource "kubernetes_namespace" "data_viz" {
  metadata {
    name = "data-viz"
  }
}


module "airflow" {
  source    = "./modules/airflow"
  namespace = data_processing.metadata.name
}

module "kafka" {
  source    = "./modules/kafka"
  namespace = data_ingestion.metadata.name

}


module "ch" {
  source    = "./modules/ch"
  namespace = data_serving.metadata.name

}



module "superset" {
  source    = "./modules/superset"
  namespace = data_viz.metadata.name
}
