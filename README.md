# Kubernetes-examples

In this repository, instructions for running the Kubernetes examples shown at Big Data Processing subject can be found.

## Minikube installation

1. Edit /etc/docker/daemon.json (`sudo nano /etc/docker/daemon.json`) file and add the following content:
```
{
    "insecure-registries" : [ "0.0.0.0/0" ]
}
```
2. Install minikube:
```
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
$ sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```
3. Deploy minikube cluster:
```
minikube start --insecure-registry "0.0.0.0/0" --nodes 2 --memory 4g --cpus 3
```
4. Install kubectl:
```
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
$ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```
