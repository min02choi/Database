def return_no():
    no = input()
    if (no == "000"):
        return 1
    elif (no == "111"):
        return 2
    else:
        print("올바르지 않은 번호입니다.")
        return 3


# 재입력 요구

print("전화번호 입력")
non = return_no()
while (non != 1 or non != 2):
    if (non == 1):
        print("right 000")
    elif (non == 2):
        print("roght 111")
    else:
        print("아이디를 다시 입력하려면 1, 신규회원가입을 진행하려면 2번을 누르십시오.")
        num = int(input(" >> "))
        if (num == 1):
            return_no()
        elif (num == 2):
