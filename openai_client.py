from openai import AzureOpenAI
import json

openai_endpoint = "https://richag-openai.openai.azure.com/"
openai_key = ""
openai_type = "azure"
openai_api_version = "2023-05-15"
openai_embeddings_deployment = "richag-embedding-deployment"
openai_embeddings_model = "text-embedding-3-large"
openai_embeddings_dimensions = 1536
openai_completions_deployment = "richag-completions-model"
openai_completions_model = "gpt-4o"

openai_client = AzureOpenAI(azure_endpoint=openai_endpoint, api_key=openai_key, api_version=openai_api_version)

def generate_embeddings(content):    
        '''
        Generate embeddings from string of text.
        This will be used to vectorize data and user input for interactions with Azure OpenAI.
        '''
        response = openai_client.embeddings.create(input=content, 
                                                model=openai_embeddings_deployment,
                                                dimensions=openai_embeddings_dimensions)
        embeddings =response.model_dump()
        return embeddings['data'][0]['embedding']

def generate_completion(user_prompt, vector_search_results):
        
        system_prompt = """You are an intelligent information retrieval and summarizer assistant, designed to provide accurate and helpful answers to user queries about Azure Cosmos DB, using only the provided JSON data.
                Instructions:
                - Only reference the content included in the JSON data.
                - If the data related to user query is not available, politely inform the user that you cannot answer queries about it.
                - If you are unsure of an answer, respond with "I don't know" or "I'm not sure," and suggest the user perform a search on their own.
                - Ensure your response is clear, complete, and suitable for display on a web page.
                - Assume the user has no prior knowledge of the topic in question.
                Formatting Instructions:
                - Format the response as a list of headlines and concise summaries.
                - Format the response to be suitable for display on a console.
                
            """
        #     Formatting Instructions:
        #         - Use <h3> for each headline.
        #         - Provide concise summaries underneath each headline in <p> tags.
        #        

        # system prompt
        messages = [{'role': 'system', 'content': system_prompt}]

        #chat history
        # for chat in chat_history:
        #     if chat['prompt'] and chat['completion']:
        #         messages.append({'role': 'user', 'content': chat['prompt'] + " " + chat['completion']})
        
        #user prompt
        messages.append({'role': 'user', 'content': user_prompt})

        #vector search results
        for result in vector_search_results:
            if result['document']:
                messages.append({'role': 'system', 'content': json.dumps(result['document'])})

        # Create the completion
        response = openai_client.chat.completions.create(
            model = openai_completions_deployment,
            messages = messages,
            temperature = 0.1
        )    
        return response.model_dump()

# if __name__ == "__main__":
#     content = "example_content"
#     embedding = generate_embeddings(content)
#     print(f"Generated embedding: {embedding[:10]}...")  # Print first 10 values for brevity
