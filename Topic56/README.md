---
title: "Kubernetes"
topic: "kubernetes"
tags: [kubernetes, containers, kubectl, pods, services, cloud, pentesting]
difficulty: advanced
day: 56
layout: default
parent: Topics
nav_order: 56
---

# Kubernetes

## What You Will Learn
- How Kubernetes organizes and manages containers
- What pods, services, namespaces, and nodes are
- How to enumerate a Kubernetes cluster as an attacker
- How to escape containers via the containerd socket

## What Is It?

**Kubernetes (K8s)** is an open-source container orchestration platform. It automates the deployment, scaling, and management of containerized applications. Large-scale cloud deployments almost always use Kubernetes.

From a security perspective, Kubernetes introduces unique attack surfaces: misconfigured RBAC, exposed dashboards, overly permissive service accounts, and accessible container runtimes.

## Why It Matters

Kubernetes is standard in enterprise environments. Gaining access to a Kubernetes cluster can mean access to dozens or hundreds of services, databases, and internal APIs.

## Terminology

| Term | Description |
|------|-------------|
| **Node** | A physical or virtual machine with actual resources (CPU, RAM) |
| **Cluster** | A group of nodes — one master and any number of workers |
| **Pod** | One or more containers that share storage and network |
| **Namespace** | Logical isolation for resources — keeps secrets separate between services |
| **Service** | A way to expose an application running on pods as a network service |

### Types of Kubernetes Services

| Type | Description |
|------|-------------|
| **ClusterIP** | Only reachable within the cluster |
| **LoadBalancer** | Single entry point from outside the cluster |
| **NodePort** | Exposes a port on the cluster to outside services |
| **ExternalName** | Maps a service to a DNS name |

## kubectl Commands

```bash
# Get all pods in all namespaces
kubectl get pods --all-namespaces
kubectl get pods -n <namespace>

# Get all services
kubectl get svc -n <namespace>

# Get all deployments
kubectl get deployments -n <namespace>

# Describe a pod (shows volumes, environment variables)
kubectl describe pod <pod-name> -n <namespace>

# Execute a command in a running pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/sh

# View pod logs
kubectl logs <pod-name> -n <namespace>

# Get all secrets (if you have permission)
kubectl get secrets -n <namespace>
kubectl get secret <name> -n <namespace> -o jsonpath='{.data}' | base64 -d
```

## Pentesting Kubernetes

### Enumerate from Inside a Pod

When you land in a container, check if it has elevated access to the Kubernetes API:

```bash
# Service account token is automatically mounted
cat /var/run/secrets/kubernetes.io/serviceaccount/token

# Kubernetes API address
env | grep KUBERNETES

# Query the API using the service account token
TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
curl -k https://kubernetes.default.svc/api/v1/namespaces \
     -H "Authorization: Bearer $TOKEN"

# List secrets (if allowed)
curl -k https://kubernetes.default.svc/api/v1/namespaces/default/secrets \
     -H "Authorization: Bearer $TOKEN"
```

### containerd.sock — Container Escape

`containerd.sock` (often at `/run/containerd/containerd.sock`) is where clients connect to the containerd runtime. If this socket is mounted inside a container, you can use it to escape.

Docker uses it to tell containerd to run containers. Kubernetes uses it via the CRI plugin.

```bash
# Check if socket is mounted
ls -la /var/run/containerd/containerd.sock
ls -la /var/run/docker.sock

# Use crictl to interact with containerd
crictl -r unix:///run/containerd/containerd.sock images
crictl -r unix:///run/containerd/containerd.sock ps
```

### Kubernetes Dashboard

An exposed Kubernetes dashboard can allow full cluster control if RBAC is not configured:

```bash
# Access dashboard proxy
kubectl proxy
# Then browse: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

## Resources

- [Kubernetes Goat — Vulnerable Kubernetes](https://madhuakula.com/kubernetes-goat/)
- [HackTricks — Kubernetes Pentesting](https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security)
- [TryHackMe — Kubernetes for Beginners](https://tryhackme.com/room/kubernetesforbeginnersthm)
- [Attacking Kubernetes — CNCF Security Whitepaper](https://github.com/cncf/tag-security)
