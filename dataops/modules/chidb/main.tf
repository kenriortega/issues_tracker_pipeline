
resource "kubernetes_manifest" "chi_db_tf" {
  manifest = {
    "apiVersion" = "clickhouse.altinity.com/v1"
    "kind"       = "ClickHouseInstallation"
    "metadata" = {
      "name"      = var.name
      "namespace" = var.namespace
    }
    "spec" = {
      "configuration" = {
        "clusters" = [
          {
            "layout" = {
              "replicasCount" = 1
              "shardsCount"   = 1
            }
            "name" = "db-01"
          },
        ]
      }
      "templates" = {
        "volumeClaimTemplates" = [
          {
            "name" = "default-volume-claim"
            "spec" = {
              "accessModes" = [
                "ReadWriteOnce",
              ]
              "resources" = {
                "requests" = {
                  "storage" = "5Gi"
                }
              }
            }
          },
        ]
      }
    }
  }

}
