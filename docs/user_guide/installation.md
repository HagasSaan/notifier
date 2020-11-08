# Installation via Docker-Compose
1. Install [docker](https://docs.docker.com/get-docker/)
2. Install [docker-compose](https://docs.docker.com/compose/install/)
3. Run `docker-compose -d up` in folder with `docker-compose.yml` file


# Installation in K8s cluster
1. Set your Sentry token in `k8s/kustomization.yaml`, or remove it from `kustomization.yaml` and `web-deployment.yaml`
2. Run `kubectl apply -k k8s/kustomization.yaml`, then check pods are running

