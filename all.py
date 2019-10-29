import requests
import json

# 注册
# register and print http response

global user_id


def register():
    url = 'http://api.revth.com/auth/register'
    payload = {'username': '小黄鸭', 'password': 'xiaopassword'}
    payloadjs = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=payloadjs)
    print(r.text)


# 注册+绑定
# register and print http response


def register2():
    url = 'http://api.revth.com/auth/register2'
    payload = {'username': '小黄鸭', 'password': 'xiaopassword', 'student_number': '031702345', 'student_password': ''}
    payloadjs = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=payloadjs)
    print(r.text)


# 登陆
# login Success return token And faild return {}/show login status
# global user_id

def login():
    url = 'http://api.revth.com/auth/login'
    payload = {'username': '小黄鸭', 'password': 'xiaopassword'}
    payloadjs = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=payloadjs)
    print(r.text)
    if (r.status_code == 200):
        print("login_success")
        responsedict = json.loads(r.text)
        status = responsedict['status']
        if (status == 0):
            return responsedict
        else:
            print("login_error")
            return {}
    else:
        print("login_error,status_code=")
        print(r.status_code)
        return {}


# 注销
# return True or False/print info


def logout(token):
    url = 'http://api.revth.com/auth/logout'
    headers = {'X-Auth-Token': token}
    r = requests.post(url, headers=headers)
    print(r.text)
    if (r.status_code == 200):
        responsedict = json.loads(r.text)
        status = responsedict['status']
        if (status == 0):
            print("logout_success")
            return True
        else:
            print("logout_error")
            return False
    else:
        print("logout_error,status_code=")
        print(r.status_code)
        return False


# 绑定
# return True or False/print info


def bind_num(token):
    url = 'http://api.revth.com/auth/bind'
    payload = {'student_number': '小黄鸭', 'student_password': 'xiaopassword'}
    payloadjs = json.dumps(payload)
    headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    r = requests.post(url, headers=headers, data=payloadjs)
    print(r.text)
    if (r.status_code == 200):
        responsedict = json.loads(r.text)
        status = responsedict['status']
        if (status == 0):
            print("bind_success")
            return True
        else:
            print("bind_error")
            return False
    else:
        print("bind_error,status_code=")
        print(r.status_code)
        return False


# 登陆验证
# check token and return True or False /show 'check_token_login_success'


def check_token(token):
    url = 'http://api.revth.com/auth/validate'
    header = {
        "X-Auth-Token": token,
    }
    r = requests.get(url, headers=header)
    print(r.text)
    if (r.status_code == 200):
        responsedict = json.loads(r.text)
        status = responsedict['status']
        user_id = responsedict['data']['user_id']
        if (status == 0 and user_id >= 0):
            print("check_token_login_success")
            return True
        else:
            return False
    else:
        return False


# 历史纪录
# return text


def history_list(token):
    if check_token(token) == False:
        token = login()
    header = {
        "X-Auth-Token": token,
    }
    data = {
        "player_id": user_id,
        "limit": 20,
        "page": 0
    }
    r = requests.get("http://api.revth.com/history", data=data, headers=header)
    return r.text


# 排行榜


def rank():
    url = 'http://api.revth.com/rank'
    ranklist = json.loads(requests.get(url).text)
    for i in ranklist:
        print(i)


# 开启牌局
# return cards_dict = {'id': id, 'cards': cards}


def get_cards(token):
    if check_token(token) == False:
        token = login()
    url = "http://api.revth.com/game/open"
    headers = {'X-Auth-Token': token}
    response = requests.request("POST", url, headers=headers)
    data = response.text
    data_dict = json.loads(data)
    cards = data_dict["data"]["card"]
    id = data_dict["data"]["id"]
    cards_dict = {'id': id, 'cards': cards}
    print('card_dict:', cards_dict)
    return cards_dict


# 出牌
# return True or False/print info


def deliver_cards(cards_dict, token):
    url = 'http://api.revth.com/game/submit'
    payload = {'id': cards_dict['id'], 'card': cards_dict['cards']}
    payloadjs = json.dumps(payload)
    headers = {'Content-Type': 'application/json', 'X-Auth-Token': token}
    r = requests.post(url, headers=headers, data=payloadjs)
    print(r.text)
    if (r.status_code == 200):
        responsedict = json.loads(r.text)
        status = responsedict['status']
        if (status == 0):
            print("deliver_success")
            return True
        else:
            print("deliver_error")
            return False
    else:
        print("deliver_error,status_code=")
        print(r.status_code)
        return False


