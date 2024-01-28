import os
import time
from datetime import timedelta

from app import config
from app.evaluations import evaluations
from app.evaluations.evaluations import persist_evaluation
from app.evaluations.evaluations_config import evaluations_config
from app.llm.llm_provider.llm_model_factory import get_llm_model
from app.model.rag_response import RagResponse
from app.retrieval.vector_db_provider.vector_db_model import get_vector_db

llm_model = None


def init():
    os.putenv("TOKENIZERS_PARALLELISM", str(config.TOKENIZERS_PARALLELISM))


init()


def prepare_transcription_fragments(relevant_movie_chunks, max_score: float):
    movie_fragments_for_llm = []

    for movie_chunk in relevant_movie_chunks:
        document, score = movie_chunk

        if score < max_score:
            movie_metadata = document.metadata
            movie_fragments_for_llm.append(
                f"Movie title: '{movie_metadata['title']}', "
                f"movie transcript: '{movie_metadata['paragraph']}'; ")
            # '{document.page_content}' is the chunk

    if len(movie_fragments_for_llm) > 0:
        return movie_fragments_for_llm
    else:
        return None


def ask_question(users_query, enable_vector_search, k=config.k, vector_db=config.default_vector_db, hybrid_search=config.hybrid_search, alpha=config.alpha):
    query_start_time = time.time()

    if enable_vector_search:
        vector_db_model = get_vector_db(vector_db)
        relevant_movie_chunks = vector_db_model.similarity_search_with_score(users_query, k, hybrid_search, alpha)
        relevant_movies_list = prepare_transcription_fragments(
            relevant_movie_chunks,
            config.vector_db_configs[vector_db].max_score
        )
        if relevant_movies_list is not None:
            relevant_movies = "\n".join(relevant_movies_list)
        else:
            relevant_movies = None
    else:
        relevant_movies = None

    if relevant_movies is not None:
        system = ("You'll get a question and a series of Youtube movie transcripts. "
                  "Each movie will contain the title and the relevant transcription fragment. "
                  "Base your answer only on the data coming from provided transcriptions and "
                  "make sure to always include the movie title in your answer."
                  f" List of movies: {relevant_movies}")
    else:
        system = ("First, say explicitly that you haven't found any relevant information "
                  "in the movie library. Then answer the following question "
                  "based on your knowledge.")

    llm_model_response = (
        get_llm_model(config.model_name, config.local_models_path).get_model_response(system, users_query))

    llm_user_response = llm_model_response.llm_user_response
    llm_full_response = llm_model_response.llm_full_response

    execution_time = time.time() - query_start_time

    if evaluations_config.evaluations_enabled and enable_vector_search and llm_user_response:
        evaluation = evaluations.evaluate_question(users_query, relevant_movies_list, llm_user_response)
    else:
        evaluation = None

    return RagResponse(
        query=users_query,
        llm_user_response=llm_user_response,
        llm_full_response=llm_full_response,
        relevant_movie_chunks=relevant_movie_chunks,
        evaluation=evaluation,
        response_time=timedelta(seconds=execution_time)
    )


def process_question(users_query, enable_vector_search, k=config.k, vector_db=config.default_vector_db, hybrid_search=config.hybrid_search, alpha=config.alpha):
    response = ask_question(users_query, enable_vector_search, k, vector_db=vector_db, hybrid_search=hybrid_search, alpha=alpha)

    if response.evaluation:
        persist_evaluation(response, k)

    return response
