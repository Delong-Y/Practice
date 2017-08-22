from bs4 import BeautifulSoup
import requests
import re
import subprocess
import sys
import traceback
import codecs
import locale
import re
import os


def main():
    while True:
        try:
            command = input()
            if command == "exit" :
                sys.exit(0)
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            if not isinstance(output, str):
                output = output.decode('gbk')
            print("[*] {0}".format(output))
        except KeyboardInterrupt:
            sys.exit(0)
        except SystemExit:
            sys.exit(0)
        except:
            traceback.print_exc()
            continue

if __name__ == '__main__':
    url = 'http://www.xiuren.org/tuigirl/special-lilisha/tuigirl-special-lilisha-double-001.jpg'
    # t = url.split('/')
    # p = '\\'.join(t[2:])
    # print(os.path.basename(p))
    # print(os.path.dirname(p))
    # print(p)
    a = 2
    b = 4

    print(a) if a <= b else None
