import json
import argparse


class Task:
    id = 1

    def __init__(self, name, description, category, deadline, priority, status=False):
        self.id = Task.id
        Task.id += 1
        self.name = name
        self.description = description
        self.category = category
        self.deadline = deadline
        self.priority = priority
        self.status = status

    def __str__(self):
        return f"""Задача: {self.name}
Описание: {self.description}
Категория: {self.category}
Срок: {self.deadline}
Приоритет: {self.priority}
Статус: {self.status}"""


class TaskSaveLoad:
    """Загрузка и сохранение задач"""

    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, 'r', encoding='UTF-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print('Ошибка при загрузке задач')
            return []

    def save_tasks(self):
        try:
            with open(self.filename, 'w', encoding='UTF-8') as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка сохранения задачи: {e}")

    def add_task(self, name, description, category, priority, deadline):
        task = Task(name, description, category, priority, deadline)
        self.tasks.append(task.__dict__)
        self.save_tasks()

    def view_task(self, category=None):
        """Просмотр всех задач или задач с определенными параметрами"""
        print(*self.get_task(category), sep='\n')

    def get_task(self, category):  # вспомогательный метод
        return list(filter(lambda task: category in list(task.values()), self.tasks) if category else self.tasks)

    def delete_task(self, param):
        """Удаление задач по одному из параметров"""
        del_task = self.get_task(param)
        if del_task:
            self.tasks.remove(del_task[0])
            self.save_tasks()

    def edit_task(self, task_id, name=None, description=None, category=None, deadline=None, priority=None, status=None):
        """Изменение конкретных параметров задачи"""
        ed_task = self.get_task(task_id)[0]
        if ed_task:
            s1 = ('name', 'description', 'category', 'deadline', 'priority', 'status')
            s2 = (name, description, category, deadline, priority, status)
            ed_task.update({i[0]: i[1] for i in zip(s1, s2) if i[1] is not None})
            self.save_tasks()


def main():
    parser = argparse.ArgumentParser(description='Управление задачами')
    parser.add_argument('--add', nargs=5, help='Добавить задачу (name, description, category, deadline, priority)',
                        required=False)
    parser.add_argument('--view', action='store_true', help='Просмотреть все задачи')
    parser.add_argument('--category', type=str, help='Категория для просмотра задач')
    parser.add_argument('--delete', type=int, metavar='id', help='Удалить задачу по ID')
    parser.add_argument('--edit', nargs='*', metavar='value',
                        help='Редактировать задачу по ID (id, [name, description, category, deadline, priority])')
    args = parser.parse_args()
    manager = TaskSaveLoad()

    if args.add:
        name, description, category, deadline, priority = args.add
        manager.add_task(name, description, category, deadline, priority)
        print(f'Задача "{name}" добавлена.')
    elif args.view:
        if args.category:
            manager.view_task(args.category)
        else:
            manager.view_task()
    elif args.delete is not None:
        manager.delete_task(args.delete)
    elif args.edit:
        task_id = int(args.edit[0])  # ID задачи
        name = args.edit[1] if len(args.edit) > 1 else None
        description = args.edit[2] if len(args.edit) > 2 else None
        category = args.edit[3] if len(args.edit) > 3 else None
        deadline = args.edit[4] if len(args.edit) > 4 else None
        priority = args.edit[5] if len(args.edit) > 5 else None
        manager.edit_task(task_id, name, description, category, deadline, priority)

    else:
        print("Не указана команда. Используйте --help для получения списка доступных команд.")


if __name__ == '__main__':
    main()