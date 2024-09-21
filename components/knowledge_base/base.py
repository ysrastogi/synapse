from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from connections.db import VectorDB
from connections.pubsub import Publisher
import uuid

class KnowledgeBaseFunc(VectorDB):
    def __init__(self):
        super().__init__()
        self.service_id = 'knowledge_base'+str(uuid.uuid4())
        self.publisher = Publisher('knowledge_base_updates', self.service_id)
    
    def get_service_id(self):
        return self.service_id
    
    def create_collection(self, collection_name: str, vector_size: int, distance: Distance) -> None:
            self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance),
            )
            self.publisher.publish(f"Collection {collection_name} created with vector size {vector_size} and distance {distance}")

    def upsert(self, collection_name: str, points: list[PointStruct], wait: bool = True) -> dict:
        operation_info = self.client.upsert(
            collection_name=collection_name,
            wait=wait,
            points=points,
        )
        self.publisher.publish(f"Upserted points into collection {collection_name}")
        return operation_info

    def search(self, collection_name: str, query: list[float], limit: int) -> list:
        search_result = self.client.query_points(
            collection_name=collection_name, query=query, limit=limit
        ).points
        self.publisher.publish(f"Searched in collection {collection_name} with query {query} and limit {limit}")
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
        self.publisher.publish(f"Searched in collection {collection_name} with query {query}, filter {filter_key}={filter_value}, and limit {limit}")
        return search_result
    
    def neural_searcher(self, collection_name: str, model=None, embeddings=None, text:str= None):
        """
        Neural Searcher function to search the given text in the collection
        """
        vector = self.model.embed_query(text)
        if not isinstance(vector, list):
            vector = vector.tolist()
        search_result = self.client.search(
            collection_name=self.collection_name, 
            query_vector=vector,
            query_filter=None, 
            limit=2
        )
        payloads = [hit.payload for hit in search_result]
        self.publisher.publish(f"Neural searcher collection {collection_name} with text '{text}'")
        return payloads