from deepsearcher import configuration
from collections import defaultdict

from deepsearcher.agent import (
    generate_final_answer,
    generate_gap_queries,
    generate_sub_queries,
    generate_cur_sec_summary,
    generate_sec_content
)


def dfs(original_query: str):
    llm = configuration.llm
    tree = defaultdict(list)
    stack, visited = [], set()
    node_values = {}  # Dictionary to store computed values
    stack.append(original_query)
    final_answer = []
    tree_complete = False

    while stack:
        node = stack[-1]  # Peek at the top of the stack

        sub_queries, used_token = generate_sub_queries(node)

        if len(sub_queries)>0:
            tree[node] = sub_queries # add children to tree
            node_response, used_token2 = generate_cur_sec_summary(node, sub_queries)
            final_answer.append(node_response) # add current section summary/content to final answer
            stack.extend(sub_queries)
        else:
            # All children processed, now process this node
            stack.pop()
            # TO-DO: add websearch to retieve docs and store them in the retrieved_PDF folder (maybe), and process those docs using search_vdb.py
            chuncks = "" 
            node_response, used_token2 = generate_sec_content(node, chuncks)
            final_answer.append(node_response)

            
            
            print("complete section reponse.")
    

    return final_answer