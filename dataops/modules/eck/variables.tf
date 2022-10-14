variable "namespace" {
  type    = string
  default = "playground"
}

variable "name" {
  type    = string
  default = "eck-operator-tf-release"
}

variable "repository" {
  type    = string
  default = "https://helm.elastic.co"
}

variable "chart" {
  type    = string
  default = "eck-operator"
}

variable "semver" {
  type    = string
  default = "2.4.0"
}

variable "timeout" {
  default = 400
}
