

import pika

username = "shiwei"
pwd = 'shiwei666666'
user_pwd = pika.PlainCredentials(username, pwd)

# 创建连接
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))

#在连接上创建一个频道
channel = conn.channel()

#创建一个fanout(广播)类型的交换机exchange，名字为logs。
channel.exchange_declare(exchange="logs", exchange_type="fanout")
message =  "info: Hello World!"
channel.basic_publish(exchange='logs',# 指定交换机exchange为logs，这里只需要指定将消息发给交换机logs就可以了，不需要指定队列，因为生产者消息是发送给交换机的。
                      routing_key='', # 在fanout类型中，绑定关键字routing_key必须忽略，写空即可
                      body=message)
print(" [x] Sent %r" % message)
conn.close()

