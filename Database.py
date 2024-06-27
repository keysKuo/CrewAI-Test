import sqlite3
import mysql.connector
import psycopg2
# import cx_Oracle

class Database:
    type = "mysql"

    def __init__(self, type):
        self.type = type 
    
    def query(self, configs):
        actions = {
            'mysql': queryMySQL(configs)
        }
        return actions.get(self.type)


def querySQLite(configs):
    conn = sqlite3.connect(configs.get('uri'))
    c = conn.cursor()

    c.execute(configs.get('ssql'))
    result = c.fetchall()
    c.close()

    return result

def queryMySQL(configs):
    conn = mysql.connector.connect(
        host= configs.get('host'),
        user= configs.get('user'),
        password= configs.get('password'),
        database= configs.get('database'),
        port=3306

    )
    c = conn.cursor()

    c.execute(configs.get('ssql'))
    result = c.fetchall()
    c.close()

    return result

DB = Database("mysql")
configs = {
    'host': 'localhost',
    'user': 'root',
    'password': '9952811',
    'database': 'ManageTest',
    'ssql': """
        SELECT
            c.FirstName,
            p.ProductName,
            o.OrderDate,
            SUM(od.Price * od.Quantity) AS Total_Price
        FROM
            Customers c
        JOIN
            Orders o ON c.CustomerID = o.CustomerID
        JOIN
            OrderDetails od ON o.OrderID = od.OrderID
        JOIN
            Products p ON od.ProductID = p.ProductID
        GROUP BY
            c.FirstName,
            p.ProductName,
            o.OrderDate
        ORDER BY
            Total_Price DESC
        LIMIT 20;
    """
}
result = DB.query(configs)
for row in result:
    print(row)