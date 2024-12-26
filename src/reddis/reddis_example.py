# Ответ от чат бота Reddis

import redis

# Connect to Redis 
r = redis.Redis(host='localhost', port=6379, db=0)

# Add a task to the todo list 
def add_task(task):
    r.rpush('todo', task)
    print(f'Task "{task}" added to the list.')
    
    # Get all tasks from the todo list 
    def get_tasks():
        tasks = r.lrange('todo', 0, -1)
        return [task.decode('utf-8') for task in tasks] 
    
    # Remove a task from the todo list 
    def remove_task(task): 
        r.lrem('todo', 0, task) 
        print(f'Task "{task}" removed from the list.') 
        
    # Example usage add_task('Buy groceries') 
    add_task('Call the bank') 
    print('Current tasks:', get_tasks()) 
    remove_task('Buy groceries') 
    print('Updated tasks:', get_tasks())

