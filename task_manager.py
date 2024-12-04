import json
import os
import argparse


class Task:
    """Класс для создания и отображения задачи"""

    def __init__(self, id, name, description, category, deadline, priority, status=False):
        self.id = id
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


class TaskManager:
    """Класс для управления задачами"""

    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
        self.current_id = max(task['id'] for task in self.tasks) + 1 if self.tasks else 1

    def load_tasks(self):  # загрузка существующих задач
        """Загрузка существующих задач из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='UTF-8') as file:
                    return json.load(file)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка при загрузке задач: {e}")
                return []
        return []

    def save_tasks(self):  # сохранение задачи
        """Сохранение задач в файл"""
        try:
            with open(self.filename, 'w', encoding='UTF-8') as file:
                json.dump(self.tasks, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка при сохранении задач: {e}")

    def add_task(self, name, description, category, deadline, priority):
        """Добавить задачу"""
        task = Task(id=self.current_id, name=name, description=description, category=category, deadline=deadline,
                    priority=priority)
        self.tasks.append(task.__dict__)  # Сохраняем задачу как словарь
        self.save_tasks()  # Сохраняем изменения
        self.current_id += 1  # Увеличиваем счетчик для следующей задачи

    def view_task(self, category=None):
        """Просмотр всех задач или задач по категории"""
        if not self.tasks:
            print('Задачи отсутствуют')
            return

        filter_task = self.tasks if category is None else [task for task in self.tasks if task['category'] == category]
        if not filter_task:
            print(f'Задач в категории "{category}" нет' if category else 'Задач нет')
            return

        for task in filter_task:
            print(Task(**task))

    def search_task(self, query):
        """Поиск задач по определенным критериям"""
        if not self.tasks:
            print('Задачи отсутсвуют')
            return

        #Перебираем уже существующий список и выбираем подходящий под один из критериев
        found_task = list(filter(lambda task: query.lower() in task['name'].lower() or
                                              query.lower() in task['description'].lower() or
                                              query.lower() in task['category'].lower(), self.tasks))

        if not found_task:
            print(f'Задачи,"{query}", не найдены.')
            return

        for task in found_task:
            print(Task(**task))

    def delete_task(self, task_id):
        """Удаление задачи по её индексц"""
        for x, task in enumerate(self.tasks):
            if task['id'] == task_id:
                self.tasks.pop(x)
                self.save_tasks()
                print(f"Задача удалена.")
                return
        print('Задача не найдена')

    def edit_task(self, task_id, name=None, description=None, category=None, deadline=None, priority=None,
                  status=False):
        """Изменение конкретных параметров задачи"""
        for task in self.tasks:
            if task['id'] == task_id:
                if name is not None:
                    task['name'] = name
                if description is not None:
                    task['description'] = description
                if category is not None:
                    task['category'] = category
                if deadline is not None:
                    task['deadline'] = deadline
                if priority is not None:
                    task['priority'] = priority
                if not status:
                    task['status'] = True
                self.save_tasks()
                print("Задача обновлена.")
                return
            print("Задача с таким ID не найдена.")


def main():
    parser = argparse.ArgumentParser(description='Управление задачами')
    parser.add_argument('--add', nargs=5,
                        help='Добавить задачу')
    parser.add_argument('--view', action='store_true', help='Просмотреть все задачи')
    parser.add_argument('--category', type=str, help='Категория для просмотра задач')
    parser.add_argument('--delete', type=int, metavar='id', help='Удалить задачу по ID')
    parser.add_argument('--edit', nargs='*', metavar='value',
                        help='Редактировать задачу по ID (id, [name, description, category, deadline, priority])')
    parser.add_argument('--search', type=str, help='Поиск задач по ключевому слову')

    args = parser.parse_args()
    manager = TaskManager()

    if args.add:
        name, description, category, deadline, priority = args.add
        manager.add_task(name, description, category, deadline, priority)
        print(f'Задача "{name}" добавлена.')
    elif args.view:
        manager.view_task(args.category)
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
    elif args.search:
        manager.search_task(args.search)
    else:
        print("Не указана команда. Используйте --help для получения списка доступных команд.")


if __name__ == '__main__':
    main()