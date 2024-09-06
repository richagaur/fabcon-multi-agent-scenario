from azure.cosmos import CosmosClient
from azure.cosmos import PartitionKey, exceptions
import hashlib

cosmos_db_endpoint = "https://cosmos-info-db.documents.azure.com:443/"
cosmos_db_key = ""
database_name = "DocsDatabase"
container_name = "DocsContainer"


class CosmosDBClient:
    def __init__(self):
            self.client = CosmosClient(cosmos_db_endpoint, cosmos_db_key)
            self.db = self.client.create_database_if_not_exists(database_name)
            
            # Create the vector embedding policy to specify vector details
            vector_embedding_policy = {
                "vectorEmbeddings": [ 
                    { 
                        "path":"/vector",
                        "dataType":"float32",
                        "distanceFunction":"cosine",
                        "dimensions": int(1536)
                    }, 
                ]
            }

            # Create the vector index policy to specify vector details
            indexing_policy = {
                "includedPaths": [ 
                { 
                    "path": "/*" 
                } 
                ], 
                "excludedPaths": [ 
                { 
                    "path": "/\"_etag\"/?",
                    "path": "/vector/*",
                } 
                ], 
                "vectorIndexes": [ 
                    {
                        "path": "/vector", 
                        "type": "quantizedFlat" 
                    }
                ]
            } 

            # Create the data collection with vector index (note: this creates a container with 10000 RUs to allow fast data load)
            try:
                self.container = self.db.create_container_if_not_exists(id=container_name, 
                                                            partition_key=PartitionKey(path='/title'), 
                                                            indexing_policy=indexing_policy,
                                                            vector_embedding_policy=vector_embedding_policy) 
                print('Container with id \'{0}\' created'.format(self.container.id)) 

            except exceptions.CosmosHttpResponseError: 
                raise 
            
    def store_metadata(self,title, page_start, page_end, blob_url, embedding):
        hash_object = hashlib.sha256(title.encode())
        doc_id = hash_object.hexdigest()
        metadata = {
            "id": doc_id,
            "title": title,
            "blobUrl": blob_url,
            "pageStart": page_start,
            "pageEnd": page_end,
            "vector": embedding
        }
        self.container.upsert_item(metadata)
        
        # Perform a vector search on the Cosmos DB container
    def vector_search(self, vectors, similarity_score=0.1, num_results=3):
        # Execute the query
        results = self.container.query_items(
            query= '''
            SELECT TOP @num_results  c.blobUrl, c.title, VectorDistance(c.vector, @embedding) as SimilarityScore 
            FROM c
            WHERE VectorDistance(c.vector,@embedding) > @similarity_score
            ORDER BY VectorDistance(c.vector,@embedding)
            ''',
            parameters=[
                {"name": "@embedding", "value": vectors},
                {"name": "@num_results", "value": num_results},
                {"name": "@similarity_score", "value": similarity_score}
            ],
            enable_cross_partition_query=True, populate_query_metrics=True)
        results = list(results)
        print(f"Found {len(results)} similar articles")
        # Extract the necessary information from the results
        formatted_results = []
        for result in results:
            score = result.pop('SimilarityScore')
            formatted_result = {
                'SimilarityScore': score,
                'document': result
            }
            formatted_results.append(formatted_result)

        return formatted_results

# if __name__ == "__main__":
#     title = "Example Section"
#     page_start = 1
#     page_end = 3
#     blob_url = "https://your-blob-url"
#     embedding = [0.1, 0.2, 0.3]  # Example embedding
#     cosmos_client = CosmosDBClient()
#     cosmos_client.store_metadata(title, page_start, page_end, blob_url, embedding)
