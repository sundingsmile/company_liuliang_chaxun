#coding:utf8
import requests,prettytable,time,re

# 登录
def login():
    post_url = 'http://192.168.1.210/cgi-bin/webif/login.sh'
    post_data = {
        'username': 'useradmin',
        'password': 'LongSure10',
        'Submit': '%E7%99%BB%E5%BD%95'
    }
    ses = requests.session()
    login_res = ses.post(post_url,data=post_data).content.decode()
    if login_res.find('alert') != -1:
        print('密码错误')
        input()
    else:
        return ses

# 读取信息
def read_data(ses):
    data_url = 'http://192.168.1.210/cgi-bin/webif/SystemInfo-online.sh?displayperpg=all&sort=3&jtab='
    data_res = ses.get(data_url)
    temp_list = re.findall('<td>(.*?)</td>',data_res.content.decode(),re.S)
    data_list = []
    temp_list.pop(0)
    temp_list.pop(0)
    for temp in temp_list:
        data_list.append(temp.strip())
    return data_list

# 打印输出
def print_data(data_list):
    tb = prettytable.PrettyTable()
    tb.field_names = ['序号','主机名','IP地址','上行速率','下行速率','上行流量','下行流量','会话数']
    length = int(len(data_list)/8)
    for temp in range(length):
        tb.add_row(data_list[temp * 8 : (temp + 1) * 8])
    print(tb)




if __name__ == '__main__':
    print('正在查询...')
    ses = login()
    while True:
        data = read_data(ses)
        print_data(data)
        time.sleep(20)
        print('*' * 105)
