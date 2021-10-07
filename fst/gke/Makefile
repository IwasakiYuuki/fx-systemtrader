GCS_BUCKET_NAME=fx-systemtrader-dev-certifications
GCS_OBJECT_NAME=mlflow-db-secret.yaml
GCS_URL=gs://$(GCS_BUCKET_NAME)/$(GCS_OBJECT_NAME)
ARGO_INSTALL_URL=https://github.com/argoproj/argo-workflows/releases/download/v3.1.13/install.yaml

check:
	@echo "Nothing to do"

build:
	@echo "Nothing to do"

push:
	@echo "Nothing to do"

clean:
	if [ -f "mlflow-db-secret.yaml" ]; then \
		rm mlflow-db-secret.yaml \
	fi

get-credentials:
	gcloud container clusters get-credentials $(CLUSTER_NAME) \
		--zone $(CLUSTER_ZONE) \
		--project $(PROJECT_ID)

install: mlflow-db-secret.yaml
	# MLFlowのデプロイ
	kubectl apply -f mlflow-db-secret.yaml
	kubectl apply -f mlflow-backend-db.yaml	
	kubectl apply -f mlflow-server.yaml

	# Argoのデプロイ
	kubectl create ns argo --dry-run=client -o yaml | kubectl apply -f -
	kubectl apply -n argo -f $(ARGO_INSTALL_URL)
	kubectl create clusterrolebinding 2445yuuki-cluster-admin-binding --clusterrole=cluster-admin --user=2445yuuki@gmail.com --dry-run=client -o yaml | kubectl apply -f -

uninstall: mlflow-db-secret.yaml
	# MLFlowの削除
	kubectl delete -f mlflow-db-secret.yaml
	kubectl delete -f mlflow-backend-db.yaml	
	kubectl delete -f mlflow-server.yaml

	# Argoの削除
	kubectl delete clusterrolebinding 2445yuuki-cluster-admin-binding
	kubectl delete -n argo -f $(ARGO_INSTALL_URL)
	kubectl delete ns argo

mlflow-db-secret.yaml:
	gsutil cp $(GCS_URL) . 

.PHONY: check build push clean install 
