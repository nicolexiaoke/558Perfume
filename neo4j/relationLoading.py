from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import pandas as pd

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def add_relations(self, sameAs_sourcefile, haveSimilarPrices_sourcefile, haveSimilarScents_sourcefile):
        with self.driver.session(database="neo4j") as session:
            sameAs_result = session.execute_write(
                self._add_relation, sameAs_sourcefile, 'sameAs')
            haveSimilarPrices_result = session.execute_write(
                self._add_relation, haveSimilarPrices_sourcefile, 'haveSimilarPrices')
            haveSimilarScents_result = session.execute_write(
                self._add_relation, haveSimilarScents_sourcefile, 'haveSimilarScents')


    @staticmethod
    def _add_relation(tx, sourcefile, relation_type):
        source_df = pd.read_csv(sourcefile, index_col=0)
        # print(source_df)
        rel_num = len(source_df)
        # print(rel_num)
        
        for i in range(rel_num):
            node_id1 = source_df.at[i ,'node_id1']
            node_id2 = source_df.at[i, 'node_id2']

            query = (
                "MATCH\
                        (a:Perfume),\
                        (b:Perfume)\
                    WHERE a.node_id = $node_id1 AND b.node_id = $node_id2\
                    CREATE (a)-[r:"+ relation_type +"]->(b)\
                    RETURN type(r)"\
            )
            result = tx.run(query, node_id1=node_id1, node_id2=node_id2)

            if i % 1000 == 0:
                print(i,'/',rel_num, ': ', node_id1, node_id2)
                for row in result:
                    print(row)
            # break




if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "bolt" URI scheme
    uri = "bolt://localhost:11003"
    user = "neo4j"
    password = "Perfume_tmp"
    app = App(uri, user, password)
    dir = '../data/entity_linking/'
    sameAs_sourcefile = dir+'sameAs_TRUE_predictions.csv'
    haveSimilarPrices_sourcefile = dir+'haveSimilarPrices_TRUE_predictions.csv'
    haveSimilarScents_sourcefile = dir+'haveSimilarScents_TRUE_predictions.csv'
    app.add_relations(sameAs_sourcefile, haveSimilarPrices_sourcefile, haveSimilarScents_sourcefile)
    app.close()