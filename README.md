# Geekshop

Магазин одежды, обуви и аксессуаров

Содержание:
1. запуск проекта
   1. запуск тестового сервера локально
   2. развертывание проекта на Ubuntu через docker-compose
2. Описание проекта

## 1. i. запуск тестового сервера локально

## 1. ii. развертывание проекта на Ubuntu через docker-compose
```
$ sudo apt install docker-compose
$ git clone https://github.com/vakhnin/geekshop.git
$ cd geekshop/production
$ sudo docker compose up --build -d
```
При развертывании проекта будет создан пользователь с административными правами 
с логином `admin` и паролем `admin` 
Авторизация через "вконтакте" на сервере будет недоступна 
(необходима дополнительная настройка).

Развертывание тестировалось на Ubuntu 20, Docker 24.0.4, docker-compose 1.25.0 


