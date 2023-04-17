import configparser
import os
import subprocess
import urllib.request
from tqdm import tqdm


config = configparser.ConfigParser()
config_file = 'config.ini'
gcc_section = 'MinGW-GCC'
gcc_option = 'path-to-MinGW'
gnuplot_section = 'Gnuplot'
gnuplot_option = 'path-to-gnuplot'
config.read('config.ini')


def repeat_forever(func):
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)
    return wrapper


@repeat_forever
def main_menu():
    print_with_clear('Выберите действие:\n[1] Настройка пути к MinGW/GCC и Gnuplot\n[2] Построение графиков\n'
                     '[3] Установка MinGW/GCC')
    type_action = input()
    if type_action == '1':
        setting_menu()
    elif type_action == '2':
        building_graphs()
    elif type_action == '3':
        installing_software()

def setting_menu():
    print_with_clear('Выберите действие:\n[1] Найти путь к утилитам автоматически\n[2] Указать папку вручную')
    setting_path = input()
    print_with_clear('Выберите программу:\n[1] MinGW/GCC\n[2] Gnuplot')
    utility_type = input()
    if setting_path == '1':
        path_automation(utility_type)
    elif setting_path == '2':
        path_manually(utility_type)

def building_graphs():
    mingw_path = config.get(gcc_section, gcc_option)
    gnuplot_path = config.get(gnuplot_section, gnuplot_option)
    print_with_clear('Использую пути:\nMinGW/GCC: {}\nGnuplot: {}'.format(mingw_path, gnuplot_path))
    graphs_folder = input('Укажите путь к папке с файлами для построения графиков: ')

def find_mingw_bin():
    possible_paths = ['C:\\', 'C:\\Program Files', 'C:\\Program Files (x86)']
    for path in possible_paths:
        mingw_path = os.path.join(path, 'MinGW')
        if os.path.exists(mingw_path):
            bin_path = os.path.join(mingw_path, 'bin\\gcc.exe')
            if os.path.exists(bin_path):
                return bin_path
    return None


def find_gnuplot_bin():
    possible_paths = ['C:\\', 'C:\\Program Files', 'C:\\Program Files (x86)']
    for path in possible_paths:
        mingw_path = os.path.join(path, 'gnuplot')
        if os.path.exists(mingw_path):
            bin_path = os.path.join(mingw_path, 'bin\\wgnuplot.exe')
            if os.path.exists(bin_path):
                return bin_path
    return None


def reporthook(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    print(f"Downloaded {count * block_size} bytes out of {total_size} bytes ({percent}%)", end="\r")


def installing_software():
    # Download MinGW installer
    print_with_clear('Выберите программу:\n[1] MinGW\n[2] Gnuplot')
    utility_type = input()
    if utility_type == '1':
        url = 'https://sourceforge.net/projects/mingw/files/latest/download'
        filename = 'mingw-setup.exe'
        with tqdm(unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
            urllib.request.urlretrieve(url, filename,
                                       reporthook=lambda count, block_size, total_size: t.update(block_size))
        print("\nMinGW скачан как: ", filename)
        subprocess.Popen([filename, '-y', '--no-admin', '--wait', '--wait-children'])
    elif utility_type == '2':
        url = 'https://sourceforge.net/projects/gnuplot/files/latest/download'
        filename = 'gnuplot-setup.exe'
        with tqdm(unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
            urllib.request.urlretrieve(url, filename,
                                       reporthook=lambda count, block_size, total_size: t.update(block_size))
        print("\nGnuplot скачан как: ", filename)
        subprocess.Popen([filename, '-y', '--no-admin', '--wait', '--wait-children'])
    main_menu()


def path_automation(utility_type):
    if utility_type == '1':
        mingw_bin = find_mingw_bin()
        if mingw_bin:
            print_with_clear(f'Путь к MinGW/GCC: {mingw_bin}')
            utility_action = input('Использовать этот путь? [y/n]: ')
            if utility_action == 'y':
                config.set(gcc_section, gcc_option, mingw_bin)
                with open(config_file, 'w') as f:
                    config.write(f)
            elif utility_action == 'n':
                pass
        else:
            print('Папка не найдена')
    if utility_type == '2':  # Автоматическое указание пути к Gnuplot
        gnuplot_bin = find_gnuplot_bin()
        if gnuplot_bin:
            print_with_clear(f'Путь к Gnuplot: {gnuplot_bin}')
            utility_action = input('Использовать этот путь? [y/n]: ')
            if utility_action == 'y':
                config.set(gnuplot_section, gnuplot_option, gnuplot_bin)
                with open(config_file, 'w') as f:
                    config.write(f)
            elif utility_action == 'n':
                pass
        else:
            print('Папка не найдена')
    print_with_clear('Вернуться к:\n[1] Настройке\n[2] Главное меню')
    menu_stage = input()
    if menu_stage == '1':
        setting_menu()
    elif menu_stage == '2':
        main_menu()


def path_manually(utility_type):
    if utility_type == '1':
        print_with_clear('Введите путь к папке MinGW/GCC:')
        print(utility_type)
        mingw_path = input()
        mingw_path = os.path.join(mingw_path, 'bin\\gcc.exe')
        if not os.path.exists(mingw_path):
            input('Путь не найден')
            setting_menu()
        print_with_clear(f'Выбран путь: {mingw_path}')
        config.set(gcc_section, gcc_option, mingw_path)
        with open(config_file, 'w') as f:
            config.write(f)
    elif utility_type == '2':
        print_with_clear('Введите путь к папке Gnuplot:')
        gnuplot_path = input()
        gnuplot_path = os.path.join(gnuplot_path, 'bin\\wgnuplot.exe')
        if not os.path.exists(gnuplot_path):
            input('Путь не найден')
            setting_menu()
        print_with_clear(f'Выбран путь: {gnuplot_path}')
        config.set(gnuplot_section, gnuplot_option, gnuplot_path)
        with open(config_file, 'w') as f:
            config.write(f)
    print('Вернуться к:\n[1] Настройке\n[2] Главное меню')
    menu_stage = input()
    if menu_stage == '1':
        setting_menu()
    elif menu_stage == '2':
        main_menu()


def print_with_clear(text: str):
    os.system('cls')
    #os.system(['clear', 'cls'][os.name == os.sys.platform])
    print(text)

main_menu()
# Проверяем, есть ли файл конфигурации
# if not config.has_section(gcc_section):
#     # Если файл конфигурации не существует или нет секции для GCC, запрашиваем путь
#     gcc_path = input("Please enter the path to GCC: ")
#
#     # Создаем секцию для GCC и сохраняем путь
#     config.set(gcc_section, gcc_option, gcc_path)
#
#     # Сохраняем файл конфигурации
#     with open(config_file, 'w') as f:
#         config.write(f)
# else:
#     # Если файл конфигурации существует и есть секция для GCC, используем сохраненный путь
#     gcc_path = config.get(gcc_section, gcc_option)
#
# # Путь к вашему файлу .c
# source_file = "path/to/your/source/file.c"
#
# # Путь для сохранения .exe файла
# output_file = "path/to/your/output/file.exe"
#
# # Команда для вызова компилятора
# command = [gcc_path, source_file, "-o", output_file]
#
# # Запускаем процесс и ждем его завершения
# proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#
# # Получаем вывод компилятора
# output = proc.stdout.decode('utf-8')
#
# # Если произошла ошибка, выводим ее на экран
# if proc.returncode != 0:
#     print("Compilation error:")
#     print(output)
# else:
#     print("Compilation successful!")