import pymysql
import pandas as pd

try:
    con = pymysql.connect (
        host='localhost',
        user='root',
        password='Min02choi!',
        db='company',
        charset='utf8',
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )
except:
    print("ERROR: MySQL 연결 실패")
    exit()


cur = con.cursor()

sql = """
SELECT * FROM employee
"""

cur.execute(sql)
rows = cur.fetchall()
con.close()
customers = pd.DataFrame(rows)
print(customers)
