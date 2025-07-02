from neo4j import GraphDatabase
import pandas as pd
import os

class Neo4jImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def import_personagens(self, csv_path):
        with self.driver.session() as session:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (p:Personagem {nome: $nome})
                    SET p.especie = $especie, p.papeis = $papeis
                    MERGE (pl:Planeta {nome: $planeta_natal})
                    MERGE (p)-[:NASCEU_EM]->(pl)
                    """,
                    nome=row['nome'],
                    especie=row['especie'],
                    planeta_natal=row['planeta_natal'],
                    papeis=row['papeis'].split(',')
                )

    def import_planetas(self, csv_path):
        with self.driver.session() as session:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (p:Planeta {nome: $nome})
                    SET p.clima = $clima, p.localizacao = $localizacao
                    """,
                    nome=row['nome'],
                    clima=row['clima'],
                    localizacao=row['localizacao']
                )

    def import_faccoes(self, csv_path):
        with self.driver.session() as session:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (f:Faccao {nome: $nome})
                    SET f.tipo = $tipo, f.lider = $lider
                    """,
                    nome=row['nome'],
                    tipo=row['tipo'],
                    lider=row['lider']
                )

    def import_eventos(self, csv_path):
        with self.driver.session() as session:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (e:Evento {nome: $nome})
                    SET e.ano = $ano, e.descricao = $descricao
                    MERGE (p:Planeta {nome: $planeta})
                    MERGE (e)-[:OCORREU_EM]->(p)
                    """,
                    nome=row['nome'],
                    ano=row['ano'],
                    descricao=row['descricao'],
                    planeta=row['planeta']
                )

    def import_naves(self, csv_path):
        with self.driver.session() as session:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (n:Nave {nome: $nome})
                    SET n.tipo = $tipo
                    MERGE (f:Faccao {nome: $faccao})
                    MERGE (n)-[:PERTENCE_A]->(f)
                    """,
                    nome=row['nome'],
                    tipo=row['tipo'],
                    faccao=row['faccao']
                )

    def import_tecnologias(self, csv_path):
        with self.driver.session() as session:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                session.run(
                    """
                    MERGE (t:Tecnologia {nome: $nome})
                    SET t.tipo = $tipo
                    MERGE (p:Personagem {nome: $usuario})
                    MERGE (p)-[:USA]->(t)
                    """,
                    nome=row['nome'],
                    tipo=row['tipo'],
                    usuario=row['usuario']
                )

    def import_relacionamentos_adicionais(self):
        with self.driver.session() as session:
            # Exemplo: Relacionamentos adicionais
            session.run(
                """
                MATCH (p:Personagem {nome: 'Luke Skywalker'}), (f:Faccao {nome: 'Aliança Rebelde'})
                MERGE (p)-[:AFILIADO_A]->(f)
                """
            )
            session.run(
                """
                MATCH (p:Personagem {nome: 'Darth Vader'}), (f:Faccao {nome: 'Império Galáctico'})
                MERGE (p)-[:AFILIADO_A]->(f)
                """
            )
            session.run(
                """
                MATCH (p:Personagem {nome: 'Luke Skywalker'}), (e:Evento {nome: 'Batalha de Yavin'})
                MERGE (p)-[:PARTICIPOU]->(e)
                """
            )
            session.run(
                """
                MATCH (p:Personagem {nome: 'Han Solo'}), (n:Nave {nome: 'Millennium Falcon'})
                MERGE (p)-[:PILOTA]->(n)
                """
            )
            session.run(
                """
                MATCH (p:Personagem {nome: 'Darth Vader'}), (l:Personagem {nome: 'Luke Skywalker'})
                MERGE (p)-[:PAI_DE]->(l)
                """
            )

if __name__ == "__main__":
    importer = Neo4jImporter("bolt://34.201.37.122:7687", "neo4j", "survivals-check-revolutions")
    importer.clear_database()  # Clear database before importing
    importer.import_personagens("data/personagens.csv")
    importer.import_planetas("data/planetas.csv")
    importer.import_faccoes("data/faccoes.csv")
    importer.import_eventos("data/eventos.csv")
    importer.import_naves("data/naves.csv")
    importer.import_tecnologias("data/tecnologias.csv")
    importer.import_relacionamentos_adicionais()
    importer.close()