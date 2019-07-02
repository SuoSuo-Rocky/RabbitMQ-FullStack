

import pika
import sys

username = "shiwei"
pwd = 'shiwei666666'
user_pwd = pika.PlainCredentials(username, pwd)

# 创建连接
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))

#在连接上创建一个频道
channel = conn.channel()

channel.exchange_declare(exchange="direct_logs", exchange_type="direct") # 参数 名改变了， 以前是 type

result = channel.queue_declare(exclusive=True,  # 创建随机队列，当消费者与rabbitmq断开连接时，这个队列将自动删除。
                               queue='',
                      )
queue_name = result.method.queue # 分配随机队列的名字。

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:                # 循环 队列， 使其与交换机绑定在一起，
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity
                       )

def callback(ch, method, properties, body):   #  定义回调函数，接收消息
    print(" [消费者] %r:%r" % (method.routing_key, body))

channel.basic_consume(queue=queue_name,
                      on_message_callback = callback,
                      auto_ack=True) # 消费者接收消息后，不给rabbimq回执确认。

channel.start_consuming() # 循环等待消息接收。