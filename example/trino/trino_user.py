import time
from locust import User
from pyhive import trino


class TrinoUser(User):
    abstract = True
    server = None
    krb5_config_path = None
    krb5_keytab_path = None
    trino_user = None
    krb5_principal = None
    namespace = None

    def __init__(self, environment):
        super().__init__(environment)
        self.client: TrinoClient = TrinoClient(
            user=self,
            host=self.server,
            port=443,
            trino_user=self.trino_user,
            catalog="hive",
            schema=self.namespace,
            krb5_config_path=self.krb5_config_path,
            krb5_keytab_path=self.krb5_keytab_path,
            krb5_principal=self.krb5_principal)


class TrinoClient:
    user: TrinoUser = None

    def __init__(self, *, user, host, port, trino_user, catalog, schema,
                 krb5_config_path=None, krb5_keytab_path=None, krb5_principal=None):
        import os

        self.user = user
        cmd = f"kinit -kt {krb5_keytab_path} {krb5_principal}"
        os.popen(cmd).read()
        self.cur = trino.connect(
            host,
            port=port,
            username=trino_user,
            principal_username=trino_user,
            catalog=catalog,
            poll_interval=10,
            source="pyhive",
            protocol="https",
            schema=schema,
            KerberosRemoteServiceName="trino",
            KerberosPrincipal=krb5_principal,
            KerberosConfigPath=krb5_config_path,
            KerberosKeytabPath=krb5_keytab_path,
            KerberosUseCanonicalHostname="false",
        ).cursor()

    def execute(self, query, name="unnamed"):
        start_time = time.time()
        start_perf_counter = time.perf_counter()
        request_type = "QUERY"
        results = None
        try:
            self.cur.execute(query)
            results = self.cur.fetchall()

            self.user.environment.events.request.fire(
                request_type=request_type,
                name=name,
                start_time=start_time,
                response_time=(time.perf_counter() - start_perf_counter) * 1000,
                response_length=0,
                context={**self.user.context()},
                url=query,
                exception=None,
            )
        except Exception as e:
            self.user.environment.events.request.fire(
                request_type=request_type,
                name=name,
                start_time=start_time,
                response_time=(time.perf_counter() - start_perf_counter) * 1000,
                response_length=0,
                context={**self.user.context()},
                url=query,
                exception=e,
            )

        return results
