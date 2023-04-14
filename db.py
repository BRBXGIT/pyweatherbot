import sqlite3

class BotDB:

    def __init__(self, db_file):

        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()


    #Добавление города в бд
    def add_city(self, user_id, value):
        self.cursor.execute("INSERT or REPLACE INTO `users_city` (`user_id`, `value`) VALUES (?, ?)", (user_id, value))
        return self.conn.commit()


    #Получение города из бд
    def get_city(self, user_id):
        result = self.cursor.execute("SELECT `value` FROM `users_city` WHERE `user_id` = ?", (user_id,))
        return result.fetchall()


    #Добавление пользователя в бд
    def add_user(self, user_id):
        self.cursor.execute("INSERT or REPLACE INTO `users_city` (`user_id`) VALUES (?)", (user_id,))


    def close(self):
        self.conn.close()