from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    


    '''---------------------------------------------below: demo data import---------------------------------------------'''   
    '''|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'''   
    def create_perfume(self):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self._create_and_return_perfume)

            print(result)
            # for row in result:
            #     print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_perfume(tx):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (n1:Perfume { node_id: '1', url: 'https://www.fragrancenet.com/cologne/calvin-klein/escape/edt#122757' ,name: 'Escape', size: '1.7 oz', smell: 'floral', price: 31.99, rating: 4.5, comments:['I love Calvin Klein escape. Problem is I ordered it February 22 and its still not here. I had a second order and it already came. Love the prices, discounts, and convenience.'] }) "
            "CREATE (n2:Perfume { node_id: '2', url: 'https://www.fragrancenet.com/cologne/calvin-klein/escape/edt#122757' ,name: 'Escape', size: '2.4 oz', smell: 'Floral', price: 50, rating: 4.8, comments:['One of my all time favorites! Great in ant season…', 'Good!']}) "
            "CREATE (n3:Perfume { node_id: '3', url: 'https://www.fragrancenet.com/cologne/coach/coach-platinum/eau-de-parfum#314403' ,name: 'Coach Platinum', size: '2 oz', smell: 'sexy', price: 54.99, rating: 4.9, comments:['A++ This… is a very nice fragrance. It s calm, soft, soothing, ugh it s just beautiful. If you want something crowd pleasing & that s not overwhelming give this a try. Can be worn year round night/ day & doesn t offend anyone. It s such a sexy & classy scent. I smelled this on paper & immediately knew I was GOING to buy the 100ML. The smell is like a soft kinda sweet powder, you definitely get that tonka bean & sandalwood with a hint of leather in the background to keep a manly tone. Next to PDM Layton, this is my second favorite Cologne. It s just sooo nice!! Highly recommended']}) "

            # "CREATE (n4:DeliveryOption {node_id: '4',description:'FedEx'}) "
            # "CREATE (n5:DeliveryOption {node_id: '5',description:'UPS'}) "
            
            "CREATE (n6:SellingPlatform {node_id: '6',name:'fragrancenet', has_offline_store:'no'}) "
            "CREATE (n7:SellingPlatform {node_id: '7',name:'amazon', has_offline_store:'no'}) "
            
            "CREATE (n8:Brand {node_id: '8',name:'calvin klein'}) "
            "CREATE (n9:Brand {node_id: '9',name:'coach'}) "

            #relationships
            #intra perfume relations
            "CREATE (n1)-[:sameAs]->(n2)" 
            "CREATE (n2)-[:sameAs]->(n1)" 
            "CREATE (n1)-[:haveSimilarPrices]->(n2)" 
            "CREATE (n2)-[:haveSimilarPrices]->(n1)" 
            "CREATE (n1)-[:haveSimilarScents]->(n2)" 
            "CREATE (n2)-[:haveSimilarScents]->(n1)" 

            # #delivery
            # "CREATE (n1)-[:deliverBy]->(n4) "
            # "CREATE (n1)-[:deliverBy]->(n5) "
            # "CREATE (n2)-[:deliverBy]->(n4) "
            # "CREATE (n2)-[:deliverBy]->(n5) "
            # "CREATE (n3)-[:deliverBy]->(n4) "
            
            #selling platforms
            "CREATE (n1)-[:listedOn]->(n6) "
            "CREATE (n2)-[:listedOn]->(n7) "
            "CREATE (n3)-[:listedOn]->(n6) "
            
            #brand
            "CREATE (n1)-[:productOf]->(n8) "
            "CREATE (n2)-[:productOf]->(n8) "
            "CREATE (n3)-[:productOf]->(n9) "

            # #provide delivery
            # "CREATE (n6)-[:provideDelivery]->(n4) "
            # "CREATE (n6)-[:provideDelivery]->(n5) "
            # "CREATE (n7)-[:provideDelivery]->(n4) "
            # "CREATE (n7)-[:provideDelivery]->(n5) "

            "RETURN n1, n2, n3, n6, n7, n8, n9"
        )
        result = tx.run(query)
        for row in result:
            print(row)

        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


    '''|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||'''   
    '''------------------------------------------above: demo data import--------------------------------------------------'''   
 
    
    def create_friendship(self, person1_name, person2_name):
        with self.driver.session(database="neo4j") as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.execute_write(
                self._create_and_return_friendship, person1_name, person2_name)
            for row in result:
                print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        
        # print(result)
        print(type(result))
        for row in result:
            print(row)

        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


    def find_person(self, person_name):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_read(self._find_and_return_person, person_name)
            for row in result:
                print("Found person: {row}".format(row=row))

    @staticmethod
    def _find_and_return_person(tx, person_name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $person_name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, person_name=person_name)
        return [row["name"] for row in result]


# if __name__ == "__main__":
#     # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
#     uri = "neo4j+s://36d638c4.databases.neo4j.io"
#     user = "neo4j"
#     password = "1McmE-lDtVUMYBPUFsiQKscrqbD4M58Oc1hJOcKulcM"
#     app = App(uri, user, password)
#     app.create_friendship("Alice", "David")
#     app.find_person("Alice")
#     app.close()

# if __name__ == "__main__":
#     # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
#     uri = "neo4j+s://36d638c4.databases.neo4j.io"
#     user = "neo4j"
#     password = "1McmE-lDtVUMYBPUFsiQKscrqbD4M58Oc1hJOcKulcM"
#     app = App(uri, user, password)
#     app.create_perfume()
#     app.close()

if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "bolt" URI scheme
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "perfumeKG"
    app = App(uri, user, password)
    app.create_perfume()
    app.close()