
import re
from typing import Any, Dict, List
import json

INTERMEDIATE_STEPS_KEY = "intermediate_steps"
resp_re = re.compile(r"(Answer|Réponse|>Cypher query|or)=")
qa_re = re.compile(r"(Answer|Réponse|>Cypher query|or|Useful Answer)=")
info_check = re.compile(r"(\n\n.+Information|\n\n\n.+|>.+|or|Question=)")
remover = re.compile(r"(<br.+>|>\n+|<\n+)")

__all__ = ["extract_cypher", "get_response_from_generator", "construct_schema",
           "qa_re", "resp_re", "INTERMEDIATE_STEPS_KEY", 
           "parse_conversation_history"]


def parse_conversation_history(history):
    history = json.loads(history)
    formatted_history = ""
    messages = history.get('messages')
    for message in messages:
        formatted_history += f"{message.get('type')}: {message.get('content')}\n"
    
    # print(formatted_history)
    return formatted_history


def extract_cypher(text: str) -> str:
    """Extract Cypher code from a text.

    Args:
        text: Text to extract Cypher code from.

    Returns:
        Cypher code extracted from the text.
    """
    # The pattern to find Cypher code enclosed in triple backticks
    pattern = r"```(.*?)```"

    # Find all matches in the input text
    matches = re.findall(pattern, text, re.DOTALL)

    return matches[0] if matches else text


def get_response_from_generator(generator, sep=resp_re):
    split_generated_cypher = sep.split(generator, re.IGNORECASE)
    if len(split_generated_cypher) >= 1:
        f_info_check = info_check.split(split_generated_cypher[0])
        if len(f_info_check) >= 1:
            print(split_generated_cypher[0], f_info_check)
            return remover.sub("", info_check.split(f_info_check[0])[0])
        else: return split_generated_cypher[0]
    else: return generator


def construct_schema(
    structured_schema: Dict[str, Any],
    include_types: List[str],
    exclude_types: List[str],
) -> str:
    """Filter the schema based on included or excluded types"""

    def filter_func(x: str) -> bool:
        return x in include_types if include_types else x not in exclude_types

    filtered_schema: Dict[str, Any] = {
        "node_props": {
            k: v
            for k, v in structured_schema.get("node_props", {}).items()
            if filter_func(k)
        },
        "rel_props": {
            k: v
            for k, v in structured_schema.get("rel_props", {}).items()
            if filter_func(k)
        },
        "relationships": [
            r
            for r in structured_schema.get("relationships", [])
            if all(filter_func(r[t]) for t in ["start", "end", "type"])
        ],
    }

    # Format node properties
    formatted_node_props = []
    for label, properties in filtered_schema["node_props"].items():
        props_str = ", ".join(
            [f"{prop['property']}: {prop['type']}" for prop in properties]
        )
        formatted_node_props.append(f"{label} {{{props_str}}}")

    # Format relationship properties
    formatted_rel_props = []
    for rel_type, properties in filtered_schema["rel_props"].items():
        props_str = ", ".join(
            [f"{prop['property']}: {prop['type']}" for prop in properties]
        )
        formatted_rel_props.append(f"{rel_type} {{{props_str}}}")

    # Format relationships
    formatted_rels = [
        f"(:{el['start']})-[:{el['type']}]->(:{el['end']})"
        for el in filtered_schema["relationships"]
    ]

    return "\n".join(
        [
            "Node properties are the following:",
            ",".join(formatted_node_props),
            "Relationship properties are the following:",
            ",".join(formatted_rel_props),
            "The relationships are the following:",
            ",".join(formatted_rels),
        ]
    )

