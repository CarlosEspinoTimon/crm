import sys
import pymysql
from werkzeug.security import generate_password_hash


def create_user(email, password):
    try:
        connection = pymysql.connect(
            host='db',
            database='app_db',
            user='user',
            password='password'
        )
        cursor = connection.cursor()

        password_hash = generate_password_hash(password)

        sql_statement = """INSERT INTO users (email, password_hash)
                            VALUES (%s, %s)"""

        record = (email, password_hash)
        cursor.execute(sql_statement, record)
        connection.commit()
        print("Record inserted")
    except Exception as error:
        print("Failed to insert with error: {}".format(error))


if __name__ == '__main__':
    create_user(sys.argv[1], sys.argv[2])
