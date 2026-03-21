# copy_delete_files.py

import os
import shutil

# Создаем исходный файл
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("This is original file.\n")



# Копирование
shutil.copy("data.txt", "data_copy.txt")


# Резервная копия
shutil.copy2("data.txt", "data_backup.txt")


# Безопасное удаление
file_to_delete = "data_copy.txt"

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
else:
    print(f"{file_to_delete} не найден.")