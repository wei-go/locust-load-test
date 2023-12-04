from locust import HttpUser, task, constant


class MyUser(HttpUser):
    wait_time = constant(1)
    host = "https://api.github.com/"

    @task
    def get_octocat_api(self):
        self.client.get("octocat", name="get_octocat_api")
