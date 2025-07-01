from langchain.llms import OpenAI
from langchain.chains import Neo4jGraphChain
from neo4j import GraphDatabase
import os

# Config OpenAI
os.environ["OPENAI_API_KEY"] = "sua_openai_api_key"  # coloque sua chave aqui

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "senha"))  # ajuste a senha

llm = OpenAI(temperature=0)
chain = Neo4jGraphChain(llm=llm, neo4j_driver=driver, verbose=True)

def consulta_langchain(pergunta: str):
    resposta = chain.run(pergunta)
    return resposta

if __name__ == "__main__":
    perguntas = [
        "Quem são os aliados de Luke Skywalker?",
        "Quais planetas aparecem no filme A New Hope?",
        "Quais personagens pertencem à Aliança Rebelde?"
    ]
    for p in perguntas:
        print(f"Pergunta: {p}")
        print(f"Resposta: {consulta_langchain(p)}")
        print("-" * 20)
