# TODO: all manifests overengineered? Check it

kubectl apply -f db-statefulset.yaml
# TODO: really stateful?
kubectl apply -f db-service.yaml

# TODO: what if db not ready yet?
# Develop reconnect in app
kubectl apply -f web-deployment.yaml
kubectl apply -f web-service.yaml

# TODO: check command for migration
#kubectl exec web -- manage.py migrate
