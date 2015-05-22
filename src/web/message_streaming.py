import datetime
from redis import StrictRedis
 
red = StrictRedis()
 
def event_stream():
    pubsub = red.pubsub()
    pubsub.subscribe('anna')
    for message in pubsub.listen():
        print message
        yield 'data: %s\n\n' % message['data']

def publish_message(user, message):
    now = datetime.datetime.now().replace(microsecond=0).time()
    aaa = u'[%s] %s: %s' % (now.isoformat(), user, message)
    print aaa
    red.publish('anna', aaa)
    event_stream()