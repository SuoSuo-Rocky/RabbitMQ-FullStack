
import pika

class Center(object):
    def __init__(self):
        username = "shiwei"
        pwd = 'shiwei666666'
        user_pwd = pika.PlainCredentials(username, pwd)

        # 创建连接
        self.conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))

        self.channel = self.conn.channel()
        # 定义接收返回消息的队列
        result = self.channel.queue_declare(exclusive=True,queue="",)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(on_message_callback=self.on_response,
                                   auto_ack=True,
                                   queue=self.callback_queue)

    # 定义接收到返回消息的处理方法
    def on_response(self, ch, method, props, body):
        self.response = body

    def request(self, n):
        self.response = None
        # 发送计算请求，并声明返回队列
        self.channel.basic_publish(exchange='',
                                   routing_key='compute_queue',
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                   ),
                                   body=str(n))
        # 接收返回的数据
        while self.response is None:
            self.conn.process_data_events()
        return int(self.response)

center = Center()

print(" [x] Requesting increase(30)")
response = center.request(30)
print(" [.] Got %r" % (response,))
