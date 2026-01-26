# Числовые типы
integer_var = 10            # int
float_var = 3.14            # float
complex_var = 2 + 3j        # complex

# Строка
string_var = "Привет, Python!"  # str

# Логический тип
bool_var = True             # bool

# Коллекции
list_var = [1, 2, 3]        # list
tuple_var = (4, 5, 6)       # tuple
set_var = {7, 8, 9}         # set
dict_var = {"a": 1, "b": 2} # dict

# Специальный тип
none_var = None             # NoneType

variables = [
    integer_var,
    float_var,
    complex_var,
    string_var,
    bool_var,
    list_var,
    tuple_var,
    set_var,
    dict_var,
    none_var
]

for value in variables:
    print(f"Значение: {value!r}, Тип: {type(value)}")
