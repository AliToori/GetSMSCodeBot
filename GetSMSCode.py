#!/usr/bin/env python3

import requests
import urllib.parse


class getsmscode:
    def req(self, args, endpoint):
        if not endpoint in [1, 2]:
            raise Exception('Endpoint must be 1 or 2.')
        if endpoint == 1:
            return requests.get(self.endpoint1 + urllib.parse.urlencode(args)).text
        elif endpoint == 2:
            return requests.get(self.endpoint2 + urllib.parse.urlencode(args)).text

    def __init__(self, username, token):
        self.endpoint1 = 'http://www.getsmscode.com/usdo.php?'
        self.endpoint2 = 'http://www.getsmscode.com/do.php?'
        res = self.req({'action': 'login', 'username': username, 'token': token}, 1)
        if res == 'username is wrong':
            raise Exception(res)
        elif res == 'token is wrong':
            raise Exception(res)
        else:
            self.username = username
            self.token = token
            return None

    def get_balance(self):
        res = self.req({'action': 'login', 'username': self.username, 'token': self.token}, 1)
        aargs = res.split('|')
        if not aargs[1]:
            raise Exception(res)
        return aargs[1]

    def get_number(self, pid, cocode):
        if cocode == 'us':
            res = self.req({'action': 'getmobile', 'username': self.username, 'token': self.token, 'pid': pid}, 1)
        else:
            res = self.req(
                {'action': 'getmobile', 'username': self.username, 'token': self.token, 'pid': pid, 'cocode': cocode},
                2)
        if res.isdigit():
            return res
        raise Exception(res)

    def get_sms(self, number, pid, cocode):
        if cocode == 'us':
            res = self.req(
                {'action': 'getsms', 'username': self.username, 'token': self.token, 'pid': pid, 'mobile': number,
                 'author': self.username}, 1)
        else:
            res = self.req(
                {'action': 'getsms', 'username': self.username, 'token': self.token, 'pid': pid, 'mobile': number,
                 'cocode': cocode}, 2)
        if res.startswith('1|'):
            return res.replace('1|', '')
        return False

    def add_blacklist(self, number, pid, cocode):
        if cocode == 'cn':
            res = self.req(
                {'action': 'addblack', 'username': self.username, 'token': self.token, 'pid': pid, 'mobile': number}, 1)
        else:
            res = self.req(
                {'action': 'addblack', 'username': self.username, 'token': self.token, 'pid': pid, 'mobile': number,
                 'cocode': cocode}, 2)
        if res == 'Message|Had add black list':
            return True
        return False


api = getsmscode.getsmscode('sdfsd@gmail.com', 'sdfsdfe8cffce5') #username = email, token can be found on the homepage @ getsmscode.com
print('My balance is: ' + str(api.get_balance())) #print balance

# #get a US (+1) number for Gmail
number = api.get_number(1, 'us')
print('Requested phone number is +' + str(number))
#loop until an sms received of for Google PID:1
print('Waiting code...')
sms = api.get_sms(number, 1, 'us')
while not sms:
    time.sleep(5)
    sms = api.get_sms(number, 1, 'us')
#print the received sms
print('Got sms:', sms)