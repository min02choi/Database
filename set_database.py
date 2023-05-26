import pymysql
import pandas as pd

con = pymysql.connect (
    host='localhost', user='root', password='Min02choi!',
    db='meal_kit_market', charset='utf8', autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
)

cur = con.cursor()

sql = """
SELECT * FROM EMPLOYEE
"""

cur.execute(sql)
rows = cur.fetchall()
con.close()
customers = pd.DataFrame(rows)
print(customers)
