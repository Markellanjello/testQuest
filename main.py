# Я хотел сделать совсем без сторонних библиотек, но pandas тут идеально подходит
import pandas as pd


def main():
    # Функция проверки согласия, обернул в функцию потому что можно применить не только для удаления но и для редактирования
    def askq(data):
        ask = str(input(f"Вы точно хотите сделать это c {data}? да/нет - "))
        if ask == "да" or ask == "Да":
            return 1
        elif ask == "Нет" or ask == "нет":
            return 0
        else:
            print("Повторите ответ)")
            askq(data)
    # Функция просто вывода данных
    def show_directory():
        df = pd.read_csv('directory.txt',
                         names=['фамилия', 'имя', 'отчество', 'название организации', 'телефон личный',
                                'телефон рабочий'])
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.options.display.expand_frame_repr = False
        print(df)

    # Функция поиска по "базе" статьи
    def search_dir():
        search = str(input("Введите данные для поиска через запятую например - Иванов, 8991411414141 : ")).split(", ")
        f = open('directory.txt', "r", encoding='utf-8')
        data = f.readlines()
        arr = []
        for el in data:
            res = 1 if (all(x in el for x in search)) else 0
            if res == 1:
                arr.append(el.replace('\n', "").split(","))
        df = pd.DataFrame(arr, columns=['фамилия', 'имя', 'отчество', 'название организации', 'телефон личный (сотовый)', 'телефон рабочий'])
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.options.display.expand_frame_repr = False
        print(df)


    # Функция добавления статьи
    def directory_dump():
        f = open('directory.txt', "a", encoding='utf-8')
        person = str(input("Введите данные через запятую, в таком порядке - 'фамилия', 'имя', 'отчество', 'название организации', 'телефон личный (сотовый)', 'телефон рабочий', для выхода введите exit: ")) + "\n"
        if person == "exit":
            return
        f.write(person)

    # Функция редактирование статьи
    def directory_edit():
        show_directory()
        f = open('directory.txt', "r", encoding='utf-8')
        index = int(input("Введите индекс строки которую хотите редактировать: "))
        if index == "exit":
            return
        data = f.readlines()
        el = data[index]
        red = str(input(f"Вы хотите отредактировать - {el}, введите новые данные в том же формате, для выхода введите exit: ")) + "\n"
        if red == "exit":
            return
        full_data = "".join(data).replace(el, red)
        f = open('directory.txt', "w", encoding='utf-8')
        f.write(full_data)

    # Функция удаления строки/элемента справочника
    def directory_delete():
        show_directory()
        f = open('directory.txt', "r", encoding='utf-8')
        index = int(input("Введите индекс строки которую хотите удалить, для выхода введите exit: "))
        if index == "exit":
            return
        data = f.readlines()
        ask = askq(data[index])
        if ask == 0:
            return
        data.pop(index)
        data = ''.join(data)
        f = open('directory.txt', "w", encoding='utf-8')
        f.write(data)

    # Панель команд реализована через if else что бы не усложнять
    def choose_command():
        try:
            print("Список команд: show, edit, dump, delete, search, exit: ")
            command = str(input("Введите команду: "))
            if command == "show":
                show_directory()
                choose_command()
            elif command == "edit":
                directory_edit()
                choose_command()
            elif command == "dump":
                directory_dump()
                choose_command()
            elif command == "delete":
                directory_delete()
                choose_command()
            elif command == "search":
                search_dir()
                choose_command()
            elif command == "exit":
                return
            else:
                print('Ха-ха, смешно, я не понял...')
                choose_command()
        except Exception as e:
            print(e)
        finally:
            print("Пока, приятно было заносить данные вместе с тобой")
    # Вызов консольного меню
    choose_command()

# Точка входа
if __name__ == "__main__":
    main()