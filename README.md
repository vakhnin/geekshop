# Geekshop

Магазин одежды, обуви и аксессуаров

Содержание:
1. Запуск тестового сервера разработки Django локально
   1. Запуск тестового сервера разработки Django локально (Windows 10)
   2. Запуск тестового сервера разработки Django локально (Ubuntu 20)
2. Развертывание проекта на сервере

## 1. i. Запуск тестового сервера разработки Django локально (Windows 10)
Необходимы предустановленные git, Python3

Развертывание проекта

В оболочке cmd (не PowerShell):

&gt; ```git clone https://github.com/vakhnin/geekshop.git``` <br>
&gt; ```cd .\geekshop\``` <br>
geekshop&gt; ```python -m venv venv``` <br>
geekshop&gt; ```.\venv\Scripts\activate.bat``` <br>
(venv) geekshop&gt; ```python.exe -m pip install --upgrade pip``` <br>
(venv) geekshop&gt; ```pip install -r requirements.txt``` <br>
(venv) geekshop&gt; ```python manage.py migrate``` <br>
(venv) geekshop&gt; ```python manage.py fill_db``` <br>
(venv) geekshop&gt; ```python manage.py runserver``` <br>

Тестировалось с Python 3.12

## 1. ii. Запуск тестового сервера разработки Django локально (Ubuntu 20)

$ ```sudo apt update``` <br>
$ ```sudo apt install git python3-venv -y``` <br>
$ ```git clone https://github.com/vakhnin/geekshop.git```<br>
$ ```cd geekshop/``` <br>
geekshop$ ```python3 -m venv venv``` <br>
geekshop$ ```source venv/bin/activate``` <br>
(venv) geekshop$ ```pip3 install -U pip``` <br>
(venv) geekshop$ ```pip3 install -r requirements.txt``` <br>
(venv) geekshop$ ```python3 manage.py migrate``` <br>
(venv) geekshop$ ```python3 manage.py fill_db``` <br>
(venv) geekshop$ ```python3 manage.py runserver``` <br>

## 2. развертывание проекта на Ubuntu через docker-compose

В терминале:<br>
$ ```sudo apt update```<br>
$ ```sudo apt install git docker docker-compose -y```<br>
$ ```git clone https://github.com/vakhnin/geekshop.git``` <br>
$ ```cd geekshop/production```<br>
geekshop/production$ ```sudo docker-compose up --build -d```

При развертывании проекта будет создан пользователь с административными правами 
с логином `admin` и паролем `admin` 
Авторизация через "вконтакте" на сервере будет недоступна 
(необходима дополнительная настройка).

Если дополнительно необходимо развернуть Grafana с Loki для 
отслеживания логов:<br>
geekshop/production$ ```sudo docker-compose -f ./docker-compose-grafana.yml up --build -d```

Развертывание тестировалось на Ubuntu 20, Docker 24.0.5, docker-compose 1.25.0 
