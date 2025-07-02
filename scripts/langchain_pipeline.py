from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import google.generativeai as genai # Importar a biblioteca Google Generative AI

GEMINI_API_KEY = "AIzaSyCz7792lmkmXc8tzZiNieJbfjZWF7uwML8" 

# Configurar a API do Gemini com sua chave
genai.configure(api_key=GEMINI_API_KEY)

# --- Verificar Modelos Disponíveis ---
print("Verificando modelos Gemini disponíveis...")
available_models = []
try:
    for m in genai.list_models():
        # Filtrar apenas os modelos que suportam a geração de conteúdo de texto
        if "generateContent" in m.supported_generation_methods:
            available_models.append(m.name)
    
    if available_models:
        print(f"Modelos Gemini disponíveis para 'generateContent': {available_models}")
        # Tentar usar um modelo mais recente e geralmente disponível
        # Priorize modelos como 'gemini-1.5-flash-latest' ou 'gemini-1.5-pro-latest'
        if "models/gemini-1.5-flash-latest" in available_models:
            SELECTED_GEMINI_MODEL = "gemini-1.5-flash-latest"
        elif "models/gemini-1.5-pro-latest" in available_models:
            SELECTED_GEMINI_MODEL = "models/gemini-1.5-pro-latest"
        elif "models/gemini-pro" in available_models:
            SELECTED_GEMINI_MODEL = "gemini-pro" # Fallback para gemini-pro se os 1.5 não estiverem
        else:
            print("Nenhum dos modelos preferidos (gemini-1.5-flash-latest, gemini-1.5-pro-latest, gemini-pro) encontrado.")
            print("Por favor, selecione um modelo da lista acima e atualize o código.")
            exit() # Sair se nenhum modelo adequado for encontrado
        print(f"Usando o modelo: {SELECTED_GEMINI_MODEL}")
    else:
        print("Nenhum modelo Gemini que suporte 'generateContent' foi encontrado com sua chave de API.")
        print("Verifique sua chave de API e as permissões no Google AI Studio.")
        exit() # Sair se nenhum modelo for encontrado
except Exception as e:
    print(f"Erro ao listar modelos Gemini: {e}")
    print("Por favor, verifique sua conexão com a internet e sua chave de API do Gemini.")
    exit()

# Initialize Neo4j connection
graph = Neo4jGraph(
    url="bolt://34.201.37.122:7687",
    username="neo4j",
    password="survivals-check-revolutions"
)

# Initialize LLM com o modelo Gemini selecionado
llm = ChatGoogleGenerativeAI(model=SELECTED_GEMINI_MODEL, temperature=0, google_api_key=GEMINI_API_KEY)

# Create LangChain pipeline with Cypher chain
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    return_intermediate_steps=True,
    allow_dangerous_requests=True
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
    # Usando .invoke() conforme recomendado pelo aviso de depreciação
    result = chain.invoke({"query": query}) 
    print(f"Response: {result}")
