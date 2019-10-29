import requests
import json

#注册
# register and print http response


def register():
    url = 'http://api.revth.com/auth/register'
    payload = {'username': '小黄鸭', 'password': 'xiaopassword'}
    payloadjs = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=payloadjs)
    print(r.text)


#注册+绑定
# register and print http response


def register2():
    url = 'http://api.revth.com/auth/register2'
    payload = {'username': '小黄鸭', 'password': 'xiaopassword', 'student_number': '031702345', 'student_password': ''}
    payloadjs = json.dumps(payload)
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=payloadjs)
    print(r.text)


# 登陆
# login Success return token And faild return 0/show login status
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
            token = responsedict['data']['token']
            global user_id
            user_id = responsedict['data']['user_id']
            return token
        else:
            print("login_error")
            return '0'
    else:
        print("login_error,status_code=")
        print(r.status_code)
        return '0'


#注销
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


#绑定
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
        if (status == 0 & user_id >= 0):
            print("check_token_login_success")
            return True
        else:
            return False
    else:
        return False


#历史纪录
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


#排行榜


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


#出牌
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


#AI 把牌分成三墩并输出

def transfer(cards_dict):
    cards=cards_dict['cards']
    #𝐴 > 𝐾 > 𝑄 > 𝐽 > 10 > 9 > 8 > 7 > 6 > 5 > 4 > 3 > 2
