# Star Wars Knowledge Graph for LLM

This project implements a Knowledge Graph for the Star Wars universe using Neo4j, integrated with LangChain and an LLM (OpenAI GPT-4) for natural language queries. The graph models entities like characters, planets, factions, events, ships, and technologies, with relationships to enable rich queries.

## Setup
1. **Install Neo4j**:
   - Download and install Neo4j Desktop (https://neo4j.com/download/) or use Neo4j Sandbox (https://sandbox.neo4j.com).
   - Set up a local database with URI `bolt://localhost:7687`, username `neo4j`, and password `password`.

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set OpenAI API key**:
   - Replace `your-openai-api-key` in `scripts/langchain_pipeline.py` with your OpenAI API key or set it as an environment variable:
     ```bash
     export OPENAI_API_KEY="your-openai-api-key"
     ```

## Running the Project
1. **Import Data**:
   ```bash
   python scripts/import_data.py
   ```
   This populates the Neo4j database with data from the `data/` directory.

2. **Query the Graph Directly**:
   ```bash
   python scripts/query_graph.py
   ```
   This runs predefined Cypher queries to test the graph.

3. **Run LangChain Pipeline**:
   ```bash
   python scripts/langchain_pipeline.py
   ```
   This executes natural language queries using LangChain and the LLM.

## Data Sources
- **SWAPI** (https://swapi.dev): Structured data for characters, planets, and ships.
- **Wookieepedia** (https://starwars.fandom.com): Manual data for events and technologies.

## Example Queries
- "Who is the father of Luke Skywalker?"
- "Which characters are affiliated with the Rebel Alliance?"
- "What events occurred on Endor?"

## Hallucination Prevention
The Neo4j graph ensures responses are grounded in validated data, and LangChain's RAG retrieves facts directly from the graph, preventing LLM hallucinations.

## Project Structure
- `data/`: CSV files with Star Wars data.
- `scripts/`: Python scripts for data import, querying, and LangChain integration.
- `requirements.txt`: Python dependencies.
- `README.md`: This file.

## Team
- Anna Beatriz Loz, Pablo Lopes, Matheus Lofy e Lucas Gadonski

## License
MIT License