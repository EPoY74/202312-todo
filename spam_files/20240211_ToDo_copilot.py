class Todo:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def view_tasks(self):
        for task in self.tasks:
            print(task)

    def remove_task(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
            
my_todo = Todo()


print(my_todo.tasks)
my_todo.add_task("Найти что-то")
print(my_todo.tasks)
my_todo.add_task("Еще одно задание")
print(my_todo.tasks)
my_todo.view_tasks()
