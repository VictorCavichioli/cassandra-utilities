import random
import logging
import threading
import time
import colorlog

from cassandra_connection import CassandraConnection

NAMES = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hank"]
ADDRESS = [
    "Rua tal 17",
    "Avenida Brasil 10",
    "Rua tal 3",
    "Rua icatu 12",
    "Rua tal 2",
    "Rua tal 10",
    "Rua tal 17",
]
STATUS = ["Regular", "Customer", "Enterprise"]


class CassandraMockData:
    def __init__(self):
        self.conn = CassandraConnection(execute_file=True)
        self.thread_colors = {}

        self.logger = colorlog.getLogger()
        self.logger.setLevel(colorlog.INFO)
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter("%(log_color)s%(levelname)s:%(name)s:%(message)s")
        )
        self.logger.addHandler(handler)

    def generate_mock_data(self, conn):
        if not conn:
            conn = self.conn

        random_name = random.choice(NAMES)
        random_address = random.choice(ADDRESS)
        random_status = random.choice(STATUS)
        customer_by_user = f"""
            INSERT INTO customer_by_user (cus_id, use_id, cus_name, cus_document_number, cus_type, cus_credit_score, cus_addresses, cus_orders)
            VALUES (
                uuid(),
                uuid(),
                '{random_name}',
                {"'123456789'"},
                '{random_status}',
                {"'Good'"},
                '{random_address}',
                {"'product'"}
            );
        """
        address_by_customer = f"""
            INSERT INTO address_by_customer (cus_id, add_cus_id, add_cus_address)
            VALUES (
                uuid(),
                uuid(),
                '{random_address}'
            );
        """

        address_by_id = f"""
            INSERT INTO address_by_id (add_id, add_street, add_number, add_zip_code, add_state, add_country)
            VALUES (
                uuid(),
                'Rua example',
                456,
                '54321-876',
                'Estado',
                'País'
            );
        """

        product_offering = f"""
            INSERT INTO product_offering (pro_id, pro_name, pro_price, pro_category)
            VALUES (
                uuid(),
                'Example Product',
                29.99,
                'Categoria'
            );
        """
        product_offering_by_id = f"""
            INSERT INTO product_offering_by_id (pro_id, pro_name, pro_price, pro_discount, pro_validate, pro_description, pro_category)
            VALUES (
                uuid(),
                'Detailed Product',
                39.99,
                0.1,
                '2024-02-28',
                'Detailed Description',
                'Detailed Category'
            );
        """
        order_by_user = f"""
            INSERT INTO order_by_user (use_id, ord_id, ord_instant_date, ord_products, ord_quantity, ord_cus, ord_address, ord_final_price)
            VALUES (
                uuid(),
                uuid(),
                '2024-01-11',
                'products',
                2,
                uuid(),
                'address',
                39.98
            );
        """

        conn.session.execute(customer_by_user)

        conn.session.execute(address_by_customer)

        conn.session.execute(address_by_id)

        conn.session.execute(product_offering)

        conn.session.execute(product_offering_by_id)

        conn.session.execute(order_by_user)

    def populate_mock_data(self, limit=1000001):
        thread_id = threading.current_thread().ident

        logger = colorlog.getLogger(f"Thread-{thread_id}")

        conn = CassandraConnection()
        cont = 0
        while cont < limit:
            logger.info(f"Inserting record number {cont}")
            self.generate_mock_data(conn)
            cont += 1
        conn.session.shutdown()

    def update_half_part_of_the_table(self):
        select_statement = "SELECT * FROM customer_by_user"

        data = self.conn.session.execute(select_statement)

        res = data[::2] + data[1::2]

        print(f"First Final Data: {res[0].use_id}")
        cont = 0
        for i in res:
            random_name = random.choice(NAMES)
            print(f"Updating record number: {cont}")
            query = f"UPDATE shoppingcart.customer_by_user SET cus_name='{random_name}' WHERE cus_type='{i.cus_type}' AND use_id={i.use_id} AND cus_id={i.cus_id};"
            self.conn.session.execute(query)
            cont += 1

    def speed_run_populate_data(self, core=5):
        start_time = time.time()
        threads = []
        for i in range(core):
            thread = threading.Thread(target=self.populate_mock_data, args=(10000,))
            threads.append(thread)
            logging.info(f"Main    :creating thread {i}")
            thread.start()

        for thread in threads:
            logging.info("Main    : wait for the thread to finish")
            thread.join()
            logging.info("Main    : all done")
        end_time = time.time()

        total_time = end_time - start_time

        logging.info(f"Main    :time spend populating data {total_time}")
