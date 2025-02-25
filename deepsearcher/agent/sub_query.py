from typing import List, Tuple

# from deepsearcher.configuration import llm
from deepsearcher import configuration

PROMPT = """To answer this question more comprehensively, please break down the original question into up to four sub-questions. Return as list of str.
If this is a very simple question and no decomposition is necessary, then keep the only one original question in the list.

Original Question: {original_query}


<EXAMPLE>
Example input:
"Provide an academic-level comprehensive literature review for sparse autoencoder"

Example output:
[
    "Foundations of sparse autoencoder",
    "Key development in sparse autoencoder research",
    "Applications of sparse autoencoder",
    "Future directions of sparse autoencoder"
]
</EXAMPLE>

Provide your response in list of str format:
"""


def generate_sub_queries(original_query: str) -> Tuple[List[str], int]:
    llm = configuration.llm
    print(llm)
    chat_response = llm.chat(
        messages=[{"role": "user", "content": PROMPT.format(original_query=original_query)}]
    )
    response_content = chat_response.content
    return llm.literal_eval(response_content), chat_response.total_tokens
