from typing import Optional

from app.llm.llm_provider.llm_model import LlmModel
from app.llm.llm_provider.llm_model_llama_cpp import LlmModelLlamaCpp
from app.llm.llm_provider.llm_model_open_ai import LlmModelOpenAI
from app.llm.llm_provider.llm_model_transformers import LlmModelTransformers

llm_model = None


def get_llm_model(model_name: str, local_models_path: str) -> Optional[LlmModel]:
    global llm_model

    if llm_model is None:
        if "gguf" in model_name:
            llm_model = LlmModelLlamaCpp(model_name, local_models_path)
        elif "gpt" in model_name:
            llm_model = LlmModelOpenAI(model_name)
        else:
            llm_model = LlmModelTransformers(model_name)

    return llm_model
