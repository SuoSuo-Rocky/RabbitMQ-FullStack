import pika
import sys

username = "shiwei"
pwd = 'shiwei666666'
user_pwd = pika.PlainCredentials(username, pwd)

# 创建连接
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))

channel = conn.channel()

channel.exchange_declare(exchange='topic_logs',
                         exchange_type='topic')  # 声明exchange的类型为模糊匹配。

result = channel.queue_declare(exclusive=True,
                               queue="",)        # 创建随机一个队列当消费者退出的时候，该队列被删除。
queue_name = result.method.queue                 # 创建一个随机队列名字。

# 绑定键。‘#’匹配所有字符，‘*’匹配一个单词。这里列表中可以为一个或多个条件，能通过列表中字符匹配到的消息，消费者都可以取到
binding_keys = ['[warn].*', 'info.*']
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

# 通过循环绑定多个“交换机-队列-关键字”，只要消费者在rabbitmq中能匹配到与关键字相应的队列，就从那个队列里取消息
for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(on_message_callback=callback,
                      queue=queue_name,
                      auto_ack=True)       # 不给rabbitmq发送确认

channel.start_consuming()                  # 循环接收消息

