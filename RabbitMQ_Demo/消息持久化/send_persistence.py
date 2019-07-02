

import pika
import sys

username = "shiwei"
pwd = 'shiwei666666'
user_pwd = pika.PlainCredentials(username, pwd)

# 创建连接
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))
chann = conn.channel()

# 源码：
"""
#     def queue_declare(self,            # channel.queueDeclare 用来创建队列，有5个参数：
#                       queue,           # String queue, 队列名；
#                       passive=False,   # 
#                       durable=False,   # boolean durable, 该队列是否需要持久化
#                       exclusive=False, # boolean exclusive,该队列是否为该通道独占的（其他通道是否可以消费该队列）
#                       auto_delete=False, # boolean autoDelete,该队列不再使用的时候，是否让RabbitMQ服务器自动删除掉；
#                       arguments=None)

"""
chann.queue_declare(queue='test_tags', # 声明 队列， 不可与 已存在的 队列重名 ， 否则 报错
                    durable=True,      # 设置队列 持久化 ， 报 ： ChannelClosedByBroker: 406 ， 错误， passive：是屈服的意思，将passive设为True，问题解决。
                    # passive= True,
                    )
message = "My name is shiwei"

chann.basic_publish(exchange='',
                    routing_key='test_tags',                              # 表明 要将 消息 发送到哪个队列
                    body = message,
                    properties = pika.BasicProperties(delivery_mode = 2)  # 设置消息持久化， 将消息的属性设置为 2 ，表示消息持久化
                    )

print('[Publisher] Send %s' % message)
conn.close()




