from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "senha"  # Altere para sua senha

driver = GraphDatabase.driver(uri, auth=(user, password))

def create_nodes(tx):
    characters = [
        {"name": "Luke Skywalker", "species": "Human", "gender": "Male", "description": "Jedi Knight"},
        {"name": "Darth Vader", "species": "Human", "gender": "Male", "description": "Sith Lord"},
        {"name": "Leia Organa", "species": "Human", "gender": "Female", "description": "Princess and Rebel Leader"}
    ]
    planets = [
        {"name": "Tatooine", "system": "Tatoo", "description": "Desert planet"},
        {"name": "Alderaan", "system": "Alderaan", "description": "Destroyed planet"}
    ]
    films = [
        {"title": "A New Hope", "episode": 4, "year": 1977, "description": "Star Wars Episode IV"},
        {"title": "The Empire Strikes Back", "episode": 5, "year": 1980, "description": "Star Wars Episode V"}
    ]
    organizations = [
        {"name": "Rebel Alliance", "type": "Rebellion", "description": "Fighting the Empire"},
        {"name": "Galactic Empire", "type": "Empire", "description": "Ruling government"}
    ]

    for c in characters:
        tx.run("CREATE (c:Character {name: $name, species: $species, gender: $gender, description: $description})", **c)
    for p in planets:
        tx.run("CREATE (p:Planet {name: $name, system: $system, description: $description})", **p)
    for f in films:
        tx.run("CREATE (f:Film {title: $title, episode: $episode, year: $year, description: $description})", **f)
    for o in organizations:
        tx.run("CREATE (o:Organization {name: $name, type: $type, description: $description})", **o)

def create_relationships(tx):
    born_on = [
        ("Luke Skywalker", "Tatooine"),
        ("Leia Organa", "Alderaan")
    ]
    for char, planet in born_on:
        tx.run("""
            MATCH (c:Character {name: $char}), (p:Planet {name: $planet})
            CREATE (c)-[:BORN_ON]->(p)
        """, char=char, planet=planet)

    member_of = [
        ("Luke Skywalker", "Rebel Alliance"),
        ("Leia Organa", "Rebel Alliance"),
        ("Darth Vader", "Galactic Empire")
    ]
    for char, org in member_of:
        tx.run("""
            MATCH (c:Character {name: $char}), (o:Organization {name: $org})
            CREATE (c)-[:MEMBER_OF]->(o)
        """, char=char, org=org)

    appears_in = [
        ("Luke Skywalker", "A New Hope"),
        ("Darth Vader", "A New Hope"),
        ("Leia Organa", "A New Hope"),
        ("Luke Skywalker", "The Empire Strikes Back")
    ]
    for char, film in appears_in:
        tx.run("""
            MATCH (c:Character {name: $char}), (f:Film {title: $film})
            CREATE (c)-[:APPEARS_IN]->(f)
        """, char=char, film=film)

    allied_with = [
        ("Luke Skywalker", "Leia Organa")
    ]
    for c1, c2 in allied_with:
        tx.run("""
            MATCH (a:Character {name: $c1}), (b:Character {name: $c2})
            CREATE (a)-[:ALLIED_WITH]->(b)
        """, c1=c1, c2=c2)

if __name__ == "__main__":
    with driver.session() as session:
        session.write_transaction(create_nodes)
        session.write_transaction(create_relationships)
    print("Dados importados com sucesso.")
