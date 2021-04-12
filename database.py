import sqlite3

try:
    sqliteConnection = sqlite3.connect('database.db')
    cursor = sqliteConnection.cursor()
    print("Succesfuldt forbundet til databasen")

    sqlite_select_Query = "Select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("Sqlite version is: ", record)
    cursor.close

except sqlite3.Error as error:
    print("Error occurred while conecting to sqlite", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQlite connection is closed")