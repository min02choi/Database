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
# 반환 -> 1: 올바른 아이디, 2: 아이디 X
def enter_cno():
    cur = con.cursor()
    cur.execute("SELECT cno FROM customer")
    rows = cur.fetchall()

    # print("전화번호를 입력해주세요.")
    input_cno = input(" 전화번호 입력 >> ")
    real_cno = ""
    for row in rows:
        if (input_cno == row['cno']):
            real_cno = row['cno']
            return real_cno, 1
    print("전화번호가 올바르지 않습니다.\n다시 입력해주세요.")
    while(input_cno != "1" and input_cno != "2"):
        print("번호를 다시 입력해주세요.")
        input_cno = input(" >> ")
    return False, 2


# 전화번호 입력
# 반환 -> 1: 올바른 비밀번호, 2: 비밀번호 X
def enter_pw1():
    cur = con.cursor()
    cur.execute("SELECT pw FROM customer")
    rows = cur.fetchall()

    input_pw = input(" 비밀번호 입력 >> ")
    real_pw = ""
    for row in rows:
        if (input_pw == row['pw']):
            real_pw = row['pw']
            return 1
    while(input_pw != real_pw):
        print("비밀번호가 올바르지 않습니다.\n다시 입력해주세요.")
        input_pw = input(" 비밀번호 입력 >> ")
    return 2


# 전화번호 입력 2
# 반환 -> 1: 올바른 비밀번호, 2: 비밀번호 X
def enter_pw(input_cno):
    cur = con.cursor()
    cur.execute("SELECT pw FROM customer WHERE cno=", input_cno)
    rows = cur.fetchall()

    input_pw = input(" 비밀번호 입력 >> ")
    real_pw = rows['pw']

    if (input_pw == real_pw):
        return 1
    else:
        while(input_pw != real_pw):
            print("비밀번호가 올바르지 않습니다.\n다시 입력해주세요.")
            input_pw = input(" 비밀번호 입력 >> ")
    return 2





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

    print("전화번호를 입력해주세요.")
    customer_no, num = enter_cno()
    if (num == 1):
        print("비밀번호를 입력해주세요.")
        if (enter_pw(customer_no) == 1):
            print("로그인 완료")



    elif (num == 2):
        print("올바르지 않은 아이디입니다.")

    

# 회원가입
else:
    print("2corr")


cur.execute(sql)
rows = cur.fetchall()
con.close()
customers = pd.DataFrame(rows)
# print(customers)
