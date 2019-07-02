

import pika
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
        username = "shiwei"
        pwd = 'shiwei666666'
        user_pwd = pika.PlainCredentials(username, pwd)

        # 创建连接
        self.conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))

        self.channel = self.conn.channel()

        result = self.channel.queue_declare(exclusive=True, queue= '')  # 随机生成 一个 queue , 用与 Server 发送消息
        self.callback_queue = result.method.queue

        self.channel.basic_consume(on_message_callback = self.on_response, auto_ack = True,  # 准备 发送 消息
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                                reply_to=self.callback_queue,
                                                correlation_id=self.corr_id,),
                                   body=str(n))
        while self.response is None:
            self.conn.process_data_events()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()
print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(7)
print(" [.] Got %r" % response)
