import pymysql
import pandas as pd

con = pymysql.connect (
    host='localhost', user='root', password='Min02choi!',
    db='company', charset='utf8', autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
)

cur = con.cursor()

sql = """
CREATE TABLE EMPLOYEE (
    Frame VARCHAR(15) NOT NULL,
    Minit CHAR,
    Lname VARCHAR(15) NOT NULL,
    Ssn CHAR(9) NOT NULL,
    Bdate DATE,
    Address VARCHAR(30),
    Sex CHAR,
    Salary DECIMAL (10,2),
    Super_ssh CHAR(9),
    Dno INT NOT NULL,
    PRIMARY KEY(Ssn))
"""

cur.execute(sql)
rows = cur.fetchall()
con.close()
customers = pd.DataFrame(rows)
print(customers)
