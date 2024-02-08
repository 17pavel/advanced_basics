#!/usr/bin/env python
# -*- coding: utf-8 -*-


# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';
"""
Про логи:
семпл лога: nginx-access-ui.log-20170630.gz
шаблон названия логов интерфейса соответствует названию сэмпла (ну, только время меняется)
так вышло, что логи могут быть и plain и gzip
лог ротируется раз в день
опять же, так вышло, что логи интерфейса лежат в папке с логами других сервисов
Про отчет:
count ‑ сколько раз встречается URL, абсолютное значение
count_perc ‑ сколько раз встречается URL, в процентнах относительно общего числа запросов
time_sum ‑ суммарный $request_time для данного URL'а, абсолютное значение
time_perc ‑ суммарный $request_time для данного URL'а, в процентах относительно общего $request_time всех
запросов
time_avg ‑ средний $request_time для данного URL'а
time_max ‑ максимальный $request_time для данного URL'а
time_med ‑ медиана $request_time для данного URL'а
Задание: реализовать анализатор логов log_analyzer.py .
Основная функциональность:
1. Скрипт обрабатывает при запуске последний (со самой свежей датой в имени, не по mtime файла!) лог в
LOG_DIR , в результате работы должен получится отчет как в report-2017.06.30.html  (для корректной работы
нужно будет найти и принести себе на диск jquery.tablesorter.min.js ). То есть скрипт читает лог, парсит
нужные поля, считает необходимую статистику по url'ам и рендерит шаблон report.html  (в шаблоне нужно
только подставить $table_json ). Ситуация, что логов на обработку нет возможна, это не должно являться
ошибкой.
2. Если удачно обработал, то работу не переделывает при повторном запуске. Готовые отчеты лежат в
REPORT_DIR . В отчет попадает REPORT_SIZE  URL'ов с наибольшим суммарным временем обработки
(time_sum ).
3. Скрипту должно быть возможно указать считать конфиг из другого файла, передав его путь через --config . У
пути конфига должно быть дефолтное значение. Если файл не существует или не парсится, нужно выходить с
ошибкой.
4. В переменной config  находится конфиг по умолчанию (и его не надо выносить в файл). В конфиге, считанном
из файла, могут быть переопределены перменные дефолтного конфига (некоторые, все или никакие, т.е. файл
может быть пустой) и они имеют более высокий приоритет по сравнению с дефолтным конфигом. Таким
образом, результирующий конфиг получается слиянием конфига из файла и дефолтного, с приоритетом
конфига из файла.
5. Использовать конфиг как глобальную переменную запрещено, т.е. обращаться в своем функционале к нему
так, как будто он глобальный ‑ нельзя. Нужно передавать как аргумент.
6. Использовать сторонние библиотеки запрещено.
Мониторинг:
1. скрипт должен писать логи через библиотеку logging в формате '[%(asctime)s] %(levelname).1s %
(message)s'  c датой в виде '%Y.%m.%d %H:%M:%S'  (logging.basicConfig позволит настроить это в одну строчку).
Допускается только использование уровней info , error  и exception . Путь до логфайла указывается в
конфиге, если не указан, лог должен писаться в stdout (параметр filename в logging.basicConfig может
принимать значение None как раз для этого).
2. все возможные "неожиданные" ошибки должны попадать в лог вместе с трейсбеком (посмотрите на
logging.exception). Имеются в виду ошибки непредусмотренные логикой работы, приводящие к остановке
обработки и выходу: баги, нажатие ctrl+C, кончилось место на диске и т.п.
3. должно быть предусмотрено оповещение о том, что большую часть анализируемого лога не удалось
распарсить (например, потому что сменился формат логирования). Для этого нужно задаться относительным
(в долях/процентах) порогом ошибок парсинга и при его превышании писать в лог, затем выходить.
Тестирование:
1. на скрипт должны быть написаны тесты с использованием библиотеки unittest
(https://pymotw.com/2/unittest/). Имя скрипта с тестами должно начинаться со слова test . Тестируемые кейсы
и структура тестов определяется самостоятельно (без фанатизма, в принципе достаточно функциональных
тестов)"""

import os
import logging
import datetime
import glob
import json
import argparse
import shutil
from string import Template


def parse_log(log_file):
    # Парсинг лог-файла и извлечение нужных полей
    # Возвращаем результат в виде словаря
    parsed_data = {}
    
    return parsed_data


def calculate_statistics(parsed_data):
    # Расчет статистики по url'ам
    # Возвращаем результат в виде словаря
    statistics = {}
    # Ваш код для расчета статистики
    return statistics


def generate_report(statistics):
    # Генерация отчета на основе статистики
    # Возвращаем отчет в виде строки
    template = Template("$table_json")
    report = template.substitute(table_json=json.dumps(statistics))
    return report


def save_report(report):
    # Сохранение отчета в файл
    report_path = os.path.join(REPORT_DIR, f"report-{datetime.datetime.now().strftime('%Y.%m.%d')}.html")
    with open(report_path, "w") as f:
        f.write(report)


def process_log(log_file):
    parsed_data = parse_log(log_file)
    statistics = calculate_statistics(parsed_data)
    report = generate_report(statistics)
    save_report(report)


def get_latest_log_file():
    # Получение пути к последнему лог-файлу в LOG_DIR
    log_files = glob.glob(os.path.join(LOG_DIR, "*.log"))
    latest_log_file = max(log_files, key=os.path.getmtime)
    return latest_log_file


def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname).1s %(message)s",
        datefmt="%Y.%m.%d %H:%M:%S",
        filename=log_file,
        filemode="w"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.json", help="Path to the config file")
    args = parser.parse_args()

    # Загрузка конфигурации из файла
    with open(args.config) as f:
        config = json.load(f)

    # Установка пути к директориям
    LOG_DIR = config.get("LOG_DIR", "logs")
    REPORT_DIR = config.get("REPORT_DIR", "reports")
    REPORT_SIZE = config.get("REPORT_SIZE", 10)

    # Создание директорий, если они не существуют
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(REPORT_DIR, exist_ok=True)

    # Установка пути к лог-файлу
    log_file = config.get("LOG_FILE")
    if log_file:
        log_file = os.path.join(LOG_DIR, log_file)
    else:
        log_file = None

    # Настройка логирования
    setup_logging(log_file)

    try:
        # Обработка лог-файла
        latest_log_file = get_latest_log_file()
        process_log(latest_log_file)

        # Перемещение обработанного лог-файла
        processed_log_dir = os.path.join(LOG_DIR, "processed")
        os.makedirs(processed_log_dir, exist_ok=True)
        shutil.move(latest_log_file, processed_log_dir)

        logging.info("Script executed successfully")
    except Exception as e:
        logging.exception("An unexpected error occurred")


if __name__ == "__main__":
    main()
