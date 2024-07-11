# Instructional Steps
## Part 1 : Containerization with Docker

### 1.1 Writing Dockerfile to containerize a sample application.
1. Make a file to run the application (~/DockerK8s/Mini_Exercise/dock/manage.py)
2. Make a Docker file containing necessary dependencies and configurations (~/DockerK8s/Mini_Exercise/dockerfile)
3. Make a requirement file containing required Python libraries to be installed with "pip" for application to run (~/DockerK8s/Mini_Exercise/requirements.txt)

### 1.2 Building Docker image
1. Run the following Docker command "docker build -t django-app ."
2. To check that Docker has successfully generated the image, run "docker image ls"
3. To map the internal Docker port 5000 to local machine's Port 8000, run "docker run -d -p 8000:8000 django-app"

### 1.3 Test run Docker image
1. Run the following Docker command "docker run django-app"
2. In Web Browser, enter the local IP address "127.0.0.1:8000"


## Part 2 : Pushing to Docker Hub

### 2.1 & 2.2 Making account & Login in
1. Make account on Docker
2. Run following Docker command "docker login"
3. Enter Docker Hub credentials for username & password from step 1.

### 2.3 Tagging Docker image
1. Run the following Docker command "docker image tag django-app akrecy/django-app", where "akrecy" is the Docker Hub user ID
2. Verify image tag was successful by running "docker image ls"

### 2.4 Pushing Docker image to Docker Hub
1. Run the following command "docker push akrecy/django-app, where "akrecy" is the Docker Hub user ID
2. To verify successful push, at docker hub web-page, click "Repositories" to view images pushed.


## Part 3 : Setting up Kubernetes

### 3.1 Configuring Kubernetes
1. To verify Kubernetes is running in local environment, run the following command "kubectl get nodes"

### 3.2 Setting up Master & Worker nodes
1. Download Kind to build a multi-node Kubernetes cluster setup by running the following commands : 
	- curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
	- chmod +x ./kind
	- sudo mv ./kind /usr/local/bin/kind
2. Create a kind-config.yml file for specifying nodes : 1 master, 2 workers ((~/DockerK8s/Mini_Exercise/kind-config.yml)
3. Create a cluster with the kind-config.yml file by running "kind create cluster --name my-cluster --config kind-config.yml"
4. Due to configuration errors, we copied and paste the kubeconfig file into our working directory instead of home and then specify our kubectl to this copied file
	- export KUBECONFIG=$(pwd)/kubeconfig.yml
	- kubectl config use-context kind-my-cluster
5. Check nodes by running "kubectl get nodes" (It will shows my-cluster-control-plane, my-cluster-worker, my-cluster-worker2)


## Part 4 : Deploying the Application

### 4.1 Creating Kubernetes deployment YAML file to deploy application
2. Create a YAML file (deployment.yml)

### 4.2 Configure 3 replicas
1. Edit the YAML file to specify 3 replicas

### 4.3
1. Edit the YAML file to specify image (image: akrecy/django-app)

### 4.4 Applying the deployment YAML file to Kubernetes cluster
1. Run the following Kubernetes command "kubectl apply -f deployment.yml"
2. Check if deployment is running by running the following command "kubectl get deployments"


## Part 5 : Persistent Volume Configuration

### 5.1 Set up a Persistent Volume
1. Create YAML file for Persistent Volume (pv.yml)
2. Apply the file by running "kubectl apply -f pv.yml"
3. Verify creation by running "kubectl get pv"

### 5.2 Create a Persistent Volume Claim to claim the PV
1. Create YAML file for Persistent Volume Claim (pvc.yml)
2. Apply the file by running "kubectl apply -f pvc.yml"
3. Verify creation by running "kubectl get pvc" (PVC is still in pending state because there is no deployment & pods yet)

### 5.3 Mount the PV to container within the Deployment YAML file
1. Modify the Deployment YAML to use the PVC
2. Apply this deployment.yml file so that the PVC can be bound

### 5.4 Log file 
1. Edit the deployment.yml file by adding "initContainer" 

### 5.5 Deleting Deployment and Recreating
1. To delete Deployment, run the following code "kubectl delete deployment deployment-1", where deployment-name is defined in deployment.yml file
2. To create a new deployment, run the following command "kubectl apply -f deployment.yml"

### 5.6 Test the container to verify log file is still present in mount path
1. To identify the pod, run "kubectl get pods"
2. To access the pod, run "kubectl exec -it deployment-1-597d468ddd-dlpwj -- /bin/bash", where deployment-1-597d468ddd-dlpwj is the identified pod name in step 1.
3. To verify log file, run "ls /django-app/logs" & there should be an output "app.log" as specified in deployment.yml


## Part 6 : Expose the Deployment as a Service

### 6.1 Expose deployment as a service of type ClusterIP
1. Create a YAML file for service (service.yml) and then apply it by running "kubectl apply -f service.yml"
2. OR simply run the following command "kubectl expose deployment deployment-1 --type=ClusterIP --port=8000 --target-port=8000" 
3. Run "kubectl get services" to verify service has been created


### 6.2 Create a test pod to access service to validate
1. Create YAML file for test pod (servicepod.yml)
2. Apply by running "kubectl apply -f servicepod.yml"
3. Access the test pod by running "kubectl exec -it service-pod -- /bin/bash", where service-pod is the name defined in servicepod.yml
4. Test the service by running "curl http://my-flask-app:8000"
5. After testing, cleanup by deleting the test pod. Run "kubectl delete pod test-pod"

1. Expose the deployment by running "kubectl expose deployment deployment-1 –-type=ClusterIP –-port=8000
2. Make a service-pod.yml file and apply it by running "kubectl apply -f service-pod.yml"
3. Port Forward by running "kubectl port-forward service-pod-1 8000:8000", where service-pod-1 is the pod name defined in service-pod.yml
4. Test connectivity using curl by running "curl http://localhost:8000/rps/"
