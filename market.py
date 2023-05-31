import pymysql
import pandas as pd


# 메인 페이지: 고객 / 관리자
# 일단 보류(union?)

################################################

# 고객, 관리자 선택
# 1: 고객, 2: 관리자
def user_admin_select():
    print("항목을 선택해주세요.")
    print("1. 고객")
    print("2. 관리자")
    num = 0
    try:
        num = int(input(" 번호 선택 >> "))
    except:
        while(num != 1 and num != 2):
            print("올바른 번호를 선택해주세요.")
            num = int(input(" 번호 선택 >> "))
    return num

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
# 반환 값 -> 등록한 아이디
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
                break   # 문자열 길이조건 추가?
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

    sql = "INSERT INTO customer (cno, name, pw) VALUES (%s, %s, %s)"
    cur.execute(sql, (newuser_cno, newuser_name, newuser_pw))

    print("회원가입이 완료되었습니다.")
    print("반갑습니다, ", newuser_name, "님!")
    return newuser_cno

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
    print("========================================================")

# 고객이 물건을 선택하는 메소드
# cart를 부름?
# 주문 한 건을 완성시켜야 함
# 현재 진행중인 주문 아이디 반환
def select_menu(user_cno):

    # order 테이블의 튜플을 생성 
    cur = con.cursor()
    sql = "INSERT INTO orders(cus_no) VALUES (%s)"
    cur.execute(sql, (str(user_cno)))
    rows = cur.fetchall()
    
    # 가장 큰 oid가 현재 주문중인 oid임. 즉, order 테이블 중 가장 큰 oid를  선택
    sql = "SELECT max(oid) FROM orders"
    cur.execute(sql)
    rows = cur.fetchall()
    current_oid = rows[0]['max(oid)']          

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
        
        # 메뉴의 수량 입력(재고 이하의 수량을 입력할 때까지 반복)
        while (True):
            print("메뉴의 수량을 입력해주세요")
            input_menu_qty = int(input(" 메뉴의 수량 >> "))

            # 메뉴 이름, 가격 구하기
            sql = "SELECT name, price FROM product WHERE pid = %s"
            cur.execute(sql, (input_pid))
            rows = cur.fetchall()
            menu_name = rows[0]['name']
            menu_price = rows[0]['price']

            ############################
            # 재고가 부족할 경우 구매 불가
            sql = "SELECT qty FROM product WHERE pid = " + str(input_pid)
            cur.execute(sql)
            rows = cur.fetchall()
            if (input_menu_qty > rows[0]['qty']):
                print("물건의 수량이 부족합니다. 최대 주문 갯수는 " + str(rows[0]['qty']) + "개 입니다.")
            else:
                break
            ############################

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

        cont = 0
        try:
            cont = int(input(" 번호 선택 >> "))
        except:
            while(cont != 1 and cont != 2):
                print("올바른 번호를 입력해주세요")
                cont = int(input(" 번호 선택 >> "))

        # stamp 수, 방문 횟수 증가
        # stamp 10000원당 1개 적립
        if (cont == 2):
            print("결제하기 화면으로 넘어갑니다.")
            continue_buy = 1
            return current_oid

