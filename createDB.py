import sqlite3
# #from main import FileSearch

conn = sqlite3.connect('LocalServer.db')
cur = conn.cursor()

cur.execute("DELETE the_list")

# # def insert():
# #     with conn:
# #         cur.execute("INSERT INTO results VALUES (:word,:filename,:frequency)",{'word':x[0],'filename':x[1],'frequency':x[2]})


# # def update():
# #     with conn:
# #         cur.execute("""UPDATE results SET frequency=:frequency WHERE word= :word AND filename = :filename""",{'word':x[0],'filename':x[1],'frequency':x[2]})


# # def delete():
# #     with conn:
# #         cur.execute("DELETE FROM results VALUES WHERE word=:word,filename=:filename,frequency=:frequency)",{'word':x[0],'filename':x[1],'frequency':x[2]})


# # def get_data():
# #     cur.execute("SELECT * FROM results WHERE word=:word AND filename=:filename",{'word':x[0],'filename':x[1]})


# # Create table
# cur.execute('''CREATE TABLE mydb
#                (word text,filename text,frequency integer)''')

# # Insert a row of data
# # cur.execute("INSERT INTO results VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# print(cur.execute("SELECT * FROM results"))


# #Save (commit) the changes
conn.commit()