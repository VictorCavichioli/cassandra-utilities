FROM cassandra:4.0

# Copie o script CQL para o diretório do contêiner
COPY schema.cql /docker-entrypoint-initdb.d/

# Defina as variáveis de ambiente, se necessário
ENV CASSANDRA_HOME /usr/share/cassandra
ENV CASSANDRA_CONF /etc/cassandra
ENV LOCAL_JMX no
ENV JVM_EXTRA_OPTS "-Dcassandra.jmx.local.port=7199 -Dcom.sun.management.jmxremote.rmi.port=7199 -Dcom.sun.management.jmxremote=true -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -Djava.rmi.server.hostname=127.0.0.1"

# Execute o script de inicialização padrão do Cassandra
CMD ["cassandra"]
