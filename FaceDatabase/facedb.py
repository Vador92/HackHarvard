import weaviate

auth_config = weaviate.auth.AuthApiKey(api_key="<FUx4NB4rYZO8JUH0U0q4Ni8OBAA7RKLjR83P>")

# Create a Weaviate client with API key authentication
client = weaviate.Client(
    url="https://face-detection-v8iqjrfg.weaviate.network",
    auth_client_secret=auth_config,
    # Add any additional headers here if needed
    additional_headers={
        "X-Cohere-Api-Key": "<COHERE-KEY>",
        "X-HuggingFace-Api-Key": "<HUGGINGFACE-KEY>",
        "X-OpenAI-Api-Key": "<OPENAI-KEY>",
    }
)
