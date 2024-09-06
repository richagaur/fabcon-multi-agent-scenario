from cosmos_client import CosmosDBClient
from openai_client import generate_completion, generate_embeddings
from blob_client import download_blob

cosmos_client  = CosmosDBClient()
def main(query):
    # Step 1: Generate embedding for the query
    embedding = generate_embeddings(query)
    
    # Step 2: Query Cosmos DB for relevant documents
    results = cosmos_client.vector_search(embedding)
    
    if not results:
        print("No relevant documents found.")
        return
    
    # Step 3: Fetch content from the top result (you can expand to multiple results)
    blob_results = []
    for result in results:
        blob_name = result['document']['blobUrl'].split('/')[-1]
        content = download_blob(blob_name)
        document = {
            'content': content.decode('utf-8'),
            'title': result['document']['title']
        }
        blob_result = {
            "document": document
        }
       
        blob_results.append(blob_result)
    
    # Step 4: Generate a chat response from the retrieved content
    response = generate_completion(query, blob_results)  # Assuming it's text, you may need to handle binary formats like PDFs differently
    formatted_responnse = response['choices'][0]['message']['content']
    print(f"Response: {formatted_responnse}")

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    main(user_query)
