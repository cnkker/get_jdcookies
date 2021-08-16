# -*- coding: utf-8 -*-
# Written by 龍天昌盛  QQ:256051
import sys
import json
import time
import requests
import logging
import qrcode
import os
import psutil
requests.packages.urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

jd_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 SP-engine/2.14.0 main%2F1.0 baiduboxapp/11.18.0.16 (Baidu; P2 13.3.1) NABar/0.0'
js_url= 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state={0}&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'
referer_url='https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state={0}&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'
returnurl_url='https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action'
token_url='https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?s_token={0}&v={1}&remember=true'
qrcode_url='https://plogin.m.jd.com/cgi-bin/m/tmauth?appid=300&client_type=m&token={0}'

def GetCookiesExit1():
  print("程序5秒后自动退出")
  time.sleep(5)
  sys.exit()
  
def kill_process():
  for proc in psutil.process_iter():
    try:
      s = proc.name()
      if s == 'FSViewer.exe':
        proc.kill()
      elif s:
        pass
      else:
        proc.kill()
    except:
      proc.kill()


def token_get():
    t = round(time.time())
    headers = {
        'User-Agent': jd_ua,
        'referer': referer_url.format(t)
    }
    t = round(time.time())
    url = js_url.format(t)
    res = s.get(url=url, headers=headers, verify=False)
    res_json = json.loads(res.text)
    s_token = res_json['s_token']
    token_post(s_token)
    # return s_token


def token_post(s_token):
    t = round(time.time() * 1000)
    headers = {
        'Connection': 'Keep-Alive',
        'User-Agent': jd_ua,
        'referer': referer_url.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = token_url.format(s_token, t)

    data = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': returnurl_url.format(t),
        'source': 'wq_passport'
        }
    res = s.post(url=url, headers=headers, data=data, verify=False)
    # print(res.text)
    res_json = json.loads(res.text)
    token = res_json['token']
    # print("token:", token)
    c = s.cookies.get_dict()
    okl_token = c['okl_token']
    # print("okl_token:", okl_token)
    qrurl = qrcode_url.format(token)
    qrcodeb = qrcode.make(qrurl)
    qrcodeb.save("JDMobQRcode.png")
    logger.info("二维码图片 JDMobQRcode.png 已生成到该目录下,请后台运行程序,电脑打开图片后用京东APP扫码登录")
    os.system('start "" "JDMobQRcode.png"')

    logger.info("请手动复制链接到在线二维码生成网站,并扫码登录")
    logger.info('')
    logger.info(qrurl)
    logger.info('')
    check_token(token, okl_token)


def check_token(token, okl_token):
    t = round(time.time() * 1000)
    headers = {
        'User-Agent': jd_ua,
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?&token={0}&ou_state=0&okl_token={1}'.format(token, okl_token)
    data = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action'.format(t),
        'source': 'wq_passport',
    }
    res = s.post(url=url, headers=headers, data=data, verify=False)
    check = json.loads(res.text)
    code = check['errcode']
    message = check['message']
    global i
    while code == 0:
        logger.info("扫码成功")
        jd_ck = s.cookies.get_dict()
        pt_key = 'pt_key=' + jd_ck['pt_key']
        pt_pin = 'pt_pin=' + jd_ck['pt_pin']
        ck = str(pt_key) + ';' + str(pt_pin) + ';'
        logger.info(ck)
        with open("ck.txt", "a") as jdcookies:
            jdcookies.write(ck + '\n')       
        os.remove('JDMobQRcode.png')
        break
    else:
        i = i + 1
        if i < 60:
            logger.info(message)
            time.sleep(3)
            check_token(token, okl_token)
        else:
            exit(0)


if __name__ == '__main__': 
    logger.info("JD扫码获取Cookie")
    i = 1
    s = requests.session()
    token_get()
    time.sleep(5)
    sys.exit()