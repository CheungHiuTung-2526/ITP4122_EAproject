#!/bin/bash

set -e

echo ""
echo "[1/4] Building and pushing Docker image..."
gcloud builds submit --tag asia-east1-docker.pkg.dev/itp4122project/itp4122-repo/flask-app:latest .

echo ""
echo "[2/4] Applying Kubernetes manifests..."
kubectl apply -f configmap.yaml
kubectl apply -f filestore-storageclass.yaml
kubectl apply -f filestore-pvc.yaml
kubectl apply -f deployment.yaml

echo ""
echo "[3/4] Waiting for Filestore PVC to be Bound..."
kubectl wait --for=condition=bound pvc/itp4122-filestore-pvc --timeout=120s || echo "⚠️ PVC may still be provisioning..."

echo ""
echo "[4/4] Waiting for deployment rollout..."
kubectl rollout status deployment/flask-app --timeout=300s

echo ""
echo "========================================"
echo "Deployment completed successfully!"
echo "========================================"
echo ""
echo "Check your service:"
kubectl get service flask-service
