import json
import os
from datetime import datetime

FILENAME = "tasks.json"

# Функция для загрузки задач из файла
def load_tasks(filename=FILENAME):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as file:
            return json.load(file)
    return []

# Функция для сохранения задач в файл
def save_tasks(tasks, filename=FILENAME):
    with open(filename, 'w') as file:
        sorted_tasks = sorted(tasks, key=lambda x: x['done'])
        json.dump(sorted_tasks, file, indent=4, ensure_ascii=False)

# Функция для добавления новой задачи
def add_task(tasks, task_text):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks.append({"text": task_text, "done": False, "date_added":current_time})
    save_tasks(tasks)
    print(f"Задача '{task_text}' добавлена.")

# Функция для вывода списка задач
def list_tasks(tasks):
    if not tasks:
        print("Список задач пуст.")
    else:
        sorted_tasks = sorted(tasks, key=lambda x: (x['done'], datetime.strptime(x['date_added'], "%Y-%m-%d %H:%M:%S")))

        for i, task in enumerate(sorted_tasks, start=1):
            status = "[+]" if task["done"] else "[ ]"
            print(f"{i}. {status} {task['text']} (добавлена {task['date_added']})")

# Функция для отметки задачи как выполненной
def mark_task_done(tasks, task_number):
    try:
        tasks[task_number - 1]["done"] = True
        save_tasks(tasks)
        print(f"Задача {task_number} отмечена как выполненная.")
    except IndexError:
        print("Неверный номер задачи.")


# Функция для удаления задачи
def delete_task(tasks, task_number):
    try:
        deleted_task = tasks.pop(task_number - 1)
        save_tasks(tasks)
        print(f"Задача '{deleted_task['text']}' удалена.")
    except IndexError:
        print("Неверный номер задачи.")

# Главная функция для обработки команд
def main():
    tasks = load_tasks()
    print("Добро пожаловать в Todo List! Введите команду (add, list, done, delete) или 'exit' для выхода.")

    while True:
        command = input("> ").strip().split(maxsplit=1)
        action = command[0].lower()

        if action == "add":
            if len(command) > 1:
                add_task(tasks, command[1])
            else:
                print("Ошибка: укажите текст задачи после команды 'add'.")

        elif action == "list":
            list_tasks(tasks)

        elif action == "done":
            if len(command) > 1 and command[1].isdigit():
                mark_task_done(tasks, int(command[1]))
            else:
                print("Ошибка: укажите номер задачи после команды 'done'.")
        elif action == "delete":
            if len(command) > 1 and command[1].isdigit():
                delete_task(tasks, int(command[1]))
            else:
                print("Ошибка: укажите номер задачи после команды 'delete'.")

        elif action == "exit":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Неизвестная команда. Доступные команды: add, list, done, delete, exit.")

# Запуск программы
if __name__ == "__main__":
    main()
