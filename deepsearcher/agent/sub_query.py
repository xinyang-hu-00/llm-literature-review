from typing import List, Tuple

# from deepsearcher.configuration import llm
from deepsearcher import configuration

PROMPT = """To provide a comprehensive answer, break the question into up to four sub-questions, each covering a different aspect. Return a list of strings. If this is a very simple question and no decomposition is necessary, then keep the only one original question in the list. Cite recent academic papers from top journals or conferences.

Original Question: {original_query}


<EXAMPLE>
Example input:
"Provide a academic-level literature review for Sparse Autoencoders."

Example output:
[
    "Definitions and foundations of sparse autoencoders",
    "Key developments and insights of sparse autoencoders",
    "Applications of sparse autoencoders",
    "Future research directions of sparse autoencoders"
]
</EXAMPLE>

Provide your response in list of str format:
"""


def generate_sub_queries(original_query: str) -> Tuple[List[str], int]:
    llm = configuration.llm
    
    chat_response = llm.chat(
        messages=[{"role": "user", "content": PROMPT.format(original_query=original_query)}]
    )
    response_content = chat_response.content
    return llm.literal_eval(response_content), chat_response.total_tokens


