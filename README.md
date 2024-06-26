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
10. At the menu on the left, click on "Access Keys" and click on "Create New Access Key":
![image](https://github.com/memaldi/kubernetes-examples/assets/1871269/49bcdb21-7208-478b-8099-6114e68ed581)
11. Set an expiration date ("Expiry") from the future and copy the "Access Key" and "Secret Key". **Warning**: once you create the Access Key, you won't be able to check the value of the "Secret Key" again.:
![image](https://github.com/memaldi/kubernetes-examples/assets/1871269/f1afb8b5-5faf-4064-b201-35004c5bc39f)
12. Close the pop-up shown when creating the access key or download the JSON with the values if you haven't copied the Access Key and the Secret Key in the previous step.
13. Click on the access key created in the previous step to add the appropriate policy to allow total access to the bucket `my-bucket` for this access key. Copy the following on the "Access Key Policy" field and click on "Update":
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::my-bucket",
                "arn:aws:s3:::my-bucket/*"
            ]
        }
    ]
}
```
![image](https://github.com/memaldi/kubernetes-examples/assets/1871269/7a4de9a9-0143-446e-9fe0-62e997a00630)

## Launch Spark

1. Build the Docker image to include the wordcount.py file. You must recover the URL of the registry given previously. You can get the URL of the registry executing `minikube --namespace registry service registry-service --url`. Notice that you must remove the schema (`http://`):
```
$ docker build -t 192.168.49.2:30920/tgvd/spark-wordcount:v1 .
```
2. Push the image to the repository:
```
$ docker push 192.168.49.2:30920/tgvd/spark-wordcount:v1
```
3. Create the service account `spark` to allow our driver to create the executors:
```
$ kubectl create serviceaccount spark
$ kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default
```
4. Get the URL of the kubernetes local proxy:
```
$ kubectl cluster-info
```
You wil get:
```
Kubernetes control plane is running at https://192.168.49.2:8443
```
5. Launch Spark job. Notice that you must replace the values at `--master`, `--conf spark.kubernetes.container.image=`, `--conf spark.hadoop.fs.s3a.access.key=` and `--conf spark.hadoop.fs.s3a.secret.key=` with your own ones:
```
$ spark-submit --master k8s://https://192.168.49.2:8443 \
    --deploy-mode cluster \
    --conf spark.executor.instances=2 \
    --conf spark.kubernetes.container.image=192.168.49.2:30920/tgvd/spark-wordcount:v1 \
    --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/opt/spark/work-dir/ -Divy.home=/opt/spark/work-dir/" \
    --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
    --conf spark.hadoop.fs.s3a.endpoint=http://minio.minio.svc.cluster.local:9000 \
    --conf spark.hadoop.fs.s3a.access.key=YOUR-ACCESS-KEY \
    --conf spark.hadoop.fs.s3a.secret.key=YOUR-SECRET-KEY \
    --conf spark.hadoop.fs.s3a.path.style.access=true \
    --packages org.apache.hadoop:hadoop-aws:3.3.4 \
    local:///opt/spark/work-dir/wordcount.py
```
6. You can check the pods created by spark executing `kubectl get all`.
7. If you want to check the logs from an specific pod, you can execute `kubectl logs -f <name-of-the-pod>`
