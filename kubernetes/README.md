# Kubernetes Canary Strategy

This folder contains the Kubernetes manifests for a canary deployment strategy of `torneo-api`.

## Goal

Deploy two versions of the API:

- `stable`: image built from `main`
- `canary`: image built from `feature/canary-health-endpoint`

And split the traffic between both versions using NGINX Ingress.

## Resources included

- `namespace.yaml`: dedicated namespace
- `secret.example.yaml`: example secret with `DATABASE_URL`
- `deployment-stable.yaml`: stable pods
- `deployment-canary.yaml`: canary pods
- `service-stable.yaml`: service for stable
- `service-canary.yaml`: service for canary
- `ingress-stable.yaml`: primary ingress
- `ingress-canary.yaml`: canary ingress with 20% traffic

## Prerequisites

Install these tools:

1. Docker Desktop
2. `kubectl`
3. A Kubernetes cluster

Recommended options:

- Docker Desktop with Kubernetes enabled
- Minikube

For canary traffic with annotations, you also need an NGINX Ingress Controller.

## Images

Build and push two images, one for each branch.

### Stable image

From branch `main`:

```powershell
docker build -t docker.io/replace-me/torneo-api:stable .
docker push docker.io/replace-me/torneo-api:stable
```

### Canary image

From branch `feature/canary-health-endpoint`:

```powershell
docker build -t docker.io/replace-me/torneo-api:canary .
docker push docker.io/replace-me/torneo-api:canary
```

Then replace `docker.io/replace-me/torneo-api` in both deployment files with your real image path.

## Prepare the database secret

Copy the example file and replace the connection string with your real database:

```powershell
Copy-Item kubernetes\secret.example.yaml kubernetes\secret.yaml
```

The API needs `DATABASE_URL` to start correctly.

## Apply manifests

Run these commands from the project root:

```powershell
kubectl apply -f kubernetes\namespace.yaml
kubectl apply -f kubernetes\secret.yaml
kubectl apply -f kubernetes\deployment-stable.yaml
kubectl apply -f kubernetes\deployment-canary.yaml
kubectl apply -f kubernetes\service-stable.yaml
kubectl apply -f kubernetes\service-canary.yaml
kubectl apply -f kubernetes\ingress-stable.yaml
kubectl apply -f kubernetes\ingress-canary.yaml
```

## Check rollout

```powershell
kubectl get pods -n torneo-api
kubectl get deployments -n torneo-api
kubectl get services -n torneo-api
kubectl get ingress -n torneo-api
```

## Health checks

The stable branch currently exposes:

```json
{
  "api": "torneo-api",
  "status": "stable",
  "version": "2.1.2"
}
```

The canary branch should expose a different `status` or `version`, for example:

```json
{
  "api": "torneo-api",
  "status": "canary",
  "version": "2.2.0-canary"
}
```

This is how you confirm which version answered the request.

## How traffic is distributed

The main ingress sends traffic to the stable service.

The canary ingress uses:

- `nginx.ingress.kubernetes.io/canary: "true"`
- `nginx.ingress.kubernetes.io/canary-weight: "20"`

That means around 20% of the requests should be routed to canary.

## Test locally

If using a local cluster, add this line to your hosts file:

```text
127.0.0.1 torneo-api.local
```

Then test:

```powershell
curl http://torneo-api.local/health
```

Run it several times and check whether the response comes from stable or canary.

## Cleanup

```powershell
kubectl delete namespace torneo-api
```
