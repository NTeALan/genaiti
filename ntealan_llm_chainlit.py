import os
from dotenv import dotenv_values
from langchain_community.graphs import Neo4jGraph
from langchain_community.llms import HuggingFaceEndpoint
from langchain.memory import ConversationBufferMemory

import chainlit as cl
from chainlit.input_widget import Select, Slider, TextInput
from chainlit.playground.config import add_llm_provider
from chainlit.playground.providers.langchain import LangchainGenericProvider

#from langfuse import Langfuse
#from langfuse.callback import CallbackHandler

from src.genaiti.callbacks import PostMessageHandler
from src.genaiti.graph_chain import GraphCypherQAChain
from src.genaiti.prompts_template import *
from src.genaiti.utils import parse_conversation_history


env_config = {
    **dotenv_values(".env"),  # load default development variables
    #**dotenv_values(".env.sample"),  # load sensitive variables (to use for you use case)
    **os.environ,  # override loaded values with environment variables
}

CYPHER_GENERATION_PROMPT = build_prompt_cypher_generator()
CYPHER_QA_PROMPT = build_prompt_cypher_qa_generator()
QUESTION_VALIDATION_PROMPT = build_question_validation_prompt()
SAFETY_PROMPT = build_safety_prompt()

#langfuse = Langfuse()
# Initialize Langfuse CallbackHandler for Langchain (tracing)
#langfuse_callback_handler = CallbackHandler()


"""Question answering over a graph."""

@cl.author_rename
def rename(orig_author):
    mapping = {
        "LLMChain": "Assistant",
        "HuggingFaceEndpoint": "Request HuggingFaceEndpoint",
    }
    return mapping.get(orig_author, orig_author)

@cl.cache
def get_chat_memory():
    return ConversationBufferMemory(memory_key="chat_history")

@cl.on_chat_resume
async def on_chat_resume(thread):
    memory = ConversationBufferMemory(return_messages=True)
    root_messages = [m for m in thread["steps"] if m["parentId"] == None]
    for message in root_messages:
        if message["type"] == "human":
            memory.chat_memory.add_user_message(message["content"])
        else:
            memory.chat_memory.add_ai_message(message["content"])

    #cl.user_session.set("memory", memory)


async def build_graph_chain(settings, CYPHER_QA_PROMPT, CYPHER_GENERATION_PROMPT,
                            SAFETY_PROMPT, QUESTION_VALIDATION_PROMPT):
    llm = None

    graph = Neo4jGraph(
        url=env_config['NEO4J_URI'], 
        username=env_config['NEO4J_USERNAME'], 
        password=env_config['NEO4J_PASSWORD']
    )

    llm = HuggingFaceEndpoint(
        repo_id=settings['qa_llm'],
        task=settings['model_task'].strip(),
        max_new_tokens=settings['max_new_token'],
        top_k=settings['top_k'],
        temperature=settings['temperature'],
        repetition_penalty=settings['repetition_penalty'],
        #model_kwargs={"add_to_git_credential":True} 
    )
    if settings['cypher_llm']:
        llm_cypher = HuggingFaceEndpoint(
            repo_id=settings['cypher_llm'],
            task=settings['model_task'].strip(),
            max_new_tokens=settings['max_new_token'],
            top_k=settings['top_k'],
            temperature=settings['temperature'],
            repetition_penalty=settings['repetition_penalty'],
            #model_kwargs={"add_to_git_credential":True} 
        )
    else: llm_cypher = llm
    if settings['validate_llm']:
        llm_checker = HuggingFaceEndpoint(
            repo_id=settings['validate_llm'],
            task=settings['model_task'].strip(),
            max_new_tokens=settings['max_new_token'],
            top_k=settings['top_k'],
            temperature=settings['temperature'],
            repetition_penalty=settings['repetition_penalty'],
            #model_kwargs={"add_to_git_credential":True} 
        )
    else: llm_checker = llm

    chain = GraphCypherQAChain.from_llm(
        llm=llm, 
        cypher_llm=llm_cypher,
        graph=graph, 
        checker_llm=llm_checker,
        #safety_prompt= SAFETY_PROMPT,
        #validate_prompt= QUESTION_VALIDATION_PROMPT,
        #qa_prompt=CYPHER_QA_PROMPT,
        #cypher_prompt=CYPHER_GENERATION_PROMPT,
        validate_cypher=True,
        exclude_types=[],
        include_types=[],
        verbose=False,
        cypher_llm_kwargs={
            "prompt": CYPHER_GENERATION_PROMPT,
            #"stop":4,
            #"stop_sequence":4
        },
        qa_llm_kwargs={
            "prompt": CYPHER_QA_PROMPT,
            #"stop":4,
            #"stop_sequence":4
        },
        checker_llm_kwargs={
            "prompt": QUESTION_VALIDATION_PROMPT,
            #"stop":4,
            #"stop_sequence":4
        },
        safety_llm_kwargs={
            "prompt": SAFETY_PROMPT,
            #"stop":4,
            #"stop_sequence":4
        } 
        #callbacks=[handler]
    )
   
    return llm, llm_cypher, graph, chain


"""
#@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    print(username,password)
    if (username, password) == ("admin@ya.fr", "admin"):
        return cl.User(
            identifier="admin", 
            metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None
   
@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="GPT-3.5",
            markdown_description="The underlying LLM model is **GPT-3.5**.",
            icon="https://picsum.photos/200",
        ),
        cl.ChatProfile(
            name="GPT-4",
            markdown_description="The underlying LLM model is **GPT-4**.",
            icon="https://picsum.photos/250",
        ),
    ]
"""

