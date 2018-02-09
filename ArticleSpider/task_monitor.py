# -*- coding: utf-8 -*-  
__author__ = "wangxuan"

try:
    import MySQLdb
except:
    import pymysql as MySQLdb

import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def connectMarketing():
    print('连接到marketing的mysql服务器...')
    connect = MySQLdb.connect('139.199.168.194', 'pagoda', 'Pagoda@123', 'marketing')
   # connect = MySQLdb.connect('10.8.13.15', 'marketing', 'HW5F2CPKJIvwWzjO', 'marketing_business')
    print('连接成功')
    return connect

def queryRecord(connect):
    cursor = connect.cursor()

    # 查询优惠券任务总数
    couponCountSql = "select count(*) from tb_e_coupon_task where createDate > timestamp(date(sysdate()));"
    cursor.execute(couponCountSql)
    couponCount = cursor.fetchone()[0]
    print("优惠券任务总数：", couponCount)

    # 查询优惠券失败任务
    couponFailTaskSql = "select count(*) from tb_e_coupon_task where createDate > timestamp(date(sysdate())) " \
                        "and couponTaskStatus = 30;"
    cursor.execute(couponFailTaskSql)
    failCouponCount = cursor.fetchone()[0]
    print("优惠券失败任务总数：", failCouponCount)

    couponFailRecord = ''
    if failCouponCount > 0:
        couponFailRecordSql = "select group_concat(id) from tb_e_coupon_task where createDate > timestamp(date(sysdate())) " \
                              "and couponTaskStatus = 10;"
        cursor.execute(couponFailRecordSql)
        couponFailRecord = cursor.fetchone()[0]

    # 查询优惠券执行中任务
    couponProcessTaskSql = "select count(*) from tb_e_coupon_task where createDate > timestamp(date(sysdate())) " \
                        "and couponTaskStatus = 10;"
    cursor.execute(couponProcessTaskSql)
    processCouponCount = cursor.fetchone()[0]
    print("优惠券执行中任务总数：", failCouponCount)

    couponprocessRecord = ''
    if processCouponCount > 0:
        couponProcessRecordSql = "select group_concat(id) from tb_e_coupon_task where createDate > timestamp(date(sysdate())) " \
                              "and couponTaskStatus = 10"
        cursor.execute(couponProcessRecordSql)
        couponprocessRecord = cursor.fetchone()[0]

    # 短信任务总数
    smsCountSql = "select count(*) from tb_e_message_task where createDate > timestamp(date(sysdate()));"

    cursor.execute(smsCountSql)
    smsCount = cursor.fetchone()[0]
    print("短信任务总数：", smsCount)

    # 短信失败任务
    smsFailCountSql = "select count(*) from tb_e_message_task where createDate > timestamp(date(sysdate())) " \
                        "and messageTaskStatus = 30;"
    cursor.execute(smsFailCountSql)
    failSmsCount = cursor.fetchone()[0]
    print("短信失败任务总数：", failSmsCount)

    smsFailRecord = ''
    if failSmsCount > 0:
        smsFailRecordSql = "select group_concat(id) from tb_e_message_task where createDate > timestamp(date(sysdate())) " \
                              "and messageTaskStatus = 30"
        cursor.execute(smsFailRecordSql)
        smsFailRecord = cursor.fetchone()[0]

    # 短信执行中任务
    smsProcessCountSql = "select count(*) from tb_e_message_task where createDate > timestamp(date(sysdate())) " \
                      "and messageTaskStatus = 10;"
    cursor.execute(smsProcessCountSql)
    processSmsCount = cursor.fetchone()[0]
    print("短信执行中任务总数：", processSmsCount)

    smsProcessRecord = ''
    if processSmsCount > 0:
        smsProcessRecordSql = "select group_concat(id) from tb_e_message_task where createDate > timestamp(date(sysdate())) " \
                           "and messageTaskStatus = 10"
        cursor.execute(smsProcessRecordSql)
        smsProcessRecord = cursor.fetchone()[0]

    connect.commit()

    list = [couponCount, failCouponCount, couponFailRecord, processCouponCount, couponprocessRecord, smsCount,
            failSmsCount, smsFailRecord, processSmsCount, smsProcessRecord]

    return list

def connectMonitor():
    print('连接到monitor的mysql服务器...')
    connect = MySQLdb.connect('localhost', 'root', 'wang', 'test')
 #   connect = MySQLdb.connect('localhost', 'root', '123456', 'monitor')
    print('连接成功！')
    return connect

def insertRecord(connect, records):
    cursor = connect.cursor()

    insertSql = """insert into task_monitor(couponTaskNum, failCouponTaskNum, failCouponTaskIds, processCouponTaskNum, 
                processCouponTaskIds, smsTaskNum, failSmsTaskNum, failSmsTaskIds, processSmsTaskNum, processSmsTaskIds)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    cursor.execute(insertSql, (records[0], records[1], records[2], records[3], records[4], records[5],
                               records[6], records[7], records[8], records[9]))
    connect.commit()

def closeMarketing(connect):
    connect.close()

def closeMonitor(connect):
    connect.close()


from email.header import Header


from email.mime.text import MIMEText
import smtplib
import datetime
def sendEmail(content):

    from_addr = "632476773@qq.com"
    password = "htmteppnboyebfce"
    smtp_server = "smtp.qq.com"
    to_addr = ["demons_wx@163.com", "wangxuan9728@163.com"]

    msg = MIMEText(content, 'plain', 'utf-8')
 #   msg['From'] = '王瑄' % to_addr
    title = '活动执行监控-' + str(datetime.date.today())
    msg['Subject'] = Header(title)

    server = smtplib.SMTP_SSL(smtp_server, 465)
  #  server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()




def main():
    marketing = connectMarketing()

    list = queryRecord(marketing)

    monitor = connectMonitor()
    insertRecord(monitor, list)

    closeMonitor(monitor)
    closeMarketing(marketing)

    content = "你好，今日活动执行情况如下，优惠券任务共" + str(list[0]) + "个，失败" + str(list[1]) + "个，" + str(list[3]) + "个仍在执行。" \
              "短信任务共" + str(list[5]) + "个，失败" + str(list[6]) + "个， " + str(list[8]) + "个仍在执行！"
    if list[1] > 0 or list[6] > 0:
        content = content + "有失败任务，请关注！"
    else:
        content = content + "一切正常，新年快乐！"

    print(content)
 #   sendEmail(content)


if __name__ == "__main__":
    main()


