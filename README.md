# Star Wars Knowledge Graph + Langchain + LLM

## Desafio Técnico - Knowledge Graph para LLM

### Tema
Universo Star Wars: Personagens, Planetas, Filmes, Organizações e suas relações.

### Tecnologias
- Neo4j (graph database)
- Python (orquestração)
- Langchain + OpenAI API para consultas em linguagem natural

### Como usar

1. Instale as dependências:
```
pip install -r requirements.txt
```

2. Configure o Neo4j (default: bolt://localhost:7687, usuário 'neo4j', senha 'senha')

3. Configure sua chave OpenAI na variável ambiente `OPENAI_API_KEY`.

4. Execute o script de importação para popular o grafo:
```
python import_data.py
```

5. Execute o script de consulta via LLM:
```
python query_llm.py
```

### Exemplos de perguntas
- Quem são os aliados de Luke Skywalker?
- Quais planetas aparecem no filme A New Hope?
- Quais personagens pertencem à Aliança Rebelde?

---

## Autor
Equipe: Anna Beatriz Loz
