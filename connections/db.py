from synapse.settings import DATABASES
import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import ApiException
import sqlite3
import redis
import pylibmc
 
def connect_and_query(query):
    try:
        connection = psycopg2.connect(DATABASES)
        cursor= connection.cursor()
        query = sql.SQL(query)
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

class VectorDB:
    def __init__(self, qdrant_url: str = "http://localhost:6333") -> None:
        try:
            self.client = QdrantClient(url=qdrant_url)
        except ApiException as e:
            print(f"Failed to connect to Qdrant client: {e}")
            self.client = None

def setup_url_cache_database(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS url_cache (
                url TEXT PRIMARY KEY,
                content TEXT,
                last_fetched TIMESTAMP
            )
        ''')
        return conn, cursor

def redis_client():
    client = redis.Redis(host='localhost',port= 6379, db= 0)
    return client

def memcached_client(self, servers: list[str] = ["127.0.0.1"]):
        try:
            self.memcached_client = pylibmc.Client(servers, binary=True, behaviors={
                "tcp_nodelay": True,
                "ketama": True,
                "remove_failed": 1,
                "retry_timeout": 1,
                "dead_timeout": 60
            })
            print("Memcached client connection established")
        except pylibmc.Error as e:
            print(f"Failed to connect to Memcached: {e}")
            self.memcached_client = None