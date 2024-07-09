# customers/customers.py
from db.connection import get_connection

class Customer:
    def __init__(self, cust_id, name, email):
        self.id = cust_id
        self.name = name
        self.email = email

    def __str__(self):
        return f"Customer({self.id}, {self.name}, {self.email})"

    @classmethod
    def create_table(cls):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE customers (
                        id serial PRIMARY KEY,
                        name varchar NOT NULL,
                        email varchar NOT NULL UNIQUE)
                    """)
                conn.commit()

    @classmethod
    def create_customer(cls, name, email):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO customers (name, email) VALUES (%s, %s)", (name, email))
                conn.commit()

    @classmethod
    def get_all_customers(cls) -> list['Customer']:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM customers")
                return [Customer(cid, name, email) for cid, name, email in cur]

    @classmethod
    def get_customer_by_email(cls, email) -> 'Customer':
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, email FROM customers WHERE email = %s", (email,))
                (cid, name, email) = cur.fetchone()
                return Customer(cid, name, email)

    @classmethod
    def delete_all_customers(cls):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM customers")
                conn.commit()
