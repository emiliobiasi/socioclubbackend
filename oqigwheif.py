import psycopg2

connection = psycopg2.connect(
            host='localhost',
            port=5431,
            database='socioclub',
            user='socioclub',
            password='socioclub'
        )

if connection:
    cursor = connection.cursor()
    cursor.execute('select * from stripe')

    data = cursor.fetchall()

    for d in data:
        print(d)
    connection.commit()
    cursor.close()
    connection.close()