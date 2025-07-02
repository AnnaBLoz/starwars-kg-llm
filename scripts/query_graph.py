from neo4j import GraphDatabase

class Neo4jQuery:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query_jedi_rebels(self):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (p:Personagem)-[:AFILIADO_A]->(f:Faccao {nome: 'Aliança Rebelde'})
                WHERE 'Jedi' IN p.papeis
                RETURN p.nome
                """
            )
            return [record["p.nome"] for record in result]

    def query_events_on_planet(self, planet_name):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (e:Evento)-[:OCORREU_EM]->(p:Planeta {nome: $planet_name})
                RETURN e.nome
                """,
                planet_name=planet_name
            )
            return [record["e.nome"] for record in result]

    def query_father_of(self, character_name):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (p:Personagem)-[:PAI_DE]->(c:Personagem {nome: $character_name})
                RETURN p.nome
                """,
                character_name=character_name
            )
            return [record["p.nome"] for record in result]

if __name__ == "__main__":
    query = Neo4jQuery("bolt://34.201.37.122:7687", "neo4j", "survivals-check-revolutions")
    print("Jedi da Aliança Rebelde:", query.query_jedi_rebels())
    print("Eventos em Endor:", query.query_events_on_planet("Endor"))
    print("Pai de Luke Skywalker:", query.query_father_of("Luke Skywalker"))
    query.close()