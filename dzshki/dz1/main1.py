import os
import tarfile
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import toml
import stat

class ShellEmulator:
    def __init__(self, config_path):
        # Загрузка конфигурации
        self.config = toml.load(config_path)
        
        # Распаковка виртуальной файловой системы
        self.extract_filesystem()
        
        # Текущий рабочий каталог
        self.current_dir = '/'
        
    def extract_filesystem(self):
        # Извлечение файловой системы из tar-архива
        tar_path = self.config['filesystem_path']
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(path='/tmp/virtual_fs')
        
    def ls(self, path=None):
        # Реализация команды ls
        target_path = os.path.join('/tmp/virtual_fs', 
                                   self.current_dir.lstrip('/'), 
                                   path or '')
        try:
            return os.listdir(target_path)
        except Exception as e:
            return f"Ошибка: {str(e)}"
    
    def cd(self, path):
        # Реализация команды cd
        try:
            new_path = os.path.normpath(os.path.join(self.current_dir, path))
            if os.path.isdir(os.path.join('/tmp/virtual_fs', new_path.lstrip('/'))):
                self.current_dir = new_path
                return self.current_dir
            else:
                return f"Ошибка: {path} не является каталогом"
        except Exception as e:
            return f"Ошибка: {str(e)}"
    
    def cp(self, src, dest):
        # Реализация команды cp
        try:
            full_src = os.path.join('/tmp/virtual_fs', 
                                    self.current_dir.lstrip('/'), 
                                    src)
            full_dest = os.path.join('/tmp/virtual_fs', 
                                     self.current_dir.lstrip('/'), 
                                     dest)
            shutil.copy2(full_src, full_dest)
            return f"Файл {src} скопирован в {dest}"
        except Exception as e:
            return f"Ошибка копирования: {str(e)}"
    
    def chmod(self, mode, path):
        # Реализация команды chmod
        try:
            full_path = os.path.join('/tmp/virtual_fs', 
                                     self.current_dir.lstrip('/'), 
                                     path)
            os.chmod(full_path, int(mode, 8))
            return f"Права доступа изменены для {path}"
        except Exception as e:
            return f"Ошибка изменения прав: {str(e)}"
    
    def du(self, path=None):
        # Реализация команды du
        target_path = os.path.join('/tmp/virtual_fs', 
                                   self.current_dir.lstrip('/'), 
                                   path or '')
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(target_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
            return f"Размер: {total_size} байт"
        except Exception as e:
            return f"Ошибка: {str(e)}"

class ShellGUI:
    def __init__(self, shell_emulator):
        self.shell = shell_emulator
        
        # Создание основного окна
        self.root = tk.Tk()
        self.root.title("Shell Emulator")
        
        # Текстовое поле вывода
        self.output_text = tk.Text(self.root, height=20, width=80)
        self.output_text.pack()
        
        # Поле ввода команд
        self.command_entry = tk.Entry(self.root, width=80)
        self.command_entry.pack()
        self.command_entry.bind('<Return>', self.execute_command)
        
    def execute_command(self, event):
        command = self.command_entry.get()
        parts = command.split()
        
        if not parts:
            return
        
        cmd = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        result = ""
        if cmd == 'ls':
            result = self.shell.ls(*args)
        elif cmd == 'cd':
            result = self.shell.cd(*args)
        elif cmd == 'cp':
            result = self.shell.cp(*args)
        elif cmd == 'chmod':
            result = self.shell.chmod(*args)
        elif cmd == 'du':
            result = self.shell.du(*args)
        elif cmd == 'exit':
            self.root.quit()
        
        self.output_text.insert(tk.END, f"{result}\n")
        self.command_entry.delete(0, tk.END)

def main():
    # Загрузка конфигурации
    config_path = 'config.toml'
    
    # Создание эмулятора shell
    shell = ShellEmulator(config_path)
    
    # Создание GUI
    gui = ShellGUI(shell)
    gui.root.mainloop()

if __name__ == '__main__':
    main()