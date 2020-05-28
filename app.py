import easygui as gui
import pandas as pd
import os
from datetime import datetime as dt

version = '小朱发廊管理系统b1.0'

def GetCurrentTime():
    now = dt.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)

    return year+'/'+month+'/'+day+'--'+hour+':'+minute
def init():
    if not os.path.exists('./用户信息.csv'):
        frame = pd.DataFrame(columns=['phone','register_time','account'])
        frame.to_csv('./用户信息.csv',encoding='utf_8_sig',index=False)
    if not os.path.exists('./操作记录.csv'):
        frame = pd.DataFrame(columns=['phone','time','operation','value','account'])
        frame.to_csv('./操作记录.csv',encoding='utf_8_sig',index=False)

def register(now):
    phone = gui.enterbox(msg='请输入手机号码（一人一号）', title=version, default='', strip=True)
    if phone:
        if phone.isdigit()==False :
            show = '请输入正确电话号码'
            gui.msgbox(msg=show,title=version)
            return
        info = pd.read_csv('./用户信息.csv')
        if len(info.loc[info['phone']==int(phone),'account'].values)>0:
            account = str(info.loc[info['phone']==int(phone),'account'].values[0])
            show = '会员：'+phone+' 已存在，余额：'+account+' ￥'
            gui.msgbox(msg=show,title=version)
            
        else:
            with open('./用户信息.csv','a') as info:
                info.write(phone+','+now+',0\n')
            with open('./操作记录.csv','a',encoding='utf_8_sig') as log:
                log.write(phone+','+now+',创建,0,0\n')
            show = '会员：'+phone+' 于 '+now+' 创建'
            gui.msgbox(msg=show,title=version)      
def recharge(now):
    inlist = gui.multenterbox(msg='请输入账户，充值金额',title=version,fields=(['电话','充值金额']),values=('',''))
    if inlist:
        phone = inlist[0]
        value = inlist[1]
        if phone.isdigit()==False:
            show = '请输入正确电话'
            gui.msgbox(msg=show,title=version)
            return
        if value.isdigit()==False:
            show = '请输入正确金额'
            gui.msgbox(msg=show,title=version)
            return

        info = pd.read_csv('./用户信息.csv')
        if len(info.loc[info['phone']==int(phone),'account'].values)>0:
            info.loc[info['phone']==int(phone),'account'] += int(value)
            account = str(info.loc[info['phone']==int(phone),'account'].values[0])
            info.to_csv('./用户信息.csv',encoding='utf_8_sig',index=False)
            with open('./操作记录.csv','a',encoding='utf_8_sig') as log:
                log.write(phone+','+now+',充值,+'+value+','+account+'\n')

            show = '会员：'+phone+' 于 '+now+' 充值：'+value+'￥，余额：'+account+'￥'
            gui.msgbox(msg=show,title=version)
        
        else:
            show = '会员：'+phone+' 不存在'
            gui.msgbox(msg=show,title=version)
def consume(now):
    inlist = gui.multenterbox(msg='请输入账户，消费金额',title=version,fields=(['电话','消费金额']),values=('',''))
    if inlist:
        phone = inlist[0]
        value = inlist[1]
        if phone.isdigit()==False:
            show = '请输入正确电话'
            gui.msgbox(msg=show,title=version)
            return
        if value.isdigit()==False:
            show = '请输入正确金额'
            gui.msgbox(msg=show,title=version)
            return
        info = pd.read_csv('./用户信息.csv')
        if len(info.loc[info['phone']==int(phone),'account'].values)>0:
            if info.loc[info['phone']==int(phone),'account'].values[0] >= int(value):
                info.loc[info['phone']==int(phone),'account'] -= int(value)
                account = str(info.loc[info['phone']==int(phone),'account'].values[0])
                info.to_csv('./用户信息.csv',encoding='utf_8_sig',index=False)
                with open('./操作记录.csv','a',encoding='utf_8_sig') as log:
                    log.write(phone+','+now+',消费,-'+value+','+account+'\n')
                show = '会员：'+phone+' 于 '+now+' 消费：'+value+'￥，余额：'+account+'￥'
                gui.msgbox(msg=show,title=version)
            else:
                account = str(info.iloc[info.iloc[:,1]==int(电话),2].values[0])
                show = '会员: '+phone+' 余额: '+account+'￥, 余额不足！'
                gui.msgbox(msg=show,title=version) 
        else:
            show = '会员：'+phone+' 不存在'
            gui.msgbox(msg=show,title=version)

def option():
    r = gui.buttonbox(msg='请选择功能', title=version, choices=('会员注册', '充值', '消费'))
    now = GetCurrentTime()
    if r == '会员注册':
        register(now)
        return 1
    if r == '充值':
        recharge(now)
        return 1
    if r == '消费':
        consume(now)
        return 1

    return 0



init()
restart = 1
while(restart):
    restart = option()
