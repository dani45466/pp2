import re

pattern = r"ab*"

tests = ["a", "ab", "abb", "ac"]
for t in tests:
    print(t, "->", bool(re.fullmatch(pattern, t)))




pattern = r"ab{2,3}"

tests = ["abb", "abbb", "abbbb", "ab"]
for t in tests:
    print(t, "->", bool(re.fullmatch(pattern, t)))




text = "snake_case example_text Wrong_Text"

matches = re.findall(r"[a-z]+_[a-z]+", text)
print(matches)






with open("raw.txt", encoding="utf-8") as f:
    text = f.read()

matches = re.findall(r"[A-Z][a-z]+", text)
print(matches)






pattern = r"a.*b"

tests = ["ab", "axxxb", "a123b", "ac"]
for t in tests:
    print(t, "->", bool(re.fullmatch(pattern, t)))






text = "Hello, world. Example text"

result = re.sub(r"[ ,.]", ":", text)
print(result)





def snake_to_camel(s):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), s)





text = "CamelCaseText"

parts = re.findall(r"[A-Z][a-z]*", text)
print(parts)





def camel_to_snake(s):
    return re.sub(r"([A-Z])", r"_\1", s).lower().lstrip("_")

print(camel_to_snake("CamelCaseText"))