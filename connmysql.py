import pymysql

def conn_mysql():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='123456',
        database='musiclist'
    )

    return conn

def close_conn(conn):
    if conn:
        conn.close()


