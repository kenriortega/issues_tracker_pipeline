
data "kubectl_file_documents" "crds" {
  content = file("olm/crds.yaml")
}

resource "kubectl_manifest" "crds_apply" {
  for_each          = data.kubectl_file_documents.crds.manifests
  yaml_body         = each.value
  wait              = true
  server_side_apply = true
}

data "kubectl_file_documents" "olm" {
  content = file("olm/olm.yaml")
}

resource "kubectl_manifest" "olm_apply" {
  depends_on = [data.kubectl_file_documents.crds]
  for_each   = data.kubectl_file_documents.olm.manifests
  yaml_body  = each.value
}

# Install ArgoCD

resource "helm_release" "argocd" {
  name = "argocd"

  repository       = "https://argoproj.github.io/argo-helm"
  chart            = "argo-cd"
  namespace        = "argocd"
  version          = "4.9.7"
  create_namespace = true

  values = [
    file("argocd/application.yaml")
  ]
}
