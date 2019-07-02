

import pika
import time

username = "shiwei"
pwd = 'shiwei666666'
user_pwd = pika.PlainCredentials(username, pwd)

# 创建连接
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))

chann = conn.channel()

chann.queue_declare(queue='test_tags',  # 声明 队列， 不可与 已存在的 队列重名 ， 否则 报错
                    durable=True,       # 设置队列 持久化 ，
                    # passive=True,     # 是否检查当前队列 是否存在 ， True 表示 当前声明队列 为 存在 的，
                    )
# 定义 接受消息 的 回调函数
def callback(ch,method, properties, body):
    print(" [消费者] Received %r" % body)
    time.sleep(3)
    print(" [消费者] Done")
    # 手动 确认  在接收到 消息后 给 rabbitmq 发送一个 确认 ACK, 返回 消息标识符
    ch.basic_ack(delivery_tag=method.delivery_tag)
"""
    def basic_consume(self,
                      queue,
                      on_message_callback,
                      auto_ack=False,
                      exclusive=False,
                      consumer_tag=None,
                      arguments=None):
"""
# 注意 源码中的 位置参数的位置
chann.basic_consume(queue='test_tags',
                    on_message_callback = callback,
                    # 是否 需要 自动 确认， 若为 False, 则需要在 消息回调函数中手动确认，
                    auto_ack = False,  # 默认是  False
                    )

chann.start_consuming()  # 开始 循环 接受消息

