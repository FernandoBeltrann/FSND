import psycopg2

db_params = {
    "dbname": "example",
    "user": "postgres",
    "password": "1234",  # provide the password for the new user
    "host": "localhost",
    "port": "5432"
}

try:
    # Establish the connection
    connection = psycopg2.connect(**db_params)

except psycopg2.OperationalError as e:
    print("Error de conexion:", e)

cursor = connection.cursor()

cursor.execute('DROP TABLE IF EXISTS table2;')

cursor.execute('''
    CREATE TABLE table2(
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT False
    );
''')

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);' , (1, True))


SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'
data={
    'id':2,
    'completed': False
}
cursor.execute(SQL, data)

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);' , (3, True))


cursor.execute('SELECT * FROM table2;')

result=cursor.fetchall()
for r in result:
    print('fetch one',r)


#result=cursor.fetchmany(2)
#print('fetchmany(2)',result)

#result2=cursor.fetchone()
#print('fetchone', result2)

#result3=cursor.fetchone()
#print('fetchone', result3)


connection.commit()
connection.close()
