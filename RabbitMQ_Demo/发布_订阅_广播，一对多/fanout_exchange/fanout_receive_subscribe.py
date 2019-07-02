

import pika
import sys

username = "shiwei"
pwd = 'shiwei666666'
user_pwd = pika.PlainCredentials(username, pwd)

# 创建连接
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))

#在连接上创建一个频道
channel = conn.channel()

channel.exchange_declare(exchange="logs", exchange_type="fanout")  # 参数名改变了，以前版本是 type

result = channel.queue_declare(exclusive=True,  # 创建随机队列，exclusive=True（唯一性）当消费者与rabbitmq断开连接时，这个队列将自动删除。
                               queue='',)

queue_name = result.method.queue # 分配随机队列的名字。
channel.queue_bind(exchange='logs',# 将交换机、队列绑定在一起，
                   queue=queue_name,)

def callback(ch, method, properties, body):   #  定义回调函数，接收消息
    print(" [消费者] %r:%r" % (method.routing_key, body))

channel.basic_consume(queue=queue_name,
                      on_message_callback = callback,
                      auto_ack=True) # 消费者接收消息后，不给rabbimq回执确认。

channel.start_consuming() # 循环等待消息接收。