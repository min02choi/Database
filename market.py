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
    print("아래 항목을 선택해주세요.\n")
    print("1. 로그인")
    print("2. 신규회원")
    num = input(" >> ")

    while(num != "1" and num != "2"):
        print("번호를 다시 입력해주세요.")
        num = input(" >> ")
    
    return int(num)

# 전화번호 입력
# 값을 미리 저장해놓는게 아닌 사용자가 입력한 아이디를 DB의 cno와 하나씩 비교
# 반환 값 -> input_cno: 올바른 아이디, 0: 아이디 X(5회 오류), 신규회원 가입 페이지로 넘어감
def enter_cno():
    cur = con.cursor()
    cur.execute("SELECT cno FROM customer")
    rows = cur.fetchall()

    # 최대 5회동안 아이디를 입력받음
    err_cnt = 1
    while (err_cnt < 6):
        input_cno = input(" 전화번호 입력 >> ")
        for row in rows:
            if (input_cno == row['cno']):
                return input_cno
        
        print("\n전화번호가 올바르지 않습니다. 다시 입력해주세요.\n5회 오류 시 신규회원 가입 화면으로 넘어갑니다.", err_cnt, "회 오류")
        err_cnt += 1

    return 0

# 입력받은 아이디에 해당하는 비밀번호 입력
# 반환 값 -> 1: 로그인 성공, 2: 비밀번호 입력 실패(5회 오류)
# 이름을 반환해야 하나?
def enter_pw(user_cno):
    cur = con.cursor()
    sql = "SELECT pw FROM customer WHERE cno =" + user_cno
    cur.execute(sql)
    rows = cur.fetchall()
    real_pw = rows[0]['pw']

    sql = "SELECT name FROM customer WHERE cno =" + user_cno
    cur.execute(sql)
    rows = cur.fetchall()
    real_name = rows[0]['name']

    err_cnt = 1
    while (err_cnt < 4):
        input_pw = input(" 비밀번호 입력 >> ")
        if (input_pw == real_pw):
            return real_name
        # 메인 화면으로 어떻게 넘어갈건데?
        else:
            print("\n비밀번호를 잘못 입력하셨습니다.\n3회 오류 시 메인 화면으로 넘어갑니다.", err_cnt, "회 오류")
            err_cnt += 1

# 신규회원 가입
# 반환 값 -> 없음
def newuser_register():
    cur = con.cursor()
    cur.execute("SELECT cno FROM customer")
    rows = cur.fetchall()

    newuser_cno = ""
    newuser_pw = ""
    newuser_name = ""

    print("신규회원 가입 페이지입니다.\n전화번호를 입력해주세요.")
    # 아이디를 입력받기
    while (True):

        # 전화번호의 형식 확인
        while (True):
            try:
                newuser_cno = input(" 전화번호 입력 >> ")[:11]
                temp = int(newuser_cno)    # 01012345678 의 형태
                break
            except:
                print("전화번호의 형식이 잘못되었습니다. 다시 입력해주세요.")

        # DB의 데이터와 중복 검사
        flag = 0
        for row in rows:
            if (newuser_cno == row['cno']):
                print("이미 존재하는 전화번호입니다.")
                flag = 1
                break
        
        # 중복 아닌 전화번호 입력 성공
        if (flag == 0):
            print("비밀번호를 입력하세요.")
            newuser_pw = input(" 비밀번호 입력 >> ")

            print("비밀번호를 재입력하세요.")
            temp = input(" 비밀번호 재입력 >> ")
            while (newuser_pw != temp):
                print("비밀번호가 틀립니다. 다시 입력하세요.")
                temp = input(" 비밀번호 재입력 >> ")
            
            print("비밀번호가 일치합니다.\n이름을 입력해주세요.")
            newuser_name = input(" 이름 입력 >> ")
            break

    # print(newuser_cno, newuser_name, newuser_pw)

    sql = "INSERT INTO customer (cno, name, pw) VALUES (%s, %s, %s)"
    cur.execute(sql, (newuser_cno, newuser_name, newuser_pw))

    print("회원가입이 완료되었습니다.")
    print("반갑습니다, ", newuser_name, "님!")

# 가게의 메뉴를 보여주는 함수
# 반환
def show_menus():
    cur = con.cursor()
    cur.execute("SELECT pid, name, cate, price FROM product")
    rows = cur.fetchall()

    print("===================== < 메뉴 목록 > =====================")
    print(" 메뉴번호 |      메뉴이름      |  카테고리  |   가격 ")
    for row in rows:
        print("{:>8}  | {:<16} {:^8} {:>10}".format(row['pid'], row['name'], row['cate'], row['price']))
        # print(row['pid'], row['name'], row['cate'])
    print("========================================================")

# 고객이 물건을 선택하는 메소드
# cart를 부름?
# 주문 한 건을 완성시켜야 함
def select_menu(user_cno):