@cl.on_chat_start
async def on_chat_start():
    GraphCypherQAChain.update_forward_refs()

    settings = await cl.ChatSettings(
        [
            Select(
                id="qa_llm",
                label="HuggingFace LLM for final generation",
                values=["databricks/dbrx-instruct",
                        "mistralai/Mixtral-8x7B-Instruct-v0.1",  
                        "stabilityai/stable-code-instruct-3b",
                        "mistralai/Mistral-7B-Instruct-v0.2"],
                initial_index=3,
            ),
            Select(
                id="cypher_llm",
                label="HuggingFace LLM for cypher extraction and generation",
                values=["databricks/dbrx-instruct",
                        "mistralai/Mixtral-8x7B-Instruct-v0.1", 
                        "stabilityai/stable-code-instruct-3b",
                        "mistralai/Mistral-7B-Instruct-v0.2"],
                initial_index=3,
            ),
            Select(
                id="validate_llm",
                label="HuggingFace LLM to validate cypher command generated",
                values=["databricks/dbrx-instruct",
                        "mistralai/Mixtral-8x7B-Instruct-v0.1", 
                        "stabilityai/stable-code-instruct-3b",
                        "mistralai/Mistral-7B-Instruct-v0.2"],
                initial_index=3,
            ),
            Select(
                id="model_task",
                label="Model task",
                values=["text-generation", "code-completion"],
                initial_index=0,
            ),
            Slider(
                id="temperature",
                label="Temperature",
                initial=0.1,
                min=0.1,
                max=1,
                step=0.1,
            ),
            Slider(
                id="top_k",
                label="Top K",
                initial=1,
                min=0,
                max=20,
                step=1,
            ),
            Slider(
                id="max_new_token",
                label="Max output tokens",
                initial=245,
                min=5,
                max=450,
                step=5,
            ),
            Slider(
                id="repetition_penalty",
                label="Repetition penalty",
                initial=0.1,
                min=0,
                max=10,
                step=0.1,
            ),
            TextInput(id="AgentName", label="Agent Name", 
                      initial="NTeALan Bot"),
        ]
    ).send()

    llm, _, graph, chain = await build_graph_chain(settings, CYPHER_QA_PROMPT,
                                    CYPHER_GENERATION_PROMPT, SAFETY_PROMPT,
                                    QUESTION_VALIDATION_PROMPT)
    # disable langfuse observability
    """
    # Create trace with tags
    trace = langfuse.trace(
        name="chain_of_thought_ntealan",
        tags=["ntealan", "llm_dictionaries"],
        user_id="user-1234"
    )
    
    # Get Langchain callback handler for this trace
    handler_langfuse = trace.get_langchain_handler()
    """

    #chat_memory = get_chat_memory()
    #await chat_memory.chat_memory.aclear()

    # Add the LLM provider
    add_llm_provider(
        LangchainGenericProvider(
            # It is important that the id of the provider matches the _llm_type
            id=llm._llm_type,
            # The name is not important. It will be displayed in the UI.
            name="HuggingFaceHub",
            # This should always be a Langchain llm instance (correctly configured)
            llm=llm,
            # If the LLM works with messages, set this to True
            is_chat=True
        )
    )
    
    #cl.user_session.set("handler_langfuse", handler_langfuse)
    cl.user_session.set("chain", chain)
    #cl.user_session.set("chat_memory", chat_memory) 
    cl.user_session.set("settings", settings)
    cl.user_session.set("neo4j_graph", graph)
    cl.user_session.set("cypher_qa_prompt", CYPHER_QA_PROMPT) 
    cl.user_session.set("cypher_generation_prompt", CYPHER_GENERATION_PROMPT)
    cl.user_session.set("validation_prompt", QUESTION_VALIDATION_PROMPT) 
    cl.user_session.set("safety_prompt", SAFETY_PROMPT)

@cl.on_settings_update
async def update_setup_agent(settings):
    CYPHER_QA_PROMPT = cl.user_session.get("cypher_qa_prompt")
    CYPHER_GENERATION_PROMPT = cl.user_session.get("cypher_generation_prompt")
    QUESTION_VALIDATION_PROMPT = cl.user_session.get("validation_prompt")
    SAFETY_PROMPT = cl.user_session.get("safety_prompt")
    # graph = cl.user_session.get("graph")

    _,_, graph, chain = await build_graph_chain(settings,
                                        CYPHER_QA_PROMPT,
                                        CYPHER_GENERATION_PROMPT,
                                        SAFETY_PROMPT,
                                        QUESTION_VALIDATION_PROMPT)
    # chain.return_intermediate_steps = False
    cl.user_session.set("neo4j_graph", graph)
    cl.user_session.set("chain", chain) 
    cl.user_session.set("settings", settings)


@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")
    #memory = cl.user_session.get("chat_memory")
    #handler_langfuse = cl.user_session.get("handler_langfuse")
    msg = cl.Message(content="")

    #conversation_history = parse_conversation_history(memory.chat_memory.json())
    #conversation_history = "" if len(conversation_history) == 0 else f"\n{conversation_history}\n\n"
    
    #memory.chat_memory.add_user_message(message.content)
    
    """
    res = ""
    async for chunk in chain.astream(
            input=message.content, 
            #history=conversation_history,
            callbacks=[cl.LangchainCallbackHandler()]
        ):
        res += chunk
        await msg.stream_token(chunk)
    """   
    res = await chain.arun(
            query=message.content, 
            #history=conversation_history,
            callbacks=[
                cl.LangchainCallbackHandler(),
                PostMessageHandler(msg),
                #langfuse_callback_handler,
                #handler_langfuse
            ]
    )

    msg.content = res
    await msg.send()
    
    #memory.chat_memory.add_ai_message(res)

    


@cl.on_chat_end
def on_chat_end():
    print("The user disconnected!")


if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)
