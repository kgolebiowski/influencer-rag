import pytest

from app.llm import llm_inference_executor


@pytest.mark.skip(reason="Not self-contained, require OpenAI key")
def test_run_llama():
    print("starting test")
    llm_inference_executor.main()
    print("test complete")
