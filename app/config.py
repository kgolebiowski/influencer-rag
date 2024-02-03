import logging
from dataclasses import dataclass

from app.model.channel import Channel
from app.retrieval.vector_db_provider.vector_db_model import VectorDbType


@dataclass
class VectorDbConfig:
    max_score: float


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

channels = [
    # Channel('WesRoth', 'UCqcbQf6yw5KzRoDDcZ_wBSw'),
    # Channel('PromptEngineer48', 'UCX6c6hTIqcphjMsXbeanJ1g'),
    # Channel('engineerprompt', 'UCDq7SjbgRKty5TgGafW8Clg'),
    Channel('BenFelixCSI', 'UCDXTQ8nWmx_EhZ2v-kp7QxA')
]

# In theory should be the same for all cosine similarity searches
max_score_threshold = 0.6

default_vector_db = VectorDbType.CHROMA
vector_db_configs = {
    VectorDbType.CHROMA: VectorDbConfig(max_score_threshold),
    VectorDbType.ELASTICSEARCH: VectorDbConfig(max_score_threshold),
    VectorDbType.WEAVIATE: VectorDbConfig(max_score_threshold)
}

transcripts_dir_path = "data/transcripts"
evaluations_dir_path = "data/evaluations"
local_models_path = "../models/"

k = 4
additional_items_to_fetch_for_mmr = 20
hybrid_search = False
mmr_search = False
alpha = 0.50

# disable parallelism for tokenizers to silence the warnings
TOKENIZERS_PARALLELISM = False

# model_name = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
model_name = "gpt-3.5-turbo-1106"  # Requires OPENAI_API_KEY
# model_name = "ericzzz/falcon-rw-1b-instruct-openorca"
