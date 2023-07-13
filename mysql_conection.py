from mysql.connector import connect, Error


def initiate_connection(user="root", password="Aditya@1", database="covid19"):
    mycon = connect(host="localhost", user=user, password=password, database=database)
    mycur = mycon.cursor()
    return mycon, mycur


def insert_data(mycon, query, val):
    try:
        cursor = mycon.cursor()
        cursor.execute(query, val)
        mycon.commit()
        return 0
    except Error as e:
        print(e)
        return 1


def create_table(mycon, query):
    try:
        cursor = mycon.cursor()
        cursor.execute(query)
        mycon.commit()
        return 0
    except Error as e:
        print(e)
        return 1


def select_data(mycon, query):
    try:
        cursor = mycon.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(e)
        return 1


def update_data(mycon, query, val):
    try:
        cursor = mycon.cursor()
        cursor.execute(query, val)
        mycon.commit()
        return 0
    except Error as e:
        print(e)
        return 1


def delete_data(mycon, query, val):
    try:
        cursor = mycon.cursor()
        cursor.execute(query, val)
        mycon.commit()
        return 0
    except Error as e:
        print(e)
        return 1


def close_connection(mycon):
    mycon.close()
