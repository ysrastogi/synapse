from synapse.settings import DATABASES
import psycopg2
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
 
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

class VectorDB():
    def __init__(self) -> None:
        self.client = QdrantClient(url="http://localhost:6333")
    
    def create_collection(self, collection_name: str, vector_size: int, distance: Distance) -> None:
        self.client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=distance),
        )

    def upsert(self, collection_name: str, points: list[PointStruct], wait: bool = True) -> dict:
        operation_info = self.client.upsert(
            collection_name=collection_name,
            wait=wait,
            points=points,
        )
        return operation_info
    
    def search(self, collection_name: str, query: list[float], limit: int) -> list:
        search_result = self.client.query_points(
            collection_name=collection_name, query=query, limit=limit
        ).points
        return search_result
    
    def search_with_filter(self, collection_name: str, query: list[float], filter_key: str, filter_value: str, limit: int) -> list:
        search_result = self.client.query_points(
            collection_name=collection_name,
            query=query,
            query_filter=Filter(
                must=[FieldCondition(key=filter_key, match=MatchValue(value=filter_value))]
            ),
            with_payload=True,
            limit=limit,
        ).points
        return search_result