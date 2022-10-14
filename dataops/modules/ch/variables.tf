variable "namespace" {
  type    = string
  default = "playground"
}

variable "name" {
  type    = string
  default = "clickhouse-tf-release"
}

variable "repository" {
  type    = string
  default = "https://charts.bitnami.com/bitnami"
}

variable "chart" {
  type    = string
  default = "clickhouse"
}

variable "semver" {
  type    = string
  default = "0.2.3"
}

variable "timeout" {
  default = 400
}
