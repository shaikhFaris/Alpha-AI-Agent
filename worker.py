import redis
import pprint
import json
import time
from agent import init_agent
queue_name = "alphaQ"
try:
    # Connect to Redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    print("connected to redis")
except Exception as e:
    print("Could  not connect to redis"+e)
    exit()

print("waiting for tasks...")
i=0
while i<3:
    raw_task = r.brpop(queue_name, timeout=3)  # blocks until a task arrives or timeout
    if raw_task:
        queue, task_json = raw_task
        task = json.loads(task_json)
        print("Processing task:")
        pprint.pprint(task)
        init_agent(task)

    else:
        print("No tasks, waiting...")
        time.sleep(2) 
        i=i+1