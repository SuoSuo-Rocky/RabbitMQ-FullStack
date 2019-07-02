import pika

username = "shiwei"
pwd = 'shiwei666666'
user_pwd = pika.PlainCredentials(username, pwd)
# 创建连接
conn = pika.BlockingConnection(pika.ConnectionParameters("localhost", credentials=user_pwd))
channel = conn.channel()

print(' [*] Waiting for n')
channel.queue_declare(queue='compute_queue')

# 将n值加1
def increase(n):
    return n + 1

# 定义接收到消息的处理方法
def request(ch, method, properties, body):
    print(" [.] increase(%s)" % (body,))

    response = increase(int(body))

    # 将计算结果发送回控制中心
    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_message_callback=request,
                      queue='compute_queue')

channel.start_consuming()