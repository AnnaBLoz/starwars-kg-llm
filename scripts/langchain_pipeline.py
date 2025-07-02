from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI
import os

# Set OpenAI API key (replace with your own or use environment variable)
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Initialize Neo4j connection
graph = Neo4jGraph(
    url="bolt://34.201.37.122:7687",
    username="neo4j",
    password="survivals-check-revolutions"
)

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create LangChain pipeline with Cypher chain
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    return_intermediate_steps=True
)

# Example queries
queries = [
    "Who is the father of Luke Skywalker?",
    "Which characters are affiliated with the Rebel Alliance?",
    "What events occurred on Endor?",
    "Which ships were used in the Battle of Yavin?",
    "Who uses lightsabers in Star Wars?"
]

# Run queries and print results
for query in queries:
    print(f"\nQuery: {query}")
    result = chain.run(query)
    print(f"Response: {result}")