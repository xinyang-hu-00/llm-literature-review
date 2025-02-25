from deepsearcher.configuration import Configuration, init_config
from deepsearcher.online_query import query

config = Configuration()

# Customize your config here,
# more configuration see the Configuration Details section below.
config.set_provider_config("llm", "OpenAI", {"model": "gpt-4o-mini"})
config.set_provider_config("embedding", "OpenAIEmbedding", {"model": "text-embedding-ada-002"})
#config.set_provider_config("vector_db", "Milvus", {"uri": "./milvus.db", "token": ""})
#config.set_provider_config("file_loader", "UnstructuredLoader", {})
init_config(config = config)

# Load your local data
# from deepsearcher.offline_loading import load_from_local_files
# load_from_local_files(paths_or_directory='coconut.pdf')

# (Optional) Load from web crawling (`FIRECRAWL_API_KEY` env variable required)
# from deepsearcher.offline_loading import load_from_website
# load_from_website(urls=website_url)

# Query
result = query("Write a report about latent space reasoning in LLM.") # Your question here