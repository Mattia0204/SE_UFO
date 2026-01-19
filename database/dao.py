from database.DB_connect import DBConnect
from model.sighting import Sighting
from model.state import State

class DAO:
    @staticmethod
    def get_all_sightings():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM sighting  
                ORDER BY s_datetime 
                """
        cursor.execute(query)
        for row in cursor:
            result.append(Sighting(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_states():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM state """

        cursor.execute(query)

        for row in cursor:
                result.append(State(row["id"], row["name"], row["capital"],
                                    row["lat"], row["lng"], row["area"],
                                    row["population"], row["neighbors"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_neighbors():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                        SELECT state1, state2
                        FROM neighbor  
                        """
        cursor.execute(query)
        for row in cursor:
            result.append((row['state1'], row['state2']))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_weight(year, shape):
        conn = DBConnect.get_connection()
        result = {}
        cursor = conn.cursor(dictionary=True)
        query = """
                    select s.state, count(id) as peso
                    from sighting s 
                    where YEAR(s.s_datetime) = %s and s.shape = %s 
                    group by s.state 
                        """
        cursor.execute(query,(year,shape))
        for row in cursor:
            result[row['state']] = row['peso']
        cursor.close()
        conn.close()
        return result