import argparse
import os
import re
import io
from contextlib import redirect_stderr

def file_write(data):
    wf = open("req.py","a+")
    wf.write(data + "\n")

def file_move(data):
    os.rename("req.py",data)

def static_write():
    file_write("import requests" + "\n\n" + "def req():")

def host_write(data,connection):
    _host = re.split(":", data)
    if connection == "http" :
        file_write("\t" + 'host = "http://' + _host[1].rstrip().lstrip() + '"')
    else:
        file_write("\t" +'host = "https://' + _host[1].rstrip().lstrip() + '"')

def url_write(url):
        file_write("\t" +'url = "' + url + '"')

def headers_write(data):
        wdata = "head = {\n"
        for x in data:
            _headers = re.split(": ",x.rstrip().lstrip())
            try:
                if (_headers[0] != "Host" and _headers[0] != "Cookie" and _headers[1] != ""):
                    wdata += "\t\t'" + _headers[0].rstrip().lstrip() + "'" + ":" + "'" + _headers[1].rstrip().lstrip() + "'" + ",\n"
            except:
                pass
        file_write("\t" +wdata[:-2] + "\n\t\t}")

def cookie_write(data):
    _cookie = ""
    _allcookies = re.split(":", data)
    _separatecookies = re.split(";", _allcookies[1])
    for x in _separatecookies:
        _cookiesvalue = re.split("=",x)
        _cookie += ( "'" + _cookiesvalue[0].lstrip().rstrip() + "'" + " : " + "'" + _cookiesvalue[1].lstrip().rstrip() + "',\n\t\t")
    wdata = "\t" +"cookie = { \n\t\t" + _cookie[:-4] + "\n\t\t}"
    file_write(wdata)

def req_write(data,cookie_status):
        _reqmethod = re.split(" ",data[0])
        wdata = "\t" +"response = "
        if _reqmethod[0] == "GET":
            wdata += "requests.get(" + "host + url," + "headers = head"
        elif _reqmethod[0] == "POST":
            contents_write(data)
            wdata += "requests.post(" + "host + url," + "headers = head," + "data = contents"
        if cookie_status == 1:
            wdata += ",cookies = cookie)"
        else:
            wdata += ")"
        file_write(wdata)

def contents_write(data):
    wdata = "\t" + "contents = {\n"
    iterdata = iter(data)
    next(iterdata)
    tmp = ""
    for x in iterdata:
        y = re.split(": ",x.rstrip())
        try:
            tmp += (y[1])
        except:
            _allcontent = y[0].lstrip().rstrip()
    if _allcontent != "":
        _listcontent = re.split("&",_allcontent)
    else:
        pass
    for x in _listcontent:
        _separatecontents = re.split("=",x)
        wdata += ("\t\t" + "'" + _separatecontents[0] + "'" + ":" + "'" + _separatecontents[1] + "'," + "\n")
    wdata = wdata[:-2]
    wdata += "}"
    file_write(wdata)

def response_write():
        file_write("\t" + "print(response.text)" + "\n\n" + 'if __name__ == "__main__":' + "\n\t" + "req()")

def file_read(read_file,connection):
    static_write()
    cookie_status = 0
    read_file = open(read_file,"r")
    contents = read_file.readlines()
    for x in contents:
        if "Host" in x:
            host_write(x,connection)
            p = re.split(" ",contents[0])
            url_write(p[1])
        if "Cookie" in x:
            cookie_write(x)
            cookie_status = 1
    headers_write(contents)
    req_write(contents,cookie_status)
    response_write()

def arguments_parse():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i","--input",required=True,help="input file")
    ap.add_argument("-o","--output",required=True,help="output file")
    ap.add_argument("-c","--connection",default="https",help="HTTP/HTTPS (default HTTPS)")
    try:
        f = io.StringIO()
        with redirect_stderr(f):
            args = vars(ap.parse_args())
            main(args["input"],args["output"],args["connection"])
    except:
        exit(2)

def main(read_file,write_file,connection):
    file_read(read_file,connection)
    file_move(write_file)

if __name__ == "__main__":
    arguments_parse()
