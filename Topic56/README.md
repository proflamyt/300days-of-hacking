# Kubernetes

## Terminology

- Nodes: This are virtual or physical machine with actual resources, like CPU and RAM.

- Kubernetes cluster: group of nodes either physical or virtual machines that contain one master node and any number of worker nodes.

- Pods:  one or more containers that share storage and network resources.

- Namespace : gives privacy to resources. keeping their secrets secluded from other servi

- Services : A way to expose an application running on a set of pods as a network service.

  


Types Of Kubernetes Services:
- ClusterIP : service is only reachable within the cluster, pods within the cluster can use this as an IP for communication
  
- LoadBalancer : A single point of entry outside the cluster

- NodePort : Expose the port within the cluster to outside service

- ExternalName : maps a service to a domain name

## Kubectl 

Get all pods within a  namespace

```bash
kubectl get pods -n <namespace>
```

Get all services within a  namespace

```bash
kubectl get svc -n <namespace>
```

## What is containerd.sock specifically?

This file (often located at /run/containerd/containerd.sock) is where clients connect to containerd.

For example:

- Docker uses it to tell containerd: “Hey, pull this image” or “Run this container.”

- Kubernetes (via CRI plugin) uses it to manage pods.




### Video

https://madhuakula.com/kubernetes-goat/docs/learning-kubernetes
