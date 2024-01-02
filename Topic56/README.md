# Kubernetes

## Terminology

- Nodes: This are virtual or physical machine with actual resources, like CPU and RAM.

- Kubernetes cluster: group of nodes either physical or virtual machines that contain one master node and any number of worker nodes.

- Pods:  one or more containers that share storage and network resources.

- Namespace : 

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