############ 에러나 ############################################

    # order 테이블의 튜플을 우선 생성 
    cur = con.cursor()
    sql = "INSERT INTO orders(cus_no) VALUES (%s)"
    cur.execute(sql, (str(user_cno)))
    rows = cur.fetchall()

########################################################
    
    # 가장 큰 oid가 현재 주문중인 oid임. 즉, order 테이블 중 가장 큰 oid를  선택
    sql = "SELECT max(oid) FROM orders"
    cur.execute(sql)
    rows = cur.fetchall()
    current_oid = rows[0]['max(oid)']          

    # print(">>>>>>>>current_oid: ", current_oid)

    total_menu_price = 0    # order에서 당기기?
    continue_buy = 0        # 계속 구매
    
    while (continue_buy == 0):

        cur = con.cursor()
        cur.execute("SELECT pid FROM product")
        rows = cur.fetchall()

        print("메뉴를 선택해 주세요.")
        show_menus()
        input_pid = int(input(" 메뉴 선택 >> "))

        # 입력한 번호가 상품 번호에 있는지
        flag = 0
        while (flag == 0):
            for row in rows:
                if (input_pid == row['pid']):
                    flag = 1
            if (flag == 0):
                print("메뉴가 올바르지 않습니다. 다시 선택해주세요")
                input_pid = int(input(" 메뉴 선택 >> "))
        
        # 메뉴의 수량 입력
        # print("")
        print("메뉴의 수량을 입력해주세요")
        input_menu_qty = int(input(" 메뉴의 수량 >> "))

        # 메뉴 이름, 가격 구하기
        sql = "SELECT name, price FROM product WHERE pid = %s"
        cur.execute(sql, (input_pid))
        rows = cur.fetchall()
        menu_name = rows[0]['name']
        menu_price = rows[0]['price']

        # 장바구니에 추가
        sql = "INSERT INTO cart(ord_no, pro_id, qty) VALUES (%s, %s, %s)"
        cur.execute(sql, (current_oid, input_pid, input_menu_qty))

        # order table의 price 수정
        sql = "UPDATE orders SET price = price + " + str(menu_price * input_menu_qty) + " WHERE oid = " + str(current_oid)
        cur.execute(sql)

        sql = "SELECT price FROM orders WHERE oid = " + str(current_oid)
        cur.execute(sql)
        rows = cur.fetchall()
        total_menu_price = rows[0]['price']


        # 주문 내역 정리
        print(menu_name, "을 ", input_menu_qty, "개 선택하였습니다.\n총 금액은 ", menu_price * input_menu_qty, "입니다.")
        print("장바구니의 총 금액은 ", total_menu_price, "입니다.")
        print("계속 구매하시겠습니까?")
        print("1. 계속 구매하기")
        print("2. 결제하기")
        cont = int(input(" 번호 선택 >> "))


######################################## 에러난다

        # stamp 수, 방문 횟수 증가
        # stamp 10000원당 1개 적립
        if (cont == 2):
            add_stamp = total_menu_price // 10000
            sql =   " UPDATE customer (no_order, stamp) SET no_order = no_order + 1, stamp = stamp + " + str(add_stamp)
            cur.execute(sql)
            rows = cur.fetchall()

            print("결제하기 화면으로 넘어갑니다.")
            continue_buy = 1

########################################



        
### 관리자용 ##############################################


#########################################################



con = pymysql.connect (
    host='localhost', user='root', password='Min02choi!',
    db='meal_kit_market', charset='utf8', autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
)

cur = con.cursor()

### 주문 이전까지의 화면 #################

user_cno = None
user_name = None

# 첫 화면
# while (True):
print("안녕하세요, 저희 가게를 방문해주셔서 감사합니다.")
firstpage = user_mainpage()

# 로그인 선택(1)
if (firstpage == 1):
    print("전화번호를 입력해주세요.")

    # 아이디 입력요구 -> 유효 아이디 성공: 아이디, 로그인 실패: 0
    user_cno = enter_cno()
    if (user_cno != 0):             # 유효 어이디 성공 -> 비밀번호 입력

        # 비밀번호 입력요구 -> 성공: 닉네임, 실패: 0
        user_name = enter_pw(user_cno)
        if (user_name != 0):                # 로그인 성공
            print("\n", user_name, "님, 반갑습니다!")
        else:                               # 로그인 실패
            print("로그인 실패!!!")
            # 로그인 실패 시 어떻게..?

    else:                           # 유효 어이디 실패 -> 신규회원 가입 페이지로 이동
        print("신규회원 가입 페이지로 이동합니다.")



# 신규회원 선택(2)
elif (firstpage == 2):
    newuser_register()

### 본격적인 주문하기 ######################################

# 로그인을 실패했을 때 여기로 넘어오지 않게 해야 함
# print("\n메뉴를 선택해 주세요.")
# show_menus()
select_menu(user_cno)
print("주문이 완료되었습니다.")



# rows = cur.fetchall()
con.close()
# customers = pd.DataFrame(rows)
