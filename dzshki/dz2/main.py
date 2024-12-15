import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

class DependencyVisualizer:
    def __init__(self, package_name, repo_url=None):
        self.package_name = package_name
        self.repo_url = repo_url or "https://pypi.org/pypi"
        self.dependencies = {}
        self.visited = set()

    def fetch_package_info(self, package_name):
        """Получение информации о пакете с PyPI"""
        try:
            url = f"{self.repo_url}/{package_name}/json"
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Ошибка получения информации о пакете {package_name}: {e}")
            return None

    def parse_dependencies(self, package_name, depth=0):
        """Рекурсивный парсинг зависимостей"""
        if package_name in self.visited or depth > 3:
            return

        self.visited.add(package_name)
        
        package_info = self.fetch_package_info(package_name)
        if not package_info:
            return

        # Извлечение зависимостей из метаданных
        deps = []
        for req in package_info.get('info', {}).get('requires_dist', []) or []:
            # Очистка имени зависимости 
            match = re.match(r'^([a-zA-Z0-9\-_]+)', req)
            if match:
                deps.append(match.group(1).lower())

        self.dependencies[package_name] = deps

        # Рекурсивный обход зависимостей
        for dep in deps:
            if dep not in self.visited:
                self.parse_dependencies(dep, depth + 1)

    def generate_plantuml(self):
        """Генерация кода PlantUML для графа зависимостей"""
        plantuml_code = "@startuml\n"
        plantuml_code += f"title Dependencies of {self.package_name}\n\n"

        for pkg, deps in self.dependencies.items():
            for dep in deps:
                plantuml_code += f"{pkg} --> {dep}\n"

        plantuml_code += "@enduml"
        return plantuml_code

    def visualize(self, output_file=None, graph_tool=None):
        """Визуализация графа зависимостей"""
        self.parse_dependencies(self.package_name)
        plantuml_code = self.generate_plantuml()

        # Вывод на экран
        print(plantuml_code)

        # Опциональная запись в файл
        if output_file:
            with open(output_file, 'w') as f:
                f.write(plantuml_code)

        # Опциональная визуализация через внешний инструмент
        if graph_tool:
            """Создаёт граф из puml файла с использованием PlantUML"""
            try:
                command = f"java -jar {graph_tool} {output_file}"
                subprocess.check_call(command, shell=True)
                print(f"Граф успешно создан и сохранён как {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Ошибка при генерации PNG: {e}")
                return False
            return True
                
        

def main():
    parser = argparse.ArgumentParser(description='Визуализация зависимостей Python-пакета')
    parser.add_argument('package', help='Имя пакета')
    parser.add_argument('-o', '--output', help='Файл для сохранения результата')
    parser.add_argument('-g', '--graph-tool', help='Путь к инструменту визуализации графов')
    parser.add_argument('-r', '--repo', help='URL репозитория пакетов')

    args = parser.parse_args()

    visualizer = DependencyVisualizer(
        args.package, 
        repo_url=args.repo
    )
    visualizer.visualize(
        output_file=args.output, 
        graph_tool=args.graph_tool
    )

if __name__ == '__main__':
    main()