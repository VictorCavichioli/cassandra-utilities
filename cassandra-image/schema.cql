CREATE KEYSPACE IF NOT EXISTS ecchronos WITH replication = {'class': 'NetworkTopologyStrategy', 'dc1': 1, 'dc2': 2, 'dc3': 1};

CREATE TABLE IF NOT EXISTS ecchronos.lock (
    resource text,
    node uuid,
    metadata map<text,text>,
    PRIMARY KEY(resource))
    WITH default_time_to_live = 600
    AND gc_grace_seconds = 0;

CREATE TABLE IF NOT EXISTS ecchronos.lock_priority (
    resource text,
    node uuid,
    priority int,
    PRIMARY KEY(resource, node))
    WITH default_time_to_live = 600
    AND gc_grace_seconds = 0;

CREATE TABLE IF NOT EXISTS ecchronos.reject_configuration (
    keyspace_name text,
    table_name text,
    start_hour int,
    start_minute int,
    end_hour int,
    end_minute int,
    PRIMARY KEY(keyspace_name, table_name, start_hour, start_minute));

CREATE TYPE IF NOT EXISTS ecchronos.token_range (
    start text,
    end text);

CREATE TYPE IF NOT EXISTS ecchronos.table_reference (
    id uuid,
    keyspace_name text,
    table_name text);

CREATE TABLE IF NOT EXISTS ecchronos.on_demand_repair_status (
    host_id uuid,
    job_id uuid,
    table_reference frozen<table_reference>,
    token_map_hash int,
    repaired_tokens frozen<set<frozen<token_range>>>,
    status text,
    completed_time timestamp,
    repair_type text,
    PRIMARY KEY(host_id, job_id))
    WITH default_time_to_live = 2592000
    AND gc_grace_seconds = 0;

CREATE TABLE IF NOT EXISTS ecchronos.repair_history(
    table_id uuid,
    node_id uuid,
    repair_id timeuuid,
    job_id uuid,
    coordinator_id uuid,
    range_begin text,
    range_end text,
    participants set<uuid>,
    status text,
    started_at timestamp,
    finished_at timestamp,
    PRIMARY KEY((table_id,node_id), repair_id))
    WITH compaction = {'class': 'TimeWindowCompactionStrategy'}
    AND default_time_to_live = 2592000
    AND CLUSTERING ORDER BY (repair_id DESC);

CREATE KEYSPACE IF NOT EXISTS shoppingcart WITH replication = {'class': 'NetworkTopologyStrategy', 'dc1': 1, 'dc2': 2, 'dc3': 1};

CREATE TABLE IF NOT EXISTS shoppingcart.user_by_email (
  use_id UUID,
  use_email TEXT,
  use_pass TEXT,
  use_authority TEXT,
  PRIMARY KEY ((use_authority), use_email, use_id)
);

CREATE TABLE IF NOT EXISTS shoppingcart.customer_by_user (
  cus_id UUID,
  use_id UUID,
  cus_name TEXT,
  cus_document_number TEXT,
  cus_type TEXT,
  cus_credit_score TEXT,
  cus_addresses TEXT,
  cus_orders TEXT,
  PRIMARY KEY ((cus_type), use_id, cus_id)
);

CREATE TABLE IF NOT EXISTS shoppingcart.address_by_customer (
  cus_id UUID,
  add_cus_id UUID,
  add_cus_address TEXT,
  PRIMARY KEY ((cus_id), add_cus_id)
);

CREATE TABLE IF NOT EXISTS shoppingcart.address_by_id (
  add_id UUID,
  add_street TEXT,
  add_number INT,
  add_zip_code TEXT,
  add_state TEXT,
  add_country TEXT,
  PRIMARY KEY ((add_state, add_id), add_zip_code)
) WITH CLUSTERING ORDER BY(add_zip_code ASC);

CREATE TABLE IF NOT EXISTS shoppingcart.product_offering (
  pro_id UUID,
  pro_name TEXT,
  pro_price FLOAT,
  pro_category TEXT,
  PRIMARY KEY ((pro_category, pro_name), pro_id)
) WITH CLUSTERING ORDER BY(pro_id ASC);

CREATE TABLE IF NOT EXISTS shoppingcart.product_offering_by_id (
  pro_id UUID,
  pro_name TEXT,
  pro_price FLOAT,
  pro_discount FLOAT,
  pro_validate DATE,
  pro_description TEXT,
  pro_category TEXT,
  PRIMARY KEY ((pro_category, pro_id), pro_validate)
 
) WITH CLUSTERING ORDER BY(pro_validate ASC);

CREATE TABLE IF NOT EXISTS shoppingcart.order_by_user (
  use_id UUID,
  ord_id UUID,
  ord_instant_date DATE,
  ord_products TEXT,
  ord_quantity INT,
  ord_cus UUID,
  ord_address TEXT,
  ord_final_price DOUBLE,
  PRIMARY KEY ((use_id), ord_id)
);