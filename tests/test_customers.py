# tests/test_customers.py
import os
import pytest
import logging
import psycopg
from testcontainers.postgres import PostgresContainer

# Import the Customer class from the correct module
from customers.customers import Customer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres = PostgresContainer("postgres:16-alpine")
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    
    # Get connection details from the container
    connection_url = postgres.get_connection_url()
    db_info = connection_url.split("/")
    db_name = db_info[-1]
    user_info = db_info[-2].split(":")
    db_user = user_info[0]
    db_password = user_info[1].split("@")[0]
    db_host = user_info[1].split("@")[1]
    db_port = db_info[-2].split(":")[-1]

    os.environ["DB_CONN"] = connection_url
    os.environ["DB_HOST"] = db_host
    os.environ["DB_PORT"] = db_port
    os.environ["DB_USERNAME"] = db_user
    os.environ["DB_PASSWORD"] = db_password
    os.environ["DB_NAME"] = db_name
    Customer.create_table()

@pytest.fixture(scope="function", autouse=True)
def setup_data():
    Customer.delete_all_customers()

def test_get_all_customers():
    logger.info("Starting test_get_all_customers")
    
    customers_list = Customer.get_all_customers()
    assert len(customers_list) == 0, "Database is not empty at the beginning of the test"
    logger.info("Database is empty before starting the test")

    Customer.create_customer("Siva", "siva@gmail.com")
    Customer.create_customer("James", "james@gmail.com")
    customers_list = Customer.get_all_customers()
    assert len(customers_list) == 2

def test_get_customer_by_email():
    Customer.create_customer("John", "john@gmail.com")
    customer = Customer.get_customer_by_email("john@gmail.com")
    assert customer.name == "John"
    assert customer.email == "john@gmail.com"

def test_get_customer_by_name():
    Customer.create_customer("Yusuf", "yusuf@gmail.com")
    customer = Customer.get_customer_by_name("Yusuf")
    assert customer.name == "Joe"
