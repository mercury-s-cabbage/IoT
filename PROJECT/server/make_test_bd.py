from bd_interactions import create_db, add_device, register_user, add_user_progress, add_level
import sqlite3

conn = sqlite3.connect('DungeonGame.db')
cursor = conn.cursor()

create_db(cursor)

add_device(cursor, "01.001", "new")
add_device(cursor, "01.002", "new")
add_device(cursor, "01.003", "new")
add_device(cursor, "01.004", "new")

# register_user(cursor, "01.001", "lena", "01.001")
# register_user(cursor, "01.001", "geka", "01.002")
# register_user(cursor, "01.001", "lisa", "01.003")
# register_user(cursor, "01.001", "danya", "01.002,")
# register_user(cursor, "01.001", "diana", "01.001")
#
# add_user_progress(cursor, 1, 1, 1)
# add_user_progress(cursor, 1, 1, 1)
# add_user_progress(cursor, 2, 1, 0)
# add_user_progress(cursor, 3, 1, 0)
# add_user_progress(cursor, 4, 1, 1)
# add_user_progress(cursor, 5, 1, 1)
# add_user_progress(cursor, 1, 1, 1)
# add_user_progress(cursor, 1, 1, 0)

add_level(cursor, "За семью печатями",
          "Вы ступаете в храм света: стены его состоят из хрусталя, "
          " солнечные лучи, преломляясь, отбрасывают радугу на ваше уставшее лицо.",
          1234,
          "Солнечный луч проходит через призму в крыше и сжигает вас как муравьишку. Вы не прошли испытание.",
          "levels/task_1.png")

add_level(cursor, "Обращаясь к свету",
          "Дверь в тайный зал библиотеки открывается после произнесенного шепотом ''Алохомора''."
          " Вы видите волшебную ловушку.",
          2412,
          "Авада Кедавра. Вы умерли.",
          "levels/task_2.png")

add_level(cursor, "Арифметика",
          "Исследуя заброшенный замок, вы находите комнату, подозрительно напоминающую учебную."
          "Неудобный стол, прибитый к полу стул, книжные полки и висящая на стене розга."
          "На столе лежит заплаканная записка: ''Ваше величество, юному принцу не дается устный счет!''",
          3132,
          "Розга срывается со стены и двумя ударами рассекает вас на раз-два-три части.",
          "levels/task_3.png")

add_level(cursor, "Выбор",
          "Вы выходите к жертвенному алтарю, вокруг тошнотворно воняет чем-то сладко-металлическим. Пол покрывает липкая"
          " алая жидкость. Сквозь нее вы разглядываете надпись.",
          3244,
          "Пластина проваливается под вами, обнажая шипы. Вас принесли в жертву.",
          "levels/task_4.png")

conn.commit()
conn.close()