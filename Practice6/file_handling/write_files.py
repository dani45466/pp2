# write_files.py

# w - запись с перезаписью файла
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Python\n")
    f.write("File handling\n")


# a - добавление в конец
with open("notes.txt", "a", encoding="utf-8") as f:
    f.write("Appending new line\n")
    f.write("Another line\n")


# Проверяем содержимое
with open("notes.txt", "r", encoding="utf-8") as f:
    print(f.read())