variable "namespace" {
  type    = string
  default = "playground"
}

variable "name" {
  type    = string
  default = "superset-tf-release"
}

variable "repository" {
  type    = string
  default = "https://apache.github.io/superset"
}

variable "chart" {
  type    = string
  default = "superset"
}

variable "semver" {
  type    = string
  default = "0.7.4"
}

variable "timeout" {
  default = 400
}
