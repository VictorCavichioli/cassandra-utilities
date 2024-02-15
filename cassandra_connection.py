from cassandra.cluster import Cluster
from tests.conftest import get_container_ips_by_name
DEFAULT_KEYSPACE = "shoppingcart"

CCM_IP_LIST = ["127.0.0.1", "127.0.0.2", "127.0.0.4", "127.0.0.3"]
DOCKER_SEED_NAMES = ['cassandra-image_cassandra-seed-dc3-rack1-node1_1','cassandra-image_cassandra-seed-dc1-rack1-node1_1','cassandra-image_cassandra-seed-dc2-rack1-node1_1']  # Lista de nomes dos containers

class CassandraConnection:
    def __init__(
        self,
        keyspace=DEFAULT_KEYSPACE,
        file="cassandra-image/schema.cql",
        execute_file=False,
    ):
        docker_ip_list = get_container_ips_by_name(DOCKER_SEED_NAMES)
        self.cluster = Cluster(docker_ip_list)
        if len(file) > 1 and execute_file == True:
            self.session = self.cluster.connect()
            self.execute_cql_from_file(file)
            self.session.shutdown()
        self.session = self.cluster.connect(keyspace)

    def execute_cql_from_file(self, file):
        with open(file, mode="r") as f:
            txt = f.read()
            stmts = txt.split(r";")
            for i in stmts:
                stmt = i.strip()
                if stmt != "":
                    print('Executing "' + stmt + '"')
                    self.session.execute(stmt)

    def execute_cql_query(self, query):
        self.session.execute(query=query)