# 比牌函数 return True or False
# 牌型大小：同花顺 > 炸弹 > 葫芦 > 同花 > 顺子 > 三条 > 二对 > 一对 > 散牌

def Shunzi(five_list):
    num = []
    for j in five_list:
        num.append(j[1])
    num.sort()
    _check = True
    for j in range(0, 4):
        if (num[j] + 1) != num[j + 1]:
            _check = False
    if _check == True:
        return True
    else:
        return False


def ShunziCheck():
    Shunzilist = [(1, 9), (2, 8), (3, 10), (0, 7), (0, 11)]
    NotShunzilist = [(0, 9), (0, 1), (0, 10), (0, 7), (0, 11)]
    print(Shunzi(Shunzilist))
    print(Shunzi(NotShunzilist))


def Tonghua(five_list):
    cnt = [0, 0, 0, 0]
    for i in five_list:
        cnt[i[0]] += 1
    for i in range(0, 4):
        if cnt[i] == 5:
            return True
    return False


def TonghuaCheck():
    Tonghualist = [(0, 9), (0, 8), (0, 10), (0, 7), (0, 11)]
    NotTonghualist = [(0, 9), (0, 1), (1, 10), (0, 7), (0, 11)]
    print(Tonghua(Tonghualist))
    print(Tonghua(NotTonghualist))


def Tonghuashun(five_list):
    if Tonghua(five_list) and Shunzi(five_list):
        return True
    return False


def TonghuashunCheck():
    Tonghuashunlist = [(0, 9), (0, 8), (0, 10), (0, 7), (0, 11)]
    NotTonghuashunlist = [(0, 9), (0, 1), (0, 10), (0, 7), (0, 11)]
    print(Tonghuashun(Tonghuashunlist))
    print(Tonghuashun(NotTonghuashunlist))


def Zhadan(five_list):
    mapcheck = {}
    for i in five_list:
        if (mapcheck.__contains__(i[1]) == True):
            # Python 3.X Not use has_key instead of __contains__
            mapcheck[i[1]] += 1
        else:
            mapcheck[i[1]] = 1
    for i in five_list:
        if mapcheck[i[1]] >= 4:
            return True
    return False


def ZhadanCheck():
    Zhadanlist = [(0, 1), (1, 1), (2, 1), (3, 1), (2, 11)]
    NotZhadanlist = [(0, 1), (1, 1), (2, 1), (3, 11), (2, 11)]
    print(Zhadan(Zhadanlist))
    print(Zhadan(NotZhadanlist))


def Santiao5(five_list):
    mapcheck = {}
    for i in five_list:
        if (mapcheck.__contains__(i[1]) == True):
            # Python 3.X Not use has_key instead of __contains__
            mapcheck[i[1]] += 1
        else:
            mapcheck[i[1]] = 1
    for i in five_list:
        if mapcheck[i[1]] >= 3:
            return True
    return False


def Santiao5Check():
    Santiao5list = [(0, 1), (1, 1), (2, 1), (3, 5), (2, 11)]
    NotSantiao5list = [(0, 1), (1, 2), (2, 1), (3, 5), (2, 11)]
    print(Santiao5(Santiao5list))
    print(Zhadan(NotSantiao5list))


def Hulu(five_list):
    mapcheck = {}
    for i in five_list:
        if (mapcheck.__contains__(i[1]) == True):
            # Python 3.X Not use has_key instead of __contains__
            mapcheck[i[1]] += 1
        else:
            mapcheck[i[1]] = 1
    sancheck = False
    twocheck = False
    for i in five_list:
        if mapcheck[i[1]] == 3:
            sancheck = True
        if mapcheck[i[1]] == 2:
            twocheck = True
    if twocheck and sancheck:
        return True
    else:
        return False


def HuluCheck():
    Hululist = [(0, 1), (1, 1), (2, 1), (3, 5), (2, 5)]
    NotHululist = [(0, 1), (1, 1), (2, 1), (3, 6), (2, 5)]
    print(Hulu(Hululist))
    print(Hulu(NotHululist))


def Erdui(five_list):
    mapcheck = {}
    for i in five_list:
        if (mapcheck.__contains__(i[1]) == True):
            # Python 3.X Not use has_key instead of __contains__
            mapcheck[i[1]] += 1
        else:
            mapcheck[i[1]] = 1
    if len(mapcheck) > 3 or len(mapcheck) == 1:
        return False
    return True


