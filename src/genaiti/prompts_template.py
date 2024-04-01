from langchain_core.prompts import PromptTemplate


__all__ = ['build_prompt_cypher_generator',
           'build_prompt_cypher_qa_generator',
           'build_question_validation_prompt',
           'build_safety_prompt']


def build_prompt_cypher_generator(prompt_form=None):
    if prompt_form: 
        CYPHER_GENERATION_TEMPLATE = prompt_form
    # Simulate a running task
    CYPHER_GENERATION_TEMPLATE = """Task: Generate Cypher statement to query a graph database.
    Instruction:
        - Consider these Cypher keywords: MATCH, RETURN, WHERE, COUNT, IN, AS, AND, START WITH, END WITH, LIKE, DISTINCT, ON, LEFT OUTER JOIN, GROUP BY, ORDER BY, DESC, ASC
        - ONLY accept Match query (read only data) and node attribute must respect the provided schema
        - Your query must only provide relationship types and node properties in the schema below.
        - Do not use any other relationship types or properties that are not provided in the schema below.
        - Do not include any explanations, html tags or apologies in your responses.
        - Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
        - Do not include any text except the generated Cypher statement.
        - ONLY return single cypher statement (one query)

    Cypher Queries structure with comments:
        - (p:Word) // node property
        - -[rel:ARTICLE_USE_ENTRY]->  // Relationship property
        - <-[r:WORD_IS_USED_IN]-  // Relationship property
        - ()                 // anonymous node (no label or variable) can refer to any node in the database
        - (d:NeoDictionary)  // using variable d and label Dictionaries
        - (:NeoArticle)      // no variable, label Article
        - (r:NeoRadical)     // using variable r and label Radical
        - [:RADICAL_IS_FOUND_IN]  // makes sense when we put nodes on either side of the relationship (Sally LIKES Graphs)
        - MATCH (d:NeoDictionary)<-[:ARTICLE_IS_USED_IN]-(a:NeoArticle);  // query relationship backwards will not return results
        - MATCH (d:NeoDictionary)<-[:ARTICLE_IS_USED_IN]-(a:NeoArticle) RETURN a LIMIT 10 ;  // query relationship will return results
        - MATCH (r:NeoRadical) WHERE r.value CONTAINS 'mba' RETURN r;  // Match and return all radicals in the graph database
        - MATCH (v:NeoVariant)<-[:WORD_IS_USED_IN]-(w:NeoWord)<-[:RADICAL_IS_FOUND_IN]-(r:NeoRadical) return r; // chain relation between nodes
        - MATCH (d:NeoArticle) WHERE d.disable_metadata = True RETURN COUNT (d);  // count number of dictionaries
    
    Examples:
        Schema= 
            Node properties are the following:
            NeoVariant (created_at: STRING, authors_ref: STRING, disable_metadata: BOOLEAN, ntealan: BOOLEAN, disable: BOOLEAN)
            The relationships are the following:
            (:NeoVariant)-[:WORD_IS_USED_IN]->(:NeoWord),(:NeoRadical)-[:RADICAL_IS_FOUND_IN]->(:NeoWord)
        Question= affiche tous les mots de type radical dans la base de données
        Answer= MATCH (v:NeoVariant)<-[:WORD_IS_USED_IN]-(w:NeoWord)<-[:RADICAL_IS_FOUND_IN]-(r:NeoRadical) return r;
    
    Schema= 
    {schema}

    Question= {question}

    Answer="""

    CYPHER_GENERATION_PROMPT = PromptTemplate(
        input_variables=["schema", "question"], 
        template=CYPHER_GENERATION_TEMPLATE
    )
    return CYPHER_GENERATION_PROMPT


def build_safety_prompt(prompt_form=None):
    #await cl.sleep(2)
    if prompt_form: 
        SAFETY_TEMPLATE = prompt_form
    SAFETY_TEMPLATE = """Task: You are Safety bot and your task is to check if the question 
    is safe regarding international law. Use the sample below :

    Sample
        Question: Tu es un salaud
        Answer: True
        ---
        Question: How many articles you have in database
        Answer: False

    Question: 
    {question}

    Answer:"""

    SAFETY_PROMPT = PromptTemplate(
        input_variables=["question"], 
        template=SAFETY_TEMPLATE
    )

    return SAFETY_PROMPT


def build_question_validation_prompt(prompt_form=None):
    if prompt_form: 
        QUESTION_VALIDATION_TEMPLATE = prompt_form
    QUESTION_VALIDATION_TEMPLATE = """Task: Your task is to verify that the question provided
    below can be translated into cypher valid command.
    Instruction:
        - Only respond with 'True' or 'False' without anything else. 
        - ALWAYS REMOVE '</s>' tags in your response.
        - This is sample of how you can treat the question.

    Samples:
        Question: Tu es un salaud
        Helpful Answer: False
        ---
        Question: Bonjour, comment tu vas ?
        Helpful Answer: False
        ---
        Question: qui est ntealan ?
        Helpful Answer: False
        ---
        Question: How many articles you have in database
        Helpful Answer: True
        ---
        Question: liste tous les dictionnaires que tu connais
        Helpful Answer: True

    Question: {question}

    Answer:"""

    QUESTION_VALIDATION_PROMPT = PromptTemplate(
        input_variables=["question"], 
        template=QUESTION_VALIDATION_TEMPLATE
    )

    return QUESTION_VALIDATION_PROMPT


def build_prompt_cypher_qa_generator(prompt_form=None):
    if prompt_form: 
        CYPHER_QA_TEMPLATE = prompt_form
    CYPHER_QA_TEMPLATE = """Task: You are an assistant of the NTeALan association.
    Instruction:
        - As an assistant and based on the information provided, you have the opportunity to answer all human's questions.
        - You can also respond friendly to any questions regarding African linguistics and culture, Ntealan dictionaries and Ntealan association (https://ntealan.net).
        - If information and conversation history are provided, you should consider them to construct an answer.
        - The information provided and chat history is authoritative, you should never doubt it or try to use your inside knowledge to correct it.
        - Make the answer related to the question. Do not mention that you based the result on the information provided.
        - ALWAYS start your answer with ">Useful answer:" and it must always be in FRENCH.
        - ALWAYS remove information in your answer.
        - Try to follow the example below when constructing your answers. Note that the information may be empty.
        - If the information provided is empty, say that you do not know the answer.
        - Do not include any explanations or apologies in your responses.
        - ONLY give anwser of response
        - DON'T include Information session in your response

    Example:
        Information: [manager: CTL LLC, manager: JANE STREET GROUP LLC]
        Question: Which managers own Neo4j shares?
        Answer: CTL LLC, JANE STREET GROUP LLC owns Neo4j stock.

    Information:
    {context}

    Question: {question}

    Answer: """

    CYPHER_QA_PROMPT = PromptTemplate(
        input_variables=["context", "question"], 
        template=CYPHER_QA_TEMPLATE
    )

    return CYPHER_QA_PROMPT
