from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://34.201.37.122:7687", auth=("neo4j", "survivals-check-revolutions"))

try:
       driver.verify_connectivity()
       print("Connection successful!")
except Exception as e:
       print(f"Connection failed: {e}")
driver.close()