from locust import task, constant, run_single_user
from trino.trino_user import TrinoUser
import os


class CustomTrinoUser(TrinoUser):
    from dotenv import load_dotenv
    wait_time = constant(1)
    load_dotenv()

    server = os.getenv("TRINO_SERVER")
    krb5_config_path = os.getenv("TRINO_CONFIG_PATH")
    krb5_keytab_path = os.getenv("TRINO_KT_PATH")
    trino_user = os.getenv("TRINO_USER")
    krb5_principal = os.getenv("TRINO_KRB5_PRINCIPAL")
    namespace = os.getenv("TRINO_NS")

    @task
    def show_tables(self):
        self.client.execute("show tables", name="show_tables")


if __name__ == "__main__":
    run_single_user(CustomTrinoUser)
