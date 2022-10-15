module "airflow" {
  source    = "./modules/airflow"
  namespace = "data-processing"
}
module "kafka" {
  source    = "./modules/kafka"
  namespace = "data-ingestion"
}
module "ch" {
  source    = "./modules/ch"
  namespace = "data-serving"
}
module "superset" {
  source    = "./modules/superset"
  namespace = "data-viz"
}