def ErduiCheck():
    Erduilist = [(0, 1), (1, 1), (2, 2), (3, 2), (2, 5)]
    NotErduilist = [(0, 1), (1, 1), (2, 2), (3, 6), (2, 5)]
    print(Erdui(Erduilist))
    print(Erdui(NotErduilist))


def Dui(five_list):
    mapcheck = {}
    for i in five_list:
        if (mapcheck.__contains__(i[1]) == True):
            # Python 3.X Not use has_key instead of __contains__
            mapcheck[i[1]] += 1
        else:
            mapcheck[i[1]] = 1
    _check = False
    for i in five_list:
        if mapcheck[i[1]] == 2:
            _check = True
    if _check:
        return True
    else:
        return False


def DuiCheck():
    Duilist = [(0, 1), (1, 1), (2, 2), (3, 6), (2, 5)]
    NotDuilist = [(0, 11), (1, 1), (2, 2), (3, 6), (2, 5)]
    print(Dui(Duilist))
    print(Dui(NotDuilist))


def check_cmp():
    print('同花顺')
    TonghuashunCheck()
    print('同花')
    TonghuaCheck()
    print('顺子')
    ShunziCheck()
    print('炸弹')
    ZhadanCheck()
    print('三条')
    Santiao5Check()
    print('葫芦')
    HuluCheck()
    print('二对')
    ErduiCheck()
    print('一对')
    DuiCheck()
    # print('散牌',TonghuaCheck())


# AI 把牌分成三墩并输出
def transfer(cards_dict):
    cards = cards_dict['cards'].split()
    print(cards)
    # 𝐴 > 𝐾 > 𝑄 > 𝐽 > 10 > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2
    # used = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 8: 0, 10: 0, 11: 0, 12: 0}
    # pai = {}
    # 单张/散牌 一墩里面没有其它特殊牌型，都是一张一张单独的牌
    # 对子 2 张相同数字的牌凑成一对
    # 二对 2 个对子加上 1 个单张
    # 三条 3 张一样的牌，中、后墩中的三条则是 3 张相同数字的牌加上 2 个单张
    # 顺子 连续 5 张牌，刚好凑成 5 个连续的牌面大小排列 同花 5 张同样花色的牌，同花牌大小以 5 张中最大牌面计算
    # 葫芦 1 组三条加上 1 组对子总共 5 张（一大一小的组合状似葫芦的样子）
    # 炸弹 4 张同样数字的牌并加上随意 1 张牌凑成 5 张一墩
    # 同花顺 刚好凑成 5 个连续的牌面大小排列，同时又是 5 张都是同样的花色
    # hua = ['#', '*', '&', '$']
    map_hua = {'#': 0, '*': 1, '&': 2, '$': 3}
    map_num = {'A': 14, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11,
               'Q': 12, 'K': 13}
    card_list = []
    for i in cards:
        x, y = map_hua[i[0]], map_num[i[1:len(i)]]
        card_list.append((x, y))
    print(card_list)
    sz = len(card_list)
    back_choose = []
    back_val = 0
    tmp_choose = []
    cnt = 0
    for i in range(0, sz, 1):
        tmp_choose.append(card_list[i])
        for j in range(i + 1, sz, 1):
            tmp_choose.append(card_list[j])
            for k in range(j + 1, sz, 1):
                tmp_choose.append(card_list[k])
                for l in range(k + 1, sz, 1):
                    tmp_choose.append(card_list[l])
                    for m in range(l + 1, sz, 1):
                        tmp_choose.append(card_list[m])
                        cnt += 1
                        val = 0
                        # 顺序比较 同花顺 > 炸弹 > 葫芦 > 同花 > 顺子 > 三条 > 二对 > 一对 > 散牌
                        if Tonghuashun(tmp_choose):
                            val = 20
                        elif Zhadan(tmp_choose):
                            val = 19
                        elif Hulu(tmp_choose):
                            val = 18
                        elif Tonghua(tmp_choose):
                            val = 17
                        elif Shunzi(tmp_choose):
                            val = 16
                        elif Santiao5(tmp_choose):
                            val = 15
                        elif Erdui(tmp_choose):
                            val = 14
                        elif Dui(tmp_choose):
                            val = 13
                        if val > back_val:
                            # python `s '==' is not a copy
                            back_choose = tmp_choose.copy()
                            # print(back_choose)
                            back_val = val
                        tmp_choose.pop()
                    tmp_choose.pop()
                tmp_choose.pop()
            tmp_choose.pop()
        tmp_choose.pop()
    print(back_choose, back_val)


redict = login()
token = redict['data']['token']
user_id = redict['data']['user_id']
transfer(get_cards(token))
