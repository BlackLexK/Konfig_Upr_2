import xml.etree.ElementTree as ET
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

# Разбор имени пакета 
def parse_package_name(name):
    try:
        group, artifact, version = name.strip().split(":")
        return group, artifact, version
    except:
        print("Ошибка: имя пакета должно быть groupId:artifactId:version")
        exit(1)

# Формирование URL к POM 
def build_pom_url(repo_url, group, artifact, version):
    group_path = group.replace(".", "/")
    return f"{repo_url.rstrip('/')}/{group_path}/{artifact}/{version}/{artifact}-{version}.pom"

# Скачивание pom-файла 
def download_pom(url):
    print("Скачивание POM по URL:", url)
    try:
        with urlopen(url) as f:
            return f.read().decode("utf-8")
    except HTTPError:
        print("Ошибка: POM не найден по указанному URL.")
        exit(1)
    except URLError:
        print("Ошибка: невозможно подключиться к репозиторию.")
        exit(1)

# Извлечение прямых зависимостей
def extract_dependencies(xml_text):
    # Парсим XML с учётом namespace
    root = ET.fromstring(xml_text)
    # Определяем namespace POM
    ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
    deps = root.find("m:dependencies", ns)

    if deps is None:
        return []

    result = []
    for d in deps.findall("m:dependency", ns):
        g = d.find("m:groupId", ns)
        a = d.find("m:artifactId", ns)
        v = d.find("m:version", ns)

        if g is not None and a is not None:
            # Если версии нет, подставим пустую или "unknown"
            ver = v.text if (v is not None and v.text) else "unknown"
            result.append(f"{g.text}:{a.text}:{ver}")

    return result


# ТОЧКА ВХОДА

package = input("Введите имя пакета (groupId:artifactId:version): ")
repo = input("Введите URL репозитория: ")

group, artifact, version = parse_package_name(package)
pom_url = build_pom_url(repo, group, artifact, version)
pom_text = download_pom(pom_url)
deps = extract_dependencies(pom_text)

print("\nПрямые зависимости:")
if deps:
    for d in deps:
        print(" -", d)
else:
    print("Нет прямых зависимостей")

#com.google.guava:guava:33.0.0-jre
#https://repo1.maven.org/maven2/