from extract_toc import extract_toc
from blob_client import upload_to_blob
from openai_client import generate_embeddings
from cosmos_client import CosmosDBClient

cosmos_client = CosmosDBClient()
 
def process_pdf(pdf_path):
    sections = extract_toc(pdf_path)
    
    for section in sections:
        title = section["title"]
        content = section["content"]  # Binary content now
        page_start = section["page_start"]
        page_end = section["page_end"]
        text = section["text_content"]
        
        # Step 2: Upload content to Blob Storage
        # blob_url = upload_to_blob(content, title) TODO: experiment with content instead of text
        blob_url = upload_to_blob(text, title)
        
        # Step 3: Optionally generate vector embeddings (on the text or content as needed)
        embedding = []
        if text is not None and text != "":
            embedding = generate_embeddings(text)  # Skipping for binary content here
        
        # Step 4: Store metadata (without embedding for now)
        cosmos_client.store_metadata(title, page_start, page_end, blob_url, embedding)

if __name__ == "__main__":
    pdf_path = "C:\\Users\\richagaur\\Desktop\\azure-cosmos-db.pdf"
    process_pdf(pdf_path)
