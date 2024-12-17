# Практическое задание №4. Системы контроля версий

## Задача 1
На сайте https://onlywei.github.io/explain-git-with-d3 или http://git-school.github.io/visualizing-git/ (цвета могут отличаться, есть команды undo/redo) с помощью команд эмулятора git получить следующее состояние проекта (сливаем master с first, перебазируем second на master): см. картинку ниже. Прислать свою картинку.
![alt-text](https://sun9-58.userapi.com/impg/NMERMXPw6B25Go4Ti6agYk-geUFYAIQCxlVtkA/2Wyai8LKcPg.jpg?size=1105x665&quality=96&sign=0a09d738a56e64cc7d0c78c7e2222503&type=album)

## Задача 2

Создать локальный git-репозиторий. Задать свои имя и почту (далее – coder1). Разместить файл prog.py с какими-нибудь данными. Прислать в текстовом виде диалог с git.
![alt-text](https://sun9-21.userapi.com/impg/ib5VhVa2xnkEXe1J4WANqteDZJbYeMIJJR4how/Ea2iyisHfJM.jpg?size=1039x1153&quality=96&sign=5c768944b16338901304597f43eed1b9&type=album)

## Задача 3
Создать рядом с локальным репозиторием bare-репозиторий с именем server. Загрузить туда содержимое локального репозитория. Команда git remote -v должна выдать информацию о server! Синхронизировать coder1 с server.

Клонировать репозиторий server в отдельной папке. Задать для работы с ним произвольные данные пользователя и почты (далее – coder2). Добавить файл readme.md с описанием программы. Обновить сервер.

Coder1 получает актуальные данные с сервера. Добавляет в readme в раздел об авторах свою информацию и обновляет сервер.

Coder2 добавляет в readme в раздел об авторах свою информацию и решает вопрос с конфликтами.

Прислать список набранных команд и содержимое git log.

Пример лога коммитов:

```
*   commit a457d748f0dab75b4c642e964172887de3ef4e3e
|\  Merge: 48ce283 d731ba8
| | Author: Coder 2 <coder2@corp.com>
| | Date:   Sun Oct 11 11:27:09 2020 +0300
| | 
| |     readme fix
| | 
| * commit d731ba84014d603384cc3287a8ea9062dbb92303
| | Author: Coder 1 <coder1@corp.com>
| | Date:   Sun Oct 11 11:22:52 2020 +0300
| | 
| |     coder 1 info
| | 
* | commit 48ce28336e6b3b983cbd6323500af8ec598626f1
|/  Author: Coder 2 <coder2@corp.com>
|   Date:   Sun Oct 11 11:24:00 2020 +0300
|   
|       coder 2 info
| 
* commit ba9dfe9cb24316694808a347e8c36f8383d81bbe
| Author: Coder 2 <coder2@corp.com>
| Date:   Sun Oct 11 11:21:26 2020 +0300
| 
|     docs
| 
* commit 227d84c89e60e09eebbce6c0b94b41004a4541a4
  Author: Coder 1 <coder1@corp.com>
  Date:   Sun Oct 11 11:11:46 2020 +0300
  
      first commit
```
![alt-text](https://sun9-34.userapi.com/impg/mSXRjnjg07mKl_jlC_pOFybzvYZEAiKnJO5rLQ/N9Z0MDIxsRc.jpg?size=904x1166&quality=96&sign=0abaed91def0c916e3ad4dcf4df5c589&type=album)
![alt-text](https://sun9-50.userapi.com/impg/msTv4iZ4-oeN_fdKRIZF0oUlODqFDlaUFxTPUw/YquFXaORufU.jpg?size=955x1159&quality=96&sign=5a3bca2af818263cf918954205f4cb5c&type=album)
![alt-text](https://sun1-90.userapi.com/impg/ZW5rtlsqpwkV9DjuciPpa4EVx4_uVx-ABke2Ow/VzboU1PTnXc.jpg?size=972x1166&quality=96&sign=ad499e1cce528198fd18e2245ee45b21&type=album)
![alt-text](https://sun9-78.userapi.com/impg/Y5ByfBcH4yoV6v6ulf7qu8d7YmJJetx6Xk2m6A/eBed4D3BCb0.jpg?size=883x1161&quality=96&sign=429bd40e55975e13e0739b6336b37fa1&type=album)
![alt-text](https://sun9-2.userapi.com/impg/D1ayZwNwuSBVmrAFvDY-99prt70JZYkY7hzMBw/ymk4MrKTMTw.jpg?size=1920x1200&quality=96&sign=751add403fba735d9190a93f96a62710&type=album)

## Задача 4
Написать программу на Питоне (или другом ЯП), которая выводит список содержимого всех объектов репозитория. Воспользоваться командой "git cat-file -p". Идеальное решение – не использовать иных сторонних команд и библиотек для работы с git.
![alt-text](https://sun9-66.userapi.com/impg/qV9wrzHzr4Xh2RW7ksIFgO44EOecc5kGuiPM7Q/DfWhcO8F4-A.jpg?size=724x944&quality=96&sign=454066b9da6ae53a14bdfb62f29eda59&type=album)
![alt-text](https://sun1-97.userapi.com/impg/qSMKDGrmDrLRbU9BMZf08yBvMzXHVXX2zJHKgA/P1nouAGSktI.jpg?size=547x631&quality=96&sign=744acc226c570ea0b8e4daed8f49858b&type=album)
