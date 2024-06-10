import mysql.connector
import json
import tkinter as tk
from tkinter import ttk

def fetch_data_from_mysql():
    try:
        # Подключение к MySQL
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="corporate_generation_db"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            # Запрос для получения данных
            query = """
SELECT e.equipment_id, e.equipment_name, ec.characteristic_id, ecc.characteristic_name, cv.characteristic_value
FROM equipment e
INNER JOIN equipment_characteristic ec ON e.equipment_id = ec.equipment_id
INNER JOIN characteristic_values cv ON ec.characteristic_id = cv.characteristic_id
INNER JOIN equipment_characteristics ecc ON ecc.characteristic_id = ec.characteristic_id


                """
            cursor.execute(query)

            # Получение результатов запроса
            data = cursor.fetchall()

            # Закрытие курсора и соединения
            cursor.close()
            connection.close()

            return data

    except mysql.connector.Error as error:
        print("Ошибка при работе с MySQL:", error)

    return None

def create_json_file(data):
    if data:
        # Запись данных в JSON файл
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


def display_data_in_table(data):
    if data:
        root = tk.Tk()
        root.title("Данные оборудования и характеристик")

        # Создание таблицы
        tree = ttk.Treeview(root)
        tree["columns"] = ("Идентификатор оборудования", "Наименование оборудования",
                           "Идентификатор характеристики", "Наименование характеристики",
                           "Значение характеристики")

        # Настройка заголовков столбцов
        tree.heading("#0", text="№")
        tree.heading("Идентификатор оборудования", text="Идентификатор оборудования")
        tree.heading("Наименование оборудования", text="Наименование оборудования")
        tree.heading("Идентификатор характеристики", text="Идентификатор характеристики")
        tree.heading("Наименование характеристики", text="Наименование характеристики")
        tree.heading("Значение характеристики", text="Значение характеристики")

        # Вставка данных в таблицу
        for idx, row in enumerate(data, start=1):
            tree.insert("", "end", text=idx,
                        values=(row["equipment_id"], row["equipment_name"],
                                row["characteristic_id"], row["characteristic_name"],
                                row["characteristic_value"]))

        tree.pack(expand=True, fill="both")
        root.mainloop()

def main():
    data = fetch_data_from_mysql()
    if data:
        print("Данные корпоративного уровня получены")
        create_json_file(data)
        display_data_in_table(data)
    else:
        print("Ошибка при извлечении данных из MySQL")

if __name__ == "__main__":
    main()
