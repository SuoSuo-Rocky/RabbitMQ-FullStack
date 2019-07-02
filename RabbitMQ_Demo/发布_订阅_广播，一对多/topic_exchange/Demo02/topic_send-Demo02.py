import pika
import sys

username = "shiwei"
pwd = 'shiwei666666'
user_pwd = pika.PlainCredentials(username, pwd)

# 创建连接
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))

channel = conn.channel()
channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')  # 创建模糊匹配类型的exchange。。

routing_key = '[warn].kern' # 这里关键字必须为点号隔开的单词，以便于消费者进行匹配。引申：这里可以做一个判断，判断产生的日志是什么级别，然后产生对应的routing_key，使程序可以发送多种级别的日志
message =  'Hello World!'
channel.basic_publish(exchange='topic_logs',#将交换机、关键字、消息进行绑定
                      routing_key=routing_key,  # 绑定关键字，将队列变成[warn]日志的专属队列
                      body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
conn.close()