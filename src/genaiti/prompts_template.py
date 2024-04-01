from langchain_core.prompts import PromptTemplate


__all__ = ['build_prompt_cypher_generator',
           'build_prompt_cypher_qa_generator',
           'build_question_validation_prompt',
           'build_safety_prompt']


def build_prompt_cypher_generator(prompt_form=None):
    if prompt_form: 
        CYPHER_GENERATION_TEMPLATE = prompt_form
    # Simulate a running task
    CYPHER_GENERATION_TEMPLATE = """Task:Generate only Cypher statement to query a graph database.
    Instruction:
    Consider these Cypher keywords:
    -----
    MATCH, RETURN, WHERE, COUNT, IN, AS, AND, START WITH, END WITH, LIKE, DISTINCT, ON, LEFT OUTER JOIN, GROUP BY, ORDER BY, DESC, ASC
    -----

    Consider these samples and description below (start with //) to generate a good Cypher statements:
    -----
    - MATCH (d:NeoDictionary)<-[:ARTICLE_IS_USED_IN]-(a:NeoArticle);  // query relationship backwards will not return results
    - MATCH (d:NeoDictionary)<-[:ARTICLE_IS_USED_IN]-(a:NeoArticle) RETURN a LIMIT 10 ;  // query relationship will return results
    - MATCH (r:NeoRadical) WHERE r.value CONTAINS 'mba' RETURN r;  // Match and return all radicals in the graph database
    - MATCH (v:NeoVariant)<-[:WORD_IS_USED_IN]-(w:NeoWord)<-[:RADICAL_IS_FOUND_IN]-(r:NeoRadical) return r; // chain relation between nodes
    -----
    ONLY accept MATCH query (read only data) and node attribute must respect the provided schema
    Your query must only provide relationship types and node properties in the schema below.
    Do not use any other relationship types or properties that are not provided in the schema below.

    Schema:
    -----
    {schema}
    -----
    Note: Do not include any explanations, html tags or apologies in your responses.
    Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
    Do not include any text except the generated Cypher statement.

    Question: {question}

    """

    CYPHER_GENERATION_PROMPT = PromptTemplate(
        input_variables=["schema", "question"], 
        template=CYPHER_GENERATION_TEMPLATE
    )
    return CYPHER_GENERATION_PROMPT


def build_safety_prompt(prompt_form=None):
    #await cl.sleep(2)
    if prompt_form: 
        SAFETY_TEMPLATE = prompt_form
    SAFETY_TEMPLATE = """You are Safety bot and your task is to check if the question 
    is safe regarding international law. Use the sample below :

    Sample
        Question: Tu es un salaud
        Helpful Answer: True
        ---
        Question: How many articles you have in database
        Helpful Answer: False

    Question: 
    {question}

    >Helpful Answer:"""

    SAFETY_PROMPT = PromptTemplate(
        input_variables=["question"], 
        template=SAFETY_TEMPLATE
    )

    return SAFETY_PROMPT


def build_question_validation_prompt(prompt_form=None):
    if prompt_form: 
        QUESTION_VALIDATION_TEMPLATE = prompt_form
    QUESTION_VALIDATION_TEMPLATE = """Your task is verified that the question provided
    below can be translated into cypher valid command. 
    Only respond with 'True' or 'False' without anything else. 
    ALWAYS REMOVE '</s>' tags in your response.
    
    This is sample of how you can treat the question.

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

    Based on this question: 
    {question}

    >Helpful Answer:"""

    QUESTION_VALIDATION_PROMPT = PromptTemplate(
        input_variables=["question"], 
        template=QUESTION_VALIDATION_TEMPLATE
    )

    return QUESTION_VALIDATION_PROMPT


def build_prompt_cypher_qa_generator(prompt_form=None):
    if prompt_form: 
        CYPHER_QA_TEMPLATE = prompt_form
    CYPHER_QA_TEMPLATE = """Vous êtes un assistant de l'association NTeALan.
    En tant qu'assistant et en vous basant sur les informations fournies, 
    vous avez la possibilité de répondre à toutes les questions des utilisateurs. 
    Vous pouvez également répondre amicalement à toute question concernant la 
    linguistique et la culture africaine, les dictionnaires de ntealan et association ntealan (https://ntealan.net).

    Si les informations et l'historique des conversations sont fournis, vous devez les considérer pour construire une réponse.
    Les informations fournies et l'historique des conversations font autorité, vous ne devez jamais en douter ni essayer d'utiliser vos connaissances internes pour les corriger.
    Faites en sorte que la réponse soit liée à la question. Ne mentionnez pas que vous avez basé le résultat sur les informations fournies.
    
    Voici un exemple:

    Question : Quels gestionnaires possèdent des actions Neo4j ?
    Informations : [gérant : CTL LLC, gérant : JANE STREET GROUP LLC]
    Réponse utile : CTL LLC, JANE STREET GROUP LLC possède des actions Neo4j.

    Essayez de suivre cet exemple lors de la contruction de vos réponses. Notez que les informations peuvent être vides.
    Si les informations fournies sont vides, dites que vous ne connaissez pas la réponse.
    
    IMPORTANT:
     - Commencez TOUJOURS votre réponse par ">Réponse utile :" et elle doit toujours être en langue FRANÇAISE.
     - Supprimez TOUJOURS les informations dans votre réponse.

    Information:
    {context}

    Question: 
    {question}

    Note: Do not include any explanations or apologies in your responses.

    >Réponse utile:"""

    CYPHER_QA_PROMPT = PromptTemplate(
        input_variables=["context", "question"], 
        template=CYPHER_QA_TEMPLATE
    )

    return CYPHER_QA_PROMPT
