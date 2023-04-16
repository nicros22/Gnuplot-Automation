import configparser
import os
import subprocess

config = configparser.ConfigParser()
config_file = 'config.ini'
gcc_section = 'GCC'
gcc_option = 'path'
gnuplot_section = 'Gnuplot'
gnuplot_option = 'path'


def find_mingw_bin():
    possible_paths = ['C:\\', 'C:\\Program Files', 'C:\\Program Files (x86)']
    for path in possible_paths:
        mingw_path = os.path.join(path, 'MinGW')
        if os.path.exists(mingw_path):
            bin_path = os.path.join(mingw_path, 'bin')
            if os.path.exists(bin_path):
                return bin_path
    return None


def path_automation(utility_type):
    if utility_type == '1':
        mingw_bin = find_mingw_bin()
        if mingw_bin:
            print(f'Путь к MinGW/GCC: {mingw_bin}')
            utility_action = input('Использовать этот путь? [y/n]: ')
        else:
            print('Папка не найдена')
    elif utility_type == '2':
        pass
    print_with_clear('Вернуться к:\n[1] Настройке\n[2] Главное меню')
    menu_stage = input()
    if menu_stage == '1':
        setting_menu()
    elif menu_stage == '2':
        main_menu()



def setting_menu():
    print_with_clear('Выберите действие:\n[1] Найти путь к утилитам самостоятельно\n[2] Указать вручную')
    setting_path = input()
    print_with_clear('Выберите программу:\n[1] MinGW/GCC\n[2] Gnuplot')
    utility_type = input()
    return setting_path, utility_type



def print_with_clear(text: str):
    os.system(['clear', 'cls'][os.name == os.sys.platform])
    print(text)


def main_menu():
    print_with_clear('Выберите действие:\n[1] Настройка пути к MinGW/GCC и Gnuplot\n[2] Построение графиков')
    type_action = input()
    return type_action


type_action = main_menu()
if type_action == '1':
    setting_path = setting_menu()
    pick_program()
elif type_action == '2':
    pass



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