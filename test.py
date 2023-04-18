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

class GraphBuilder:
    def __init__(self, mingw_path, gnuplot_path):
        self.mingw_path = mingw_path
        self.gnuplot_path = gnuplot_path

    def build_project(self, file):
        # Компилируем выбранный файл в exe
        proc = subprocess.run([self.mingw_path, '-o', f'{os.path.splitext(file)[0]}.exe', file], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        if proc.returncode == 0:
            print('Компиляция прошла успешно!')
        # Если произошла ошибка, выводим ее на экран
        else:
            print('Ошибка компиляции:')
            print(proc.stderr.decode('utf-8'))
        exe_file = f'{os.path.splitext(file)[0]}.exe'
        self.run_project(exe_file)


    def run_project(self, exe_file):
        with open('data.dat', 'w') as f:
            run_proc = subprocess.run([exe_file], stdout=f, stderr=subprocess.PIPE)
        if run_proc.returncode == 0:
            print('Данные успешно записаны в файл data.dat')
            input('Нажмите Enter для продолжения...')
        # Если произошла ошибка, выводим ее на экран
        else:
            print('Ошибка компиляции:')
            print(run_proc.stderr.decode('utf-8'))


    def gnuplot_action(self):


    def building_graphs(self):
        print_with_clear('Использую пути:\nMinGW/GCC: {}\nGnuplot: {}'.format(self.mingw_path, self.gnuplot_path))
        while True:
            graphs_folder = input('Укажите путь к папке с файлами для построения графиков: ')
            # Получаем список файлов .c в папке и выводим их на экран
            files = sorted(os.listdir(graphs_folder), key=lambda x: x.split('.')[-1])
            files = [f for f in files if f.endswith('.c') or f.endswith('.exe')]
            if not files:
                print('В папке нет файлов с расширением .c или .exe, попробуйте ввести другой путь')
                continue
            else:
                break

        for i, f in enumerate(files):
            print(f'[{i+1}] {f}')

        # Пользователь выбирает номер файла для компиляции
        while True:
            choice = input('Выберите файл для компиляции (введите номер или название файла): ')
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(files):
                    filename = files[index]
                    break
            elif os.path.isfile(os.path.join(graphs_folder, choice)):
                filename = choice
                break
            print('Некорректный выбор, попробуйте снова.')

        c_file = os.path.join(graphs_folder, filename)
        print(f"Файл: {c_file}")
        file_extension = os.path.splitext(c_file)[1]

        if file_extension == '.exe':
            self.run_project(c_file)
        elif file_extension == '.c':
            self.build_project(c_file)


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
        mingw_path = config.get(gcc_section, gcc_option)
        gnuplot_path = config.get(gnuplot_section, gnuplot_option)
        graph_builder = GraphBuilder(mingw_path, gnuplot_path)
        graph_builder.building_graphs()
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


def find_mingw_bin():
    possible_paths = ['C:\\', 'C:\\Program Files', 'C:\\Program Files (x86)']
    for path in possible_paths:
        mingw_path = os.path.join(path, 'TDM-GCC-64')
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


def download_file(url, filename):
    with tqdm(unit="B", unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
        def reporthook(count, block_size, total_size):
            progress_bytes = count * block_size
            if total_size > 0:
                progress_percent = progress_bytes / total_size * 100
                t.update(block_size)
                t.set_postfix(percent=f"{progress_percent:.1f}%")
            else:
                t.update(block_size)
        urllib.request.urlretrieve(url, filename, reporthook=reporthook)


def installing_software():
    # Download MinGW installer
    print_with_clear('Выберите программу:\n[1] MinGW\n[2] Gnuplot')
    utility_type = input()
    if utility_type == '1':
        url = 'https://sourceforge.net/projects/tdm-gcc/files/TDM-GCC%20Installer/tdm64-gcc-5.1.0-2.exe/download'
        filename = 'tdm64-gcc-5.1.0-2.exe'
        print(f"Скачиваю по ссылке: {url}")
        download_file(url, filename)
        print("\nMinGW скачан как: ", filename)
        subprocess.Popen([filename, '-y', '--admin', '--wait', '--wait-children'])
    elif utility_type == '2':
        url = 'https://sourceforge.net/projects/gnuplot/files/latest/download'
        filename = 'gnuplot-setup.exe'
        print(f"Скачиваю по ссылке: {url}")
        download_file(url, filename)
        print("\nGnuplot скачан как: ", filename)
        subprocess.Popen([filename, '-y', '--admin', '--wait', '--wait-children'])
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