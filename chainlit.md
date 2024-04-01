## NTeALan GTP African language dictionaries

This tool is use to experiment how we can use generate IA for 
enhance search capability in a lexicographic graph database build
with neo4j.

This interface is used to test on sample of NTeALan lexicographic data.  

## 1 - How this work ?

For each question asked, we need to :

- check if the question needs to be translated as cypher query
    - if question can be translated, translate it with llm cypher endpoint
    - otherwise, send it to llm endpoint 
- check if generated cypher command is safe and match requirements context
    - if cypher command if safe, send it to the next chain
    - if not safe, throw error message
- restrict the context node properties to the neo4j node found in command
- compress the final context prompt 
- get final response


## 2 - Contributions

You can contribute to the project on Github

Please follow this link : 