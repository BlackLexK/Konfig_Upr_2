import sys
import xml.etree.ElementTree as ET

if len(sys.argv) < 2:
    print("Error_1")
    sys.exit(1)

c = sys.argv[1]

try:
    tree = ET.parse(c)
    root = tree.getroot()
except FileNotFoundError:
    print(f"Ошибка: файл '{c}' не найден.")
    sys.exit(1)
except ET.ParseError as e:
    print(f"Ошибка разбора XML: {e}")
    sys.exit(1)

p = ["package_name", "repository_url", "repo_mode", "output_image", "ascii_mode", "filter"]

config = {}

# Считывание параметров
for par in p:
    el = root.find(par)
    if el is None or not el.text:
        print(f"Ошибка: отсутствует параметр <{par}> в конфигурационном файле.")
        sys.exit(1)
    config[par] = el.text.strip()

# Проверка корректности значений
if config["repo_mode"] not in ("local", "remote"):
    print("Ошибка: параметр <repo_mode> должен быть 'local' или 'remote'.")
    sys.exit(1)

if config["ascii_mode"].lower() not in ("true", "false"):
    print("Ошибка: параметр <ascii_mode> должен быть 'true' или 'false'.")
    sys.exit(1)

# Вывод параметров
print("Параметры конфигурации:")
for key, value in config.items():
    print(f"{key} = {value}")