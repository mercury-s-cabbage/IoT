from bd_interactions import create_db, add_device, register_user, add_user_progress, add_level
import sqlite3

conn = sqlite3.connect('DungeonGame.db')
cursor = conn.cursor()

# create_db(cursor)
#
# add_device(cursor, "01.001", "new")
# add_device(cursor, "01.002", "new")
# add_device(cursor, "01.003", "new")
#
# register_user(cursor, "01.001", "lena", 4)
#register_user(cursor, "01.007", "lena", 4)

#add_user_progress(cursor, 1, 1, 1)

#add_level(cursor, "start", "text text text", "image/path")

conn.commit()
conn.close()