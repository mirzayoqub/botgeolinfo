import mysql.connector as conn
from telebot.types import ReplyKeyboardMarkup



class db:
    def __init__(self):
        self.conn = conn.connect(
            host="iphost",
            user="root",
            password="password",
            database="database_name"
        )
        self.menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    def get_name(self, lang):
        with self.conn:
            mycursor = self.conn.cursor()
            if lang == 'Русский':
                col = 'name_ru'
            else:
                col = 'name_uz'
            mycursor.execute(f"select {col} from geol_bot.department;")
            myresult = mycursor.fetchall()


        for i in myresult:
            for j in i:
                self.menu.row(str(j))
        self.menu.add("⬅️Orqaga")

        return self.menu

    def save_db(self, message, feedback, department, file):
        with self.conn:
            mycursor = self.conn.cursor()
            if feedback in ['Bildirgi', 'Жалоба']:
                sql = "INSERT INTO bildirgi (department, text) VALUES (%s, %s);"
                post = (department, file)
                mycursor.execute(sql, post)
            elif feedback in ['Maslahat', 'Предложение']:
                sql = "INSERT INTO sovet (department, text) VALUES (%s, %s);"
                post = (department, file)
                mycursor.execute(sql, post)
            else:
                print('oops')
            self.conn.commit()

    def save_score(self, department, score):
        with self.conn:
            mycursor = self.conn.cursor()
            sql = "INSERT INTO score (department, score) VALUES (%s, %s);"
            post = (department, score)
            mycursor.execute(sql, post)

            self.conn.commit()