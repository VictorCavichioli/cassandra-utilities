from cassandra.cluster import Cluster

DEFAULT_KEYSPACE = "shoppingcart"


class CassandraConnection:
    def __init__(
        self,
        keyspace=DEFAULT_KEYSPACE,
        file="cassandra-image/schema.cql",
        execute_file=False,
    ):
        self.cluster = Cluster(["127.0.0.1", "127.0.0.2", "127.0.0.4", "127.0.0.3"])
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
