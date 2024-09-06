from azure.storage.blob import BlobServiceClient

container_name = "learn-docs"
connection_string = ""
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
blob_container_client = blob_service_client.get_container_client(container_name)

def upload_to_blob(section_content, title):
    blob_name = f"section_{title.replace(' ', '_')}"
    blob_client = blob_container_client.get_blob_client(blob_name)
    blob_client.upload_blob(section_content, blob_type="BlockBlob", overwrite=True)
    
    return f"https://learndocstorage.blob.core.windows.net/docs/{blob_name}"


def download_blob(blob_name):
    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Get the BlobClient for the specific blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    # Download the blob data
    download_stream = blob_client.download_blob()
    blob_data = download_stream.readall()  # Read all data from the blob
    
    return blob_data

# if __name__ == "__main__":
#     section_content = b"example_binary_content"  # Use binary content
#     title = "Example Section"
#     url = upload_to_blob(section_content, title)
#     print(f"Uploaded to {url}")
