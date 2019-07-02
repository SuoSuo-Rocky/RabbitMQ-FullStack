#  发送端， 消费者
import pika

credentials = pika.PlainCredentials('shiwei', 'shiwei666666')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))

# 在连接之上创建一个 rabbit 协议的通道
channel = connection.channel()

# 在通道中 声明 一个 queue
channel.queue_declare(queue='hello')

# 一个消息永远不能直接发送到队列，它总是需要经过一个交换
# n RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
channel.basic_publish(exchange='',  # 交换机
                      routing_key='hello',   # 路由键，写明将消息发往哪个队列，本例是将消息发往队列hello
                      body='Hello World!')   # 生产者要发送的消息 内容
print(" [x] Sent 'Hello World!'")
connection.close()  # 当生产者发送完消息后，可选择关闭连接

