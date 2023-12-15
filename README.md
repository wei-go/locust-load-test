**Performance Test Tool**

Performance Test Tool is a python based project which is triggered by [Locust Load Tests Framework](https://docs.locust.io/).

[Locust Git](https://github.com/locustio/locust)

---

## Running on local with config

It's easy to run the performance test on local with config.
Prepare your test case file under the ```tests``` folder, and modify the ```master.conf``` file to set the test case file name.

Steps:

1. setup the python environment
```pip install -r requirements.txt```

2. prepare the test case file under the ```tests``` folder
ex: ```tests/locust_testfile.py```

3. modify the
```master.conf```
```
locustfile = tests/{TEST_CASE_FILE_NAME}.py
host = ""
users = {MAX_NUM_OF_USERS}
spawn-rate = {SPAWN_RATE}
run-time = 10m # set the run time
headless = true # if you want to run it without UI
```

4. execute the command to run the performance test
```locust -f master.conf```

---

## Dsitributed Performance Test on Kubernetes

* We use [Helm](https://helm.sh/docs/intro/install/) to do deployment, so please check you have it. *

Pre-Actions:

1. Build the docker image and push to the GCR

For Grafana:
```cd {REPO_ROOT}/build/grafana```
```docker build -t {PATH_OF_DOCKER_NAME}:{TAG} .```
```docker push {PATH_OF_DOCKER_NAME}:{TAG}```
For TimescaleDB:
```cd {REPO_ROOT}/build/timescaledb```
```docker build -t {PATH_OF_DOCKER_NAME}:{TAG} .```
```docker push {PATH_OF_DOCKER_NAME}:{TAG}```
For Locust:
```cd {REPO_ROOT}/```
```docker build -t {PATH_OF_DOCKER_NAME}:{TAG} .```
```docker push {PATH_OF_DOCKER_NAME}:{TAG}```

2. Push the test file to Git Repo

3. Modify the ```helm/values.yml``` file to set the image path, test file, repo...etc

Steps:

1. Go to kubernetes cluster and assign the namespace
```kubectl config set-context --current --namespace={NAMESPACE}```

2. install the helm chart
```helm install {RELEASE_NAME} helm/```

3. Wait for the pods are ready, then forward the port to your local to access locust UI
```kubectl port-forward service/locust-service 8000:80```

```if you want to establish a public link to access the locust UI, you can use the following command to get the public IP and setup ingress```

4. open the ```http://localhost:8000/``` on your browser then you should see the locust page with workers

All set. Enjoy it!

---
