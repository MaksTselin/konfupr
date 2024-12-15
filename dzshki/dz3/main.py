import argparse
import re
import xml.etree.ElementTree as ET
import sys

class ConfigLanguageTranslator:
    def __init__(self):
        self.constants = {}
    
    def parse_constant_expression(self, expr):
        """Вычисление константного выражения в постфиксной форме"""
        tokens = expr.split()
        stack = []
        
        for token in tokens:
            if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
                stack.append(int(token))
            elif token == '+':
                if len(stack) < 2:
                    raise ValueError(f"Недостаточно операндов для операции сложения")
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            elif token == '-':
                if len(stack) < 2:
                    raise ValueError(f"Недостаточно операндов для операции вычитания")
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif token == '*':
                if len(stack) < 2:
                    raise ValueError(f"Недостаточно операндов для операции умножения")
                b, a = stack.pop(), stack.pop()
                stack.append(a * b)
            elif token == 'abs()':
                if not stack:
                    raise ValueError(f"Недостаточно операндов для функции abs()")
                stack.append(abs(stack.pop()))
            else:
                # Обработка именованных констант
                if token in self.constants:
                    stack.append(self.constants[token])
                else:
                    raise ValueError(f"Неизвестный токен: {token}")
        
        if len(stack) != 1:
            raise ValueError("Некорректное константное выражение")
        
        return stack[0]
    
    def convert_value(self, value):
        """Преобразование значения"""
        if isinstance(value, str):
            # Строковое значение
            return f'@"{value}"'
        elif isinstance(value, (int, float)):
            # Числовое значение 
            return str(value)
        elif isinstance(value, dict):
            # Словарь
            return self.convert_dictionary(value)
        else:
            raise ValueError(f"Неподдерживаемый тип значения: {type(value)}")
    
    def convert_dictionary(self, d):
        """Преобразование словаря"""
        entries = []
        for key, val in d.items():
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9]*$', key):
                raise ValueError(f"Некорректное имя ключа: {key}")
            entries.append(f"{key} -> {self.convert_value(val)}.")
        
        return "{\n" + "\n".join(entries) + "\n}"
    
    def translate_xml_to_config(self, xml_root):
        """Трансляция XML в конфигурационный язык"""
        result = []
        
        # Обработка констант
        for const_elem in xml_root.findall(".//constant"):
            name = const_elem.get('name')
            value_elem = const_elem.find('value')
            
            if value_elem is not None:
                # Константное выражение
                if value_elem.get('type') == 'expression':
                    value = self.parse_constant_expression(value_elem.text)
                else:
                    # Прямое значение
                    value = self.parse_value(value_elem)
                
                # Объявление константы
                result.append(f"{name} is {self.convert_value(value)};")
                self.constants[name] = value
        
        # Обработка словарей
        for dict_elem in xml_root.findall(".//dictionary"):
            name = dict_elem.get('name')
            dict_data = self.parse_dictionary(dict_elem)
            result.append(f"{name} -> {self.convert_dictionary(dict_data)}")
        
        return "\n".join(result)
    
    def parse_value(self, value_elem):
        """Парсинг значения из XML"""
        value_type = value_elem.get('type')
        value_text = value_elem.text
        
        if value_type == 'number':
            return int(value_text)
        elif value_type == 'string':
            return value_text
        elif value_type == 'dictionary':
            return self.parse_dictionary(value_elem)
        else:
            raise ValueError(f"Неподдерживаемый тип значения: {value_type}")
    
    def parse_dictionary(self, dict_elem):
        """Парсинг словаря из XML"""
        result = {}
        for entry in dict_elem.findall('entry'):
            key = entry.get('name')
            value_elem = entry.find('value')
            result[key] = self.parse_value(value_elem)
        return result
    
    def process_file(self, input_file, output_file):
        """Обработка входного XML-файла"""
        try:
            # Парсинг XML
            tree = ET.parse(input_file)
            root = tree.getroot()
            
            # Трансляция 
            config_text = self.translate_xml_to_config(root)
            
            # Запись результата
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(config_text)
            
            print(f"Трансляция завершена. Результат сохранен в {output_file}")
        
        except ET.ParseError as e:
            print(f"Ошибка парсинга XML: {e}")
        except ValueError as e:
            print(f"Синтаксическая ошибка: {e}")
        except IOError as e:
            print(f"Ошибка работы с файлом: {e}")

def main():
    parser = argparse.ArgumentParser(description='Транслятор XML в конфигурационный язык')
    parser.add_argument('input', help='Путь к входному XML-файлу')
    parser.add_argument('output', help='Путь к выходному файлу')
    
    args = parser.parse_args()
    
    translator = ConfigLanguageTranslator()
    translator.process_file(args.input, args.output)

if __name__ == '__main__':
    main()