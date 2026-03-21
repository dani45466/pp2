# Создаем файл и записываем в него данные
with open("sample.txt", "w", encoding="utf-8") as f:
    f.write("First line\n")
    f.write("Second line\n")
    f.write("Third line\n")


# read()
with open("sample.txt", "r", encoding="utf-8") as f:
    content = f.read()

print(content)


# readline()
with open("sample.txt", "r", encoding="utf-8") as f:
    print(f.readline().strip())
    print(f.readline().strip())



# readlines()
with open("sample.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
