variable "namespace" {
  type    = string
  default = "playground"
}

variable "name" {
  type    = string
  default = "airflow-tf-release"
}

variable "repository" {
  type    = string
  default = "https://airflow.apache.org"
}

variable "chart" {
  type    = string
  default = "airflow"
}

variable "semver" {
  type    = string
  default = "1.6.0"
}

variable "timeout" {
  default = 400
}
