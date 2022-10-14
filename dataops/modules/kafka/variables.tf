variable "namespace" {
  type    = string
  default = "playground"
}

variable "name" {
  type    = string
  default = "kafka-tf-release"
}

variable "repository" {
  type    = string
  default = "https://charts.bitnami.com/bitnami"
}

variable "chart" {
  type    = string
  default = "kafka"
}

variable "semver" {
  type    = string
  default = "19.0.0"
}

variable "timeout" {
  default = 400
}
