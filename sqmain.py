import sqlite3 as sq
import pandas as pd
def main():
    con = sq.connect('directory.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS directory (id INTEGER PRIMARY KEY AUTOINCREMENT, surname TEXT, name TEXT, father_name TEXT, org_name TEXT, phone_pub TEXT, work_phone TEXT)""")

    # Сохранил пару строк за счет этой функции
    def sqlaaaa(command):
        cur.execute(command)
        con.commit()

    # Функция вывода dataFrame
    def pd_show(data):
        df = pd.DataFrame(data, columns=['id', 'фамилия', 'имя', 'отчество', 'название организации', 'телефон личный', 'телефон рабочий'])
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.options.display.expand_frame_repr = False
        print(df)

    #Функция поиска
    def search_dir():
        search = input("Введите данные для поиска через запятую например - Иванов, 8991411414141: ").split(", ")
        query = cur.execute("SELECT * FROM directory WHERE " + " OR ".join([f"{col} LIKE '%{item}%'" for col in ['id', 'surname', 'name', 'father_name', 'org_name', 'phone_pub', 'work_phone'] for item in search])).fetchall()
        pd_show(query)

    #Функция добавления
    def directory_dump():
        person = input(
            "Введите данные через запятую, в таком порядке - 'фамилия', 'имя', 'отчество', 'название организации', 'телефон личный (сотовый)', 'телефон рабочий', для выхода введите exit: ").split(", ")
        if person[0] == "exit": return
        sqlaaaa(f"INSERT INTO directory (surname, name, father_name, org_name, phone_pub, work_phone) VALUES ('{person[0]}', '{person[1]}', '{person[2]}', '{person[3]}', '{person[4]}', '{person[5]}')")

    #Функция редактирования
    def directory_edit(all_data):
        pd_show(all_data)
        index = input("Введите индекс строки, которую хотите редактировать, для выхода введите exit: ")
        if index == "exit": return
        data = cur.execute(f"SELECT * FROM directory WHERE id={int(index)}").fetchone()
        person = input(f"Вы собираетесь редактировать - {data} Введите данные через запятую, в том же формате: ").split(", ")
        sqlaaaa(f"UPDATE directory SET surname='{person[0]}', name='{person[1]}', father_name='{person[2]}', org_name='{person[3]}', phone_pub='{person[4]}', work_phone='{person[5]}' WHERE id={index}")

    #Функция Удаления
    def directory_delete(all_data):
        pd_show(all_data)
        index = input("Введите индекс строки, которую хотите удалить, для выхода введите exit: ")
        if index == "exit": return
        sqlaaaa(f"DELETE FROM directory WHERE id={int(index)}")

    #Функция командного интерфейса
    def choose_command():
        while True:
            command = input("Список команд: show, edit, dump, delete, search, exit Введите команду: ")
            all_data = cur.execute("SELECT * FROM directory").fetchall()
            if command == "show": pd_show(all_data)
            elif command == "edit": directory_edit(all_data)
            elif command == "dump": directory_dump()
            elif command == "delete": directory_delete(all_data)
            elif command == "search": search_dir()
            elif command == "exit": break
            else: print('Ха-ха, смешно, я не понял...')
    choose_command()
    cur.close()
    con.close()

if __name__ == "__main__":
    main()