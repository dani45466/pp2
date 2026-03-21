

import os

# Создаем папки
os.makedirs("Practice6/test_folder/inner_folder", exist_ok=True)


# Показываем текущую директорию
print(os.getcwd())
print()

# Содержимое папки Practice6:
for item in os.listdir("Practice6"):
    print(item)