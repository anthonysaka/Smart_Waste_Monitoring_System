import psycopg2

class Connectiondb():
    def  getConnectionToPostgre():

        try:
            connection = psycopg2.connect(user = "anthonysaka",
                                        password = "nose@postgres",
                                        host = "127.0.0.1",
                                        port = "5432",
                                        database = "gomibako")
           
            print("conectado a la db con exito")
          #  print ( connection.get_dsn_parameters(),"\n")
        
        except (Exception, psycopg2.DatabaseError) as error :
            print ("Error while connecting to PostgreSQL", error)
        finally:
            return connection #return database connection
            