# 결제 완료 창
def buy_product(user_cno, cur_oid):
    print("\n")
    cur = con.cursor()
    
    # 고객 정보 출력
    sql = "SELECT name FROM customer WHERE cno = " + str(user_cno)
    cur.execute(sql)
    rows = cur.fetchall()
    user_name = rows[0]['name']


    # 장바구니 내역 보여주기
    sql = "SELECT cart.pro_id, product.name, cart.qty, cart.qty * product.price FROM cart, product WHERE cart.ord_no = " + str(cur_oid) + " AND cart.pro_id = product.pid"
    cur.execute(sql)
    rows = cur.fetchall()

    print("======= < 장바구니 내역 > =======")
    print(" 상품 이름   상품 수량   총 금액 ")
    for row in rows:
        print(" {:<14} {:<6} {:<8}".format(row['name'], row['qty'], row['cart.qty * product.price']))
    print("=================================")

    sql = "SELECT price FROM orders WHERE oid = " + str(cur_oid)
    cur.execute(sql)
    rows = cur.fetchall()
    total_menu_price = rows[0]['price']
    print("총 결제 금액: [ " + str(total_menu_price) + "원 ]\n")

    print(user_name + "님, 결제하시겠습니까?")
    print("1. 결제하기")
    print("2. 취소하기")
    num = int(input(" 번호 선택 >> "))
    while (num != 1 and num != 2):
        print("올바른 번호를 선택해주세요.")
        num = int(input(" 번호 선택 >> "))
    
    # 1을 눌렀을 때 진행(결제 진행)
    if (num == 1):
        ####################################        
        # product 테이블의 qty 갱신
        cur = con.cursor()
        sql = "UPDATE product, cart SET product.qty = product.qty - cart.qty WHERE product.pid = cart.pro_id AND cart.ord_no = " + str(cur_oid)
        cur.execute(sql)
        ####################################

        # stamp 수 갱신
        add_stamp = total_menu_price // 10000

        sql = "UPDATE customer, orders SET customer.no_order = customer.no_order + 1, customer.stamp = customer.stamp + " + str(add_stamp) + " WHERE customer.cno = orders.cus_no AND orders.oid = " + str(cur_oid)

        cur.execute(sql)
        rows = cur.fetchall()

        cur = con.cursor()
        print("결제가 완료되었습니다.")
        sql = "SELECT name, stamp FROM customer WHERE cno =" + str(user_cno)
        cur.execute(sql)
        rows = cur.fetchall()
        user_name = rows[0]['name']
        user_stamp = rows[0]['stamp']

        # add_stamp = total_menu_price // 10000
        print("스탬프 " + str(add_stamp) + "개가 적립되었습니다.")
        print(user_name + "님의 스탬프 보유 수량은 " + str(user_stamp) + "개 입니다.")

        if (user_stamp >= 10):
            print("스탬프 10개를 사용하여 증정품을 받으시겠습니까?")
            print("1. 예")
            print("2. 아니오")
            num = int(input(" 번호 입력 >> "))
            if (num == 1):
                sql = "UPDATE customer SET stamp = stamp - 10 WHERE cno = " + str(user_cno)
                cur.execute(sql)
                print("증정품 지급이 완료되었습니다. 남은 스탬프 수는 " + str(user_stamp - 10) + "개 입니다.")
        
        print("저희 가게를 이용해주셔서 감사합니다.\n안녕히 가십시오.")


    # 주문을 취소했으므로 oid 삭제하기 -> cart의 값도 삭제가 됨
    else:
        sql = "DELETE FROM orders WHERE oid =" + str(cur_oid)
        cur.execute(sql)
        print("메뉴 주문을 취소하였습니다.")

#############################################

#########################################################


### 관리자용 ##############################################

# 관리자 로그인 화면
def login_admin():
    cur = con.cursor()
    cur.execute("SELECT admin_id FROM admin")
    rows = cur.fetchall()
    
    input_adminid = ""
    admin_name = ""

    # 최대 3회동안 아이디를 입력받음
    err_cnt = 1
    flag = 0
    while (err_cnt < 4 and flag == 0):
        input_adminid = input(" 전화번호 입력 >> ")
        for row in rows:
            if (input_adminid == row['admin_id']):
                flag = 1
                break       # 존재하는 아이디
        if (flag == 0):
            print("\n아이디가 올바르지 않습니다. 다시 입력해주세요.\n3회 오류 시 메인 화면으로 넘어갑니다.", err_cnt, "회 오류")
            err_cnt += 1

    if (err_cnt == 4):
        print("아이디를 3회 잘못 입력하셨습니다.")
        return 0

    # 최대 3회동안 비밀번호를 입력받음
    sql = "SELECT admin_pw, admin_name FROM admin WHERE admin_id = " + str(input_adminid)
    cur.execute(sql)
    rows = cur.fetchall()

    admin_name = rows[0]['admin_name']

    err_cnt = 1
    flag = 0
    while (err_cnt < 4):
        input_adminpw = input(" 비밀번호 입력 >> ")
        if (input_adminpw == rows[0]['admin_pw']):
            print("관리자 " + admin_name + "님, 반갑습니다!")
            return admin_name
                       
        print("\n비밀번호가 올바르지 않습니다. 다시 입력해주세요.\n3회 오류 시 메인 화면으로 넘어갑니다.", err_cnt, "회 오류")
        err_cnt += 1

        if (err_cnt == 4):
            print("비밀번호를 3회 잘못 입력하셨습니다.")
            return 0

    return 0

# 관리자 화면의 메뉴
def admin_menu():
    print("원하는 항목을 선택해주세요")
    print("1. 상품 재고 확인\n2. 매출 확인\n3. 영업 마감\n4. 프로그램 종료")
    num = 0
    try:
        num = int(input(" 항목 선택 >> "))
    except:
        while(num != 1 and num != 2 and num != 3 and num != 4):
            print("번호를 잘못 입력하였습니다. 다시 입력해주세요.")
            num = int(input(" 항목 선택 >> "))
    return num

# 상품의 재고 확인: 관리자 번호 1번
def admin_show_product():
    cur = con.cursor()
    cur.execute("SELECT * FROM product")
    rows = cur.fetchall()

    print("======================= < 상품 재고 목록 > =======================")
    print(" 상품번호 |      상품이름      |  카테고리  |   가격  |    재고 ")
    for row in rows:
        print("{:>8}  | {:<16} {:^8} {:>10} {:>6}".format(row['pid'], row['name'], row['cate'], row['price'], row['qty']))
    print("=================================================================")

# 그날 상품 별 판매개수와 매출확인
def admin_show_sales():
    cur = con.cursor()
    # 그날 날짜: 가장 큰 oid로 해당 날짜 조회, 이 날짜로 그날 있었던 모든 oid를 찾아냄
    # 이 방식에 문제가 있다면 python 자체에서 날짜를 구하고, 이를 사용
    sql = "SELECT ord_date FROM orders WHERE oid = (SELECT max(oid) FROM orders)"
    cur.execute(sql)
    rows = cur.fetchall()
    cur_date = rows[0]['ord_date']

    # 매출을 나타내는
    sql = "SELECT product.pid, product.name, SUM(cart.qty), SUM(product.price * cart.qty) FROM product, orders, cart WHERE orders.ord_date = '" + str(cur_date) + "' AND orders.oid = cart.ord_no AND cart.pro_id = product.pid GROUP BY product.pid, product.name ORDER BY product.pid"

    cur.execute(sql)
    rows = cur.fetchall()

    # 매출 표 출력
    print("================ < " + str(cur_date) + " 매출 표 > =================")
    print(" 상품번호 |    상품 이름    | 판매 수량 | 상품의 총 금액")
    for row in rows:
        print("{:>8}    {:<14} {:>6} {:>10}".format(row['pid'], row['name'], row['SUM(cart.qty)'], row['SUM(product.price * cart.qty)']))
    print("=========================================================")

    # 그날의 총 매출
    sql = "SELECT sum(price) AS P FROM orders WHERE ord_date = '" + str(cur_date) + "'"
    cur.execute(sql)
    # row = cur.fetchone()
    # tot_price = row[0]
    rows = cur.fetchall()
    total_price = rows[0]['P']

    print(" [총 매출: " + str(total_price) + "원 ]")

    # 나가기 버튼?


#########################################################

# DB와의 연결
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
user_admin = user_admin_select()

if (user_admin == 1):
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
            user_cno = newuser_register()


    # 신규회원 선택(2)
    elif (firstpage == 2):
        user_cno = newuser_register()

    ### 본격적인 주문하기 ######################################

    # 로그인을 실패했을 때 여기로 넘어오지 않게 해야 함: 파이썬 파일 강제 종료?
    # print("\n메뉴를 선택해 주세요.")
    # show_menus()
    cur_oid = select_menu(user_cno)

    # print("주문이 완료되었습니다.")

    # 결제하기 화면
    print("결제하기")
    buy_product(user_cno, cur_oid)

elif (user_admin == 2):
    print("관리자로 로그인합니다.")
    result = login_admin()
    if (result != 0):   # 로그인 성공
        while (True):
            menu_select = admin_menu()

            # 상품 재고 확인
            if (menu_select == 1):
                admin_show_product()
            # 당일 매출 확인
            elif (menu_select == 2):
                admin_show_sales()
            # 영업 마감
            elif (menu_select == 3):
                print("미정")
            elif (menu_select == 4):
                print("프로그램을 종료합니다.")
                break


# rows = cur.fetchall()
con.close()
# customers = pd.DataFrame(rows)
