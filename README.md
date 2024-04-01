<p align="center">
    <br><br><br>
    <a href="https://github.com/NTeALan/Genaiti"><img src="" alt="Genaiti" width="150px"/></a>
    <br><br><br>
</p>
<p align="center">
    <b style="color:#D84727; font-size:30px">Genaiti</b>
</p>
<p align="center">
    <span>This tool is use to experiment how we can use generate IA to enhance search capabilities in a african lexicographic graph database build with Neo4j.</span><br>
    <p align="center">Project from <b>NTeALan Research and Development</b></p>
</p>

<p align="center">
    <a href="http://creativecommons.org/licenses/by/4.0/"><img src="https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg" alt="creativecommons" width="110px">
    <p>
    <b>Security note</b>: 
    Make sure that the database connection uses credentials
    that are narrowly-scoped to only include necessary permissions.
    Failure to do so may result in data corruption or loss, since the calling code may attempt commands that would result in deletion, mutation of data if appropriately prompted or reading sensitive data if such data is present in the database.
    The best way to guard against such negative outcomes is to (as appropriate) limit the permissions granted to the credentials used with this tool. 
    See https://python.langchain.com/docs/security for more information.
    </p>
</p>

<p align="center"> 
    <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"/>      
    <img src="https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white" alt="Git"/>            
</p>

[![Code style: ntealan](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# NTeALan Contexte

NTeAlan project aims to provide lexical, cultural and tools for under-resource african languages.

NTeALan has builded 5 years ago many lexicographic resources and tools for african languages.

- Resources are hosted and shared in : `https://apis.ntealan.net`
- Collaborative dictionaries is hosted in : `https://www.ntealan.net`


# Problem behind this package 

NTeALan want to switch relational to graph representation of its lexicographic database. Because the 
structure of its dictionaries are more complex to build, use default cypher command can be so complex
for non expert. The evidence is that, query large graph knowledge is very hard to understand and transpose to Neo4j Cypher command.

We want to explore the advantage of generate AI in other to simplify neo4j graph query for our database
purpose. 


This Python package, build with `langchain` and `chainlit`, is used to demonstrate an simple implementation to resolve this problem. 


This project can be apply to other type of neo4j database.


# Installation

This project use `poetry` python package.

## prerequis

This project use these necessary tools :

- docker
- docker-compose
- neo4j data (dictionaries or anyone else)

## Local environment

Follow these steps to install your developpement environment

1- clone this repository

```bash

git clone https://github.com/genai_graph_dictionary
cd genai_graph_dictionary

```

2- install dependencies and connect to the dev environment

```bash

poetry install
poetry shell

```

3- update env file `.env.sample` with your own configuration and rename it

```bash

mv .env.sample .env

```

4- start graph db with docker compose (make sure it is installed)

```bash

docker-compose up

```

5- start chainlit app

```bash

chainlit run ntealan_llm_chainlit.py

```

6- start chainlit copilot app


```bash

chainlit run ntealan_llm_chainlit_copilot.py

open src/integration/copilot_chainlit.html

```

## Install with Docker

```bash

docker build -t genaiti:latest .
docker-compose up

```



# Update prompt

Prompte are located at `src/genaiti/prompts_template.py`


# Contributions

You can contribute to the project on this Github repository.