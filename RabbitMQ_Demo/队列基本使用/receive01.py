

import pika
import time
credentials = pika.PlainCredentials('shiwei', 'shiwei666666')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()

# You may ask why we declare the queue again ‒ we have already declared it in our previous code.
# We could avoid that if we were sure that the queue already exists. For example if send.py program
# was run before. But we're not yet sure which program to run first. In such cases it's a good
# practice to repeat declaring the queue in both programs.
# 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
channel.queue_declare(queue='hello')

# 定义一个回调函数，用来接收生产者发送的消息
def callback(ch, method, properties, body):
    print("received msg...start processing....",body)
    time.sleep(5)
    print(" [x] msg process done....",body)

channel.basic_consume(on_message_callback=callback, # 定义一个回调函数，用来接收生产者发送的消息
                      auto_ack=True,
                      queue='hello',                # 指定取消息的队列名
                      )

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()                           #开始循环取消息

