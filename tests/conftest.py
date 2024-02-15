import pytest
import docker
import yaml
import subprocess

CONFIG_FILE = "test_config.yaml"
COMPOSE_FILE="cassandra-image/cassandracluster.yaml"

def _read_yaml_file(config_file=CONFIG_FILE):
    with open(config_file, "r") as yaml_file:
        config = yaml.safe_load(yaml_file.read())
        return config


def create_cassandra_cluster():

    result = subprocess.run(['docker-compose', '-f', f'{COMPOSE_FILE}', 'up', '-d'], capture_output=True, text=True)
    print(result.stdout)
import docker

def get_container_ips_by_name(container_names):
    client = docker.from_env()
    ips = []

    for container_name in container_names:
        try:
            container = client.containers.get(container_name)
            ip_address = container.attrs['NetworkSettings']['Networks']['cassandra-image_cassandra']['IPAddress']
            ips.append(ip_address)
        except docker.errors.NotFound:
            print(f"Container '{container_name}' not found.")
        except KeyError:
            print(f"IP for container '{container_name}' not found.")

    return ips

