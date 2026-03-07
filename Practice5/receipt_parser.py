import re
import json

def normalize_price(price_str):
    return float(price_str.replace(" ", "").replace(",", "."))

with open(r"C:\dani45466\pp2\Practice5\raw.txt", "r", encoding="utf-8") as f:
    text = f.read()


#Extract all prices

price_pattern = r"\d[\d ]*,\d{2}"
all_prices_raw = re.findall(price_pattern, text)
all_prices = [normalize_price(p) for p in all_prices_raw]


#Find all product names

product_pattern = r"\d+\.\n(.+)"
product_names = re.findall(product_pattern, text)


# Calculate total amount

item_total_pattern = r"x [\d ]+,\d{2}\n([\d ]+,\d{2})"
item_totals_raw = re.findall(item_total_pattern, text)
item_totals = [normalize_price(t) for t in item_totals_raw]

calculated_total = sum(item_totals)


#Extract date and time

datetime_pattern = r"Время:\s(\d{2}\.\d{2}\.\d{4})\s(\d{2}:\d{2}:\d{2})"
datetime_match = re.search(datetime_pattern, text)

date = datetime_match.group(1) if datetime_match else None
time = datetime_match.group(2) if datetime_match else None


# Find payment method

payment_pattern = r"(Банковская карта|Наличные)"
payment_match = re.search(payment_pattern, text)

payment_method = payment_match.group(1) if payment_match else None


# Structured output (JSON)

result = {
    "product_names": product_names,
    "all_prices": all_prices,
    "calculated_total": calculated_total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(result, ensure_ascii=False, indent=4))






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