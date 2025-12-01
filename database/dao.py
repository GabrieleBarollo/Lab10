from database.DB_connect import DBConnect
from model.hub import Hub


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """
    # TODO
    @staticmethod
    def get_primi_risultati():
        risultati = []
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT id_hub_origine, id_hub_destinazione, SUM(valore_merce) AS valore_merce_tot, COUNT(*) AS num_spedizioni 
                    FROM spedizione
                    GROUP BY id_hub_origine, id_hub_destinazione"""
        cursor.execute(query)
        for row in cursor:
            #print(row)
            risultati.append({'id_hub_origine': row['id_hub_origine'],
                              "id_hub_destinazione": row['id_hub_destinazione'],
                              "valore_merce_tot": row['valore_merce_tot'],
                              "num_spedizioni": row['num_spedizioni']})
        cursor.close()
        cnx.close()
        return risultati

    @staticmethod
    def get_hubs():
        risultati = {}
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT *
                    FROM hub"""

        cursor.execute(query)
        for row in cursor:
            h = Hub(row["id"], row["codice"], row["nome"], row["citta"], row["stato"], row["latitudine"], row["longitudine"])
            risultati[row["id"]] = h

        cursor.close()
        cnx.close()
        return risultati

