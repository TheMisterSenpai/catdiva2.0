from contextlib import closing
import sqlite3

class Get:
    def __init__(self):
        pass

    def privateChannels(self, member):
        conn = sqlite3.connect("./Data/Cache/guild_channels.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM privates WHERE member={member.id}")
        result = cursor.fetchone()

        conn.close()
        return result

    def options(self, name):
        conn = sqlite3.connect("./Data/DataBase/guild_options.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM {name}")
        result = cursor.fetchone()

        conn.close()
        return result    

class Set:
    def __init__(self):
        pass

    def privateChannels(self, channel, member):
        conn = sqlite3.connect("./Data/Cache/guild_channels.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM privates WHERE member={member.id}")
        if cursor.fetchone():
            cursor.execute(f"UPDATE privates SET member={member.id}, channel={channel.id} WHERE member={member.id}")
        else:
            cursor.execute(f"INSERT INTO privates VALUES ({channel.id}, {member.id})")

        conn.commit()
        conn.close()

    def options(self, data):  # [{"name": "имя", "data": "инфа"}, {}, {}]
        conn = sqlite3.connect("./Data/DataBase/guild_options.db")
        cursor = conn.cursor()

        for i in data:
            name = i["name"]
            update = i["update"]
            insert = i["insert"]

            cursor.execute(f"SELECT * FROM {name}")

            if not cursor.fetchone():
                cursor.execute(f"INSERT INTO {name} VALUES ({insert})")
            else:
                cursor.execute(f"UPDATE {name} SET {update}")

        conn.commit()
        conn.close()     


class userwarndb:
    def __init__(self):
        pass

    def warnuser(self, member):
        conn = sqlite3.connect('./Data/DataBase/warn_users.db')
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        warns INT,
        id INT
    )""")

        for guild in client.guilds:
            for member in guild.members:
                if cursor.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None: #заполняем у всех пользователей количество варнов = 0
                    cursor.execute(f"INSERT INTO users VALUES('{member.id}', 0)")
            else:
                pass
        conn.commit()
        conn.close() 
        