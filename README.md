# Kubernetes-examples

In this repository, instructions for running the Kubernetes examples shown at Big Data Processing subject can be found.

## Minikube installation

1. Edit /etc/docker/daemon.json (`sudo nano /etc/docker/daemon.json`) file and add the following content:
```
{
    "insecure-registries" : [ "0.0.0.0/0" ]
}
```
2. Restart docker:
```
$ sudo systemctl restart docker
```
3. Install minikube:
```
$ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
$ sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```
4. Deploy minikube cluster:
```
minikube start --insecure-registry "0.0.0.0/0" --nodes 2 --memory 4g --cpus 3
```
5. Install kubectl:
```
$ curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
$ sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```
6. Check the minikube deployment:
```
$ kubectl get nodes
```

## NGINX example

1. From the directory in which you have this repository cloned, deploy the service:

```
$ kubectl apply -f nginx-deployment-service.yml
```

2. Expose the service:

```
$ minikube service nginx-service --url
```
3. Open the URL obtained in the previous step in a web browser.
4. Execute the following to get the names of the Pods:
```
$ kubectl get pods
```
5. To check the logs of different pods, execute (CTRL+C to exit):
```
$ kubectl logs -f <name-of-the-pod>
```
6. To delete the deployment:
```
$ kubectl delete deployment/nginx-deployment
```

## Spark example

Those steps are executed from the `spark` directory.

### Docker registry

1. Create `registry` namespace:
```
$ kubectl create namespace registry
```
2.  Deploy the registry:
```
$ kubectl --namespace registry apply -f registry/
```
3. Wait until the deployment is ready:
```
$ kubectl --namespace registry get deployments
```
4. Expose the registry. This URL will be used later:
```
minikube --namespace registry service registry-service --url
```

### MinIO

1. Create `minio` namespace:
```
$ kubectl create namespace minio
```
2. Deploy MinIO:
```
$ kubectl --namespace minio apply -f minio/
```
3. Wait until the deployment is ready:
```
$ kubectl --namespace minio get deployments
```
4. Expose MinIO:
```
$ minikube --namespace minio service minio --url
```
5. Access to one of the links from the previous step and access to MinIO. The user is `minio` and the password is `miniosecret`.
6. Click on "Create bucket" and create a bucket named `my-bucket`. Let all the options as they are by default:
![image](https://github.com/memaldi/kubernetes-examples/assets/1871269/403ec032-0066-464f-8396-e8e3584a2712)
7. Select the bucket created in the previous step and, at the right-top corner, click on the folder icon ("Browse Bucket"):
![image](https://github.com/memaldi/kubernetes-examples/assets/1871269/9bb076c2-853b-4d57-bb28-b82dd43e109d)
8. Click on "Create new path" and create a folder called `input`:
![image](https://github.com/memaldi/kubernetes-examples/assets/1871269/cb5b48c6-b6ec-46b5-8174-046f64930272)
9. Drag & drop or click into "Upload" to upload the well-known `sonnets.txt` file. You can find this file at `/home/osboxes/hadoop-exercises/wordcount/input/sonnets.txt`:
![image](https://github.com/memaldi/kubernetes-examples/assets/1871269/00062cbe-14f0-4ee4-9d53-a7bffa888f11)


