import pymysql
import pandas as pd


# 메인 페이지: 고객 / 관리자
# 일단 보류(union?)
# def select_user():

#     return


### 고객용 ###############################################

# 메인화면: 로그인 / 신규회원
# 1: 로그인, 2: 신규회원
def user_mainpage():
    print("안녕하세요, 저희 가게를 방문해주셔서 감사합니다.")
    print("아래 항목을 선택해주세요.\n")
    print("1. 로그인")
    print("2. 신규회원")

    num = input(" >> ")
    while(num != "1" and num != "2"):
        print("번호를 다시 입력해주세요.")
        num = input(" >> ")
    
    return int(num)

# 전화번호 입력
#
def enter_cno():
    cur = con.cursor()



### 관리자용 ##############################################

con = pymysql.connect (
    host='localhost', user='root', password='Min02choi!',
    db='meal_kit_market', charset='utf8', autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
)

cur = con.cursor()

sql = """
SELECT * FROM product
"""

# 로그인
if (user_mainpage() == 1):
    print("전화번호를 입력해주세요")
    phone = input(" 전화번호 입력 >> ")
    cur.execute("SELECT cno FROM customer")
    rows = cur.fetchall()
    for row in rows:
        print("row", row)
        if phone == row['cno']:
            print("있는 번호!! 굿")
    

# 회원가입
else:
    print("2corr")


cur.execute(sql)
rows = cur.fetchall()
con.close()
customers = pd.DataFrame(rows)
# print(customers)
