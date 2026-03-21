

import os
import shutil

# Создаем папки
os.makedirs("Practice6/source", exist_ok=True)
os.makedirs("Practice6/destination", exist_ok=True)

# Создаем файл
with open("Practice6/source/test.txt", "w", encoding="utf-8") as f:
    f.write("Hello from source folder")



# Копируем файл
shutil.copy("Practice6/source/test.txt", "Practice6/destination/test_copy.txt")


# Перемещаем файл
shutil.move("Practice6/source/test.txt", "Practice6/destination/test_moved.txt")
