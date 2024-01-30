import psycopg2


def get_database_connection():
    return psycopg2.connect(
        host="localhost",
        database="gaildorf_goals",
        user="ronny",
        password="ronny"
    )
