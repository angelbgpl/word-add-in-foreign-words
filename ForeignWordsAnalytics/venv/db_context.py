import cx_Oracle

connection = None
try:
    connection = cx_Oracle.connect(
        "SYS",
        "password",
        "localhost:1522/XE",
        encoding="UTF-8",
        mode=cx_Oracle.SYSDBA)

    # show the version of the Oracle Database
    print(connection.version)
except cx_Oracle.Error as error:
    print(error)
finally:
    # release the connection
    if connection:
        connection.close()
