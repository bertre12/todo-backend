import json
import os
from typing import List


# Добавление отступов для вывода списка продуктов.
def print_with_indent(value, indent=0):
    indentation = '  ' * indent
    print(indentation + str(value))


class Entry:
    def __init__(self, title, entries=None, parent=None):
        # Для новой записи в список.
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    # Для вывода в читабельный вид.
    def __str__(self):
        return self.title

    # Вывод записей.
    def print_entries(self, indent=0):
        # Вывод записей по порядку. (через рекурсию)
        # print(self)
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent + 1)

    # Добавление новых записей.
    def add_entry(self, entry):
        self.entries.append(entry)
        # Назначение родительской записи добавляемой записи.
        entry.parent = self
        # print(f'Добавили новую запись - {entry.title}')

    # Вывод данных в формате dict через JSON.
    def json(self):
        res = {
            'title': self.title,
            'entries': []
        }
        for entry in self.entries:
            # res['entries'].append(entry.title)
            # Запись в формате JSON.
            res['entries'].append(entry.json())
        return res

    # Классметод принадлежит к классу, а не к объекту.
    @classmethod
    # Преобразование данных из JSON в словарь (dict) через рекурсию.
    def entry_from_json(cls, value: dict):
        new_entry = cls(value['title'])
        # for item in value['entry']:
        for item in value.get('entries', []):
            new_entry.add_entry(cls.entry_from_json(item))

        return new_entry

    @classmethod
    # Загрузка данных из файла.
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_json(data)

    def save(self, path):
        # Убедимся, что директория существует
        os.makedirs(path, exist_ok=True)
        # Формируем полный путь к файлу
        file_path = os.path.join(path, f'{self.title}.json')
        # Сохраняем JSON-представление в файл
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.json(), f, ensure_ascii=False, indent=4)


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries: List[Entry] = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        if not os.path.exists(self.data_path):
            return  # Если директории нет, просто выходим — нечего загружать

        for filename in os.listdir(self.data_path):
            if filename.endswith('.json'):
                full_path = os.path.join(self.data_path, filename)
                entry = Entry.load(full_path)
                self.entries.append(entry)

    # def load(self):
    #     if not os.path.isdir(self.data_path):
    #         os.makedirs(self.data_path)
    #     else:
    #         for filename in os.listdir(self.data_path):
    #             if filename.endswith('json'):
    #                 entry = Entry.load(os.path.join(self.data_path, filename))
    #                 self.entries.append(entry)
    #     return self

    def add_entry(self, title: str):
        new_entry = Entry(title)
        self.entries.append(new_entry)

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

# Создание объекта класса.
# my_entry = Entry('Продукт')
#
# # # Добавление записей напрямую.
# # my_entry.entries.append(Entry('Что-то съестное'))
#
# # Добавление записей через метод(функцию).
# # my_entry.add_entry(Entry('Что-то съестное'))
#
# # Создание объекта класса.
# meet = Entry('Мясное')
# my_entry.add_entry(meet)
#
# # Создание объекта класса.
# kolbasa = Entry('Колбаса')
# meet.add_entry(kolbasa)
#
# # Создание объекта класса.
# salami = Entry('Салями')
# kolbasa.add_entry(salami)
#
# # Создание объекта класса.
# chicken = Entry('Куриный')
# salami.add_entry(chicken)

# Вывод добавленных продуктов.(снизу вверх)
# entry = chicken
# while entry.parent:
#     print(entry)
#     entry = entry.parent


# print(my_entry)

# Вывод последней записи через вызов метода.
# my_entry.print_entries()

# print(my_entry.json())

# Вывод данных в JSON формате.
# res = my_entry.json()
# print(json.dumps(res, ensure_ascii=False, indent=4))

# Вывод преобразованных данных в словаре.
# Вызов метода из класса.
# new_entry = Entry.entry_from_json(res)
# new_entry.print_entries()

## Вывод без заголовка.
# new_entry = entry_from_json(my_entry.json())
# for child in new_entry.entries:
#     child.print_entries()
