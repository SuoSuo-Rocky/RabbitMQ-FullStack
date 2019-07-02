

import pika
import sys

username = "shiwei"
pwd = 'shiwei666666'
user_pwd = pika.PlainCredentials(username, pwd)

# 创建连接
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))

#在连接上创建一个频道
channel = conn.channel()

#创建一个交换机并声明 direct 的类型为：关键字类型，表示该交换机会根据消息中不同的关键字将消息发送给不同的队列
channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

severity = sys.argv[1] if len(sys.argv) > 1 else "info"

message = ' '.join(sys.argv[2:]) or "Hello World!"

channel.basic_publish(exchange='direct_logs', # 指明用于发布消息的交换机、关键字
                      routing_key=severity,   # 绑定关键字，即将message与关键字info绑定，明确将消息发送到哪个关键字的队列中。
                      body=message)
print(" [x] Sent %r" % message)
conn.close()

