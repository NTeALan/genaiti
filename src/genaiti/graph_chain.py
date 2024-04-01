
from typing import Any, Dict, List, Optional

from langchain_community.graphs.graph_store import GraphStore
from langchain_core.callbacks import CallbackManagerForChainRun
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.pydantic_v1 import Field

from langchain.chains.base import Chain
from langchain.chains.graph_qa.cypher_utils import CypherQueryCorrector, Schema
from langchain.chains.llm import LLMChain
from langchain.chains import ConversationChain

from .utils import *
from .prompts_template import *

CYPHER_GENERATION_PROMPT = build_prompt_cypher_generator()
CYPHER_QA_PROMPT = build_prompt_cypher_qa_generator()
QUESTION_VALIDATION_PROMPT = build_question_validation_prompt()
SAFETY_PROMPT = build_safety_prompt()


class GraphCypherQAChain(Chain):

    """Chain for question-answering against a graph by generating Cypher statements.

    *Security note*: Make sure that the database connection uses credentials
        that are narrowly-scoped to only include necessary permissions.
        Failure to do so may result in data corruption or loss, since the calling
        code may attempt commands that would result in deletion, mutation
        of data if appropriately prompted or reading sensitive data if such
        data is present in the database.
        The best way to guard against such negative outcomes is to (as appropriate)
        limit the permissions granted to the credentials used with this tool.

        See https://python.langchain.com/docs/security for more information.
    """

    graph: GraphStore = Field(exclude=True)
    cypher_generation_chain: LLMChain
    qa_chain: LLMChain
    checker_chain: LLMChain
    safety_chain: LLMChain

    graph_schema: str
    input_key: str = "query"  #: :meta private:
    #history_key: str = "history"  #: :meta private:
    output_key: str = "result"  #: :meta private:

    top_k: int = 10
    """Number of results to return from the query"""
    return_intermediate_steps: bool = False
    """Whether or not to return the intermediate steps along with the final answer."""
    return_direct: bool = False
    """Whether or not to return the result of querying the graph directly."""
    cypher_query_corrector: Optional[CypherQueryCorrector] = None
    """Optional cypher validation tool"""

    @property
    def input_keys(self) -> List[str]:
        """Return the input keys.

        :meta private:
        """
        return [self.input_key]
    
    #@property
    #def history_keys(self) -> List[str]:
    #    """Return the history keys.
    #
    #    :meta private:
    #    """
    #    return [self.history_key]
    
    @property
    def output_keys(self) -> List[str]:
        """Return the output keys.

        :meta private:
        """
        _output_keys = [self.output_key]
        return _output_keys

    @property
    def _chain_type(self) -> str:
        return "graph_cypher_chain"

    @classmethod
    def from_llm(
        cls,
        llm: Optional[BaseLanguageModel] = None,
        *,
        qa_prompt: Optional[BasePromptTemplate] = None,
        safety_prompt: Optional[BasePromptTemplate] = None,
        validate_prompt: Optional[BasePromptTemplate] = None,
        cypher_prompt: Optional[BasePromptTemplate] = None,
        cypher_llm: Optional[BaseLanguageModel] = None,
        qa_llm: Optional[BaseLanguageModel] = None,
        checker_llm: Optional[BaseLanguageModel] = None,
        exclude_types: List[str] = [],
        include_types: List[str] = [],
        validate_cypher: bool = False,
        qa_llm_kwargs: Optional[Dict[str, Any]] = None,
        cypher_llm_kwargs: Optional[Dict[str, Any]] = None,
        checker_llm_kwargs: Optional[Dict[str, Any]] = None,
        safety_llm_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ):
        """Initialize from LLM."""
        #if not safety_prompt and not validate_prompt:
        #    raise ValueError("Either `validate_prompt` or `safety_prompt` parameters must be provided")
        if not cypher_llm and not llm:
            raise ValueError("Either `llm` or `cypher_llm` parameters must be provided")
        if not qa_llm and not llm:
            raise ValueError("Either `llm` or `qa_llm` parameters must be provided")
        if cypher_llm and qa_llm and llm:
            raise ValueError(
                "You can specify up to two of 'cypher_llm', 'qa_llm'"
                ", and 'llm', but not all three simultaneously."
            )
        if cypher_prompt and cypher_llm_kwargs:
            raise ValueError(
                "Specifying cypher_prompt and cypher_llm_kwargs together is"
                " not allowed. Please pass prompt via cypher_llm_kwargs."
            )
        if qa_prompt and qa_llm_kwargs:
            raise ValueError(
                "Specifying qa_prompt and qa_llm_kwargs together is"
                " not allowed. Please pass prompt via qa_llm_kwargs."
            )
        if (safety_prompt and safety_llm_kwargs) or (validate_prompt and checker_llm_kwargs):
            raise ValueError(
                "Specifying safety_prompt/validate_prompt and use_checker_llm_kwargs together is"
                " not allowed. Please pass prompt via use_checker_llm_kwargs."
            )
        use_qa_llm_kwargs = qa_llm_kwargs if qa_llm_kwargs is not None else {}
        use_cypher_llm_kwargs = (
            cypher_llm_kwargs if cypher_llm_kwargs is not None else {}
        )
        use_checker_llm_kwargs= (
            checker_llm_kwargs if checker_llm_kwargs is not None else {}
        )
        use_safety_llm_kwargs= (
            safety_llm_kwargs if safety_llm_kwargs is not None else {}
        )
        if "prompt" not in use_qa_llm_kwargs:
            use_qa_llm_kwargs["prompt"] = (
                qa_prompt if qa_prompt is not None else CYPHER_QA_PROMPT
            )
        if "prompt" not in use_cypher_llm_kwargs:
            use_cypher_llm_kwargs["prompt"] = (
                cypher_prompt if cypher_prompt is not None else CYPHER_GENERATION_PROMPT
            )
        if "prompt" not in use_checker_llm_kwargs:
            use_checker_llm_kwargs["prompt"] = (
                validate_prompt if validate_prompt is not None else QUESTION_VALIDATION_PROMPT
            )
        if "prompt" not in use_safety_llm_kwargs:
            use_safety_llm_kwargs["prompt"] = (
                safety_prompt if safety_prompt is not None else SAFETY_PROMPT
            )

        qa_chain = LLMChain(llm=qa_llm or llm,
                            **use_qa_llm_kwargs)

        checker_chain = LLMChain(llm=checker_llm or llm,
                                **use_checker_llm_kwargs)
        
        safety_chain = LLMChain(llm=checker_llm or llm,
                                **use_safety_llm_kwargs)

        cypher_generation_chain = LLMChain(
            llm=cypher_llm or llm,
            **use_cypher_llm_kwargs
        )

        if exclude_types and include_types:
            raise ValueError(
                "Either `exclude_types` or `include_types` "
                "can be provided, but not both"
            )

        graph_schema = construct_schema(
            kwargs["graph"].get_structured_schema, 
            include_types, exclude_types
        )

        cypher_query_corrector = None
        if validate_cypher:
            corrector_schema = [
                Schema(el["start"], el["type"], el["end"])
                for el in kwargs["graph"].structured_schema.get("relationships")
            ]
            cypher_query_corrector = CypherQueryCorrector(corrector_schema)

        return cls(
            graph_schema=graph_schema,
            qa_chain=qa_chain,
            checker_chain=checker_chain,
            safety_chain=safety_chain,
            cypher_generation_chain=cypher_generation_chain,
            cypher_query_corrector=cypher_query_corrector,
            **kwargs
        )

    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        """Generate Cypher statement, use it to look up in db and answer question."""
        _run_manager = run_manager or CallbackManagerForChainRun.get_noop_manager()
        callbacks = _run_manager.get_child()
        question = inputs[self.input_key]
        #history = inputs[self.history_key]

        intermediate_steps: List = []

        # get cypher command based of user question
        is_can_be_cypher_command = self.checker_chain.run(
            {"question": question}, 
            callbacks=callbacks
        )
        is_can_be_cypher_command = get_response_from_generator(is_can_be_cypher_command, qa_re)
        intermediate_steps.append({"is_can_be_translated_to_cypher_command": is_can_be_cypher_command})
        print("is_can_be_cypher_command: ", is_can_be_cypher_command)
        if is_can_be_cypher_command.strip() == "False":
            _run_manager.on_text("User can't be translated to Cypher:", end="\n", verbose=self.verbose)
            _run_manager.on_text(
                is_can_be_cypher_command, color="green", end="\n", verbose=self.verbose
            )
            result = self.qa_chain.run(
                {"question": question, "context": ""},
                callbacks=callbacks,
            )
            final_result = get_response_from_generator(result["text"], qa_re)
            chain_result: Dict[str, Any] = {self.output_key: final_result}
            return chain_result
            
        # get cypher command based of user question
        generated_cypher = self.cypher_generation_chain.run(
            {"question": question, "schema": self.graph_schema}, 
            callbacks=callbacks
        )

        generated_cypher = get_response_from_generator(generated_cypher)
        # Extract Cypher code if it is wrapped in backticks
        generated_cypher = extract_cypher(generated_cypher)

        print("generated_cypher: ", generated_cypher)

        # Correct Cypher query if enabled
        if self.cypher_query_corrector:
            generated_cypher = self.cypher_query_corrector(generated_cypher)

        _run_manager.on_text("Generated Cypher:", end="\n", verbose=self.verbose)
        _run_manager.on_text(
            generated_cypher, color="green", end="\n", verbose=self.verbose
        )
        intermediate_steps.append({"query": generated_cypher})

        # Retrieve and limit the number of results
        # Generated Cypher be null if query corrector identifies invalid schema
        if generated_cypher:
            try:
                context = self.graph.query(generated_cypher)[: self.top_k]
            except:
                chain_result: Dict[str, Any] = {self.output_key: 
                    "Je ne peux pas obtenir de réponse avec la requète Cypher générée. <br> Exception générée dans le graphe."}
                return chain_result
        else: context = []

        if self.return_direct:
            final_result = context
        else:
            # print("context", context)
            _run_manager.on_text("Full Context:", end="\n", verbose=self.verbose)
            _run_manager.on_text(
                str(context), color="green", end="\n", verbose=self.verbose
            )

            intermediate_steps.append({"context": context})

            result = self.qa_chain(
                {"question": question, "context": context},
                callbacks=callbacks,
            )
            print(result)
            final_result = result[self.qa_chain.output_key]

            final_result = get_response_from_generator(final_result, qa_re)

        chain_result: Dict[str, Any] = {self.output_key: final_result}
        if self.return_intermediate_steps:
            chain_result[INTERMEDIATE_STEPS_KEY] = intermediate_steps

        return chain_result
    
