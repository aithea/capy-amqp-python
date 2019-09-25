# Capy RabbitMQ wrapper library for python

Acинхронный клиент к брокеру сообщений реализующий шаблон PFL - Publish/Fetch/Listen. 
Доставка и получение собщений к брокеру остается асинхронной и не блокирует клиентское приложение.

## Зависимости
1. cmake>=3.12
1. clang>=4.3или gcc>=8.0 
1. openssl dev 1.0.2r
1. libuv
1. zlib
1. pyenv
1. pipenv
1. setuptools

## Инсталяция пакета

```bash
    pipenv install -e . 
```