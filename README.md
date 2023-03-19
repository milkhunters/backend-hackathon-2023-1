# Backend часть проекта 

Данный проект предназначен для решения кейса **Часть корпоративного портала для предприятия закрытого типа** от Вебпрактик 


## Frontend

Реализацию фронтедна для данного решения можно найти во [втором репозитории.](https://github.com/milkhunters/frontend2-hackathon-2023-1)

Взаимодействие между фронтом и бэком происходит по REST API.

## API

Документация Swagger доступна по адресу: [https://hack.milkhunters.ru/api/v1/docs](https://hack.milkhunters.ru/api/v1/docs)

Также, можно скачать в виде файла [openapi.json](https://hack.milkhunters.ru/api/v1/openapi.json)

## Демо

Демо доступно по ссылке [https://hack.milkhunters.ru](https://hack.milkhunters.ru)

Для тестирования приложения можно использовать следующие учетные записи:

| Логин            | Пароль        | Роль                     |
|------------------|---------------|--------------------------|
| `admin@milk.com` | `Password123` | Администратор            |
| `user1@milk.com` | `Password123` | Пользователь 1-го уровня |
| `user2@milk.com` | `Password123` | Пользователь 2-го уровня |

* Несмотря на то, что пароли кажутся простыми, их валидация
полностью соответствует требованиям задания.

## Дополнительный функционал 

### Множественная загрузка файлов (отключено из-з нестабильности)

Хорошо организованная схема базы данных и хорошая архитектура 
бэкенд приложения позволяют реализовать множественную загрузку файлов.
Однако, в качестве меры ограничения, было решено, что к сообщению можно 
будет прикрепить максимум 10 файлов. Данная цифра может быть изменена.

### (в разр) Отображение кол-ва непрочитанных сообщений, вместо просто индикатора

![img.png](https://i.imgur.com/SDUrrcT.png)

### Дополнительная административная функциональность

Также, есть статичная административная функциональность.
В основном оно касается Раздела новостей, а также пользователей

![alt](https://i.imgur.com/Etdg8lR.png)
![alt](https://i.imgur.com/MQUStVP.png)

## Конфигурирование

Указать конфигурации приложения можно разными способами:

### Через Consul kv

Бэкенд приложение будет ожидать consul на `127.0.0.1:8500`.

Для того чтобы указать конфигурацию, нужно создать в consul kv следующие ключи:

```
# --- Необязательные параметры ---
consul_root/BASE/CONTACT/EMAIL
consul_root/BASE/CONTACT/NAME
consul_root/BASE/CONTACT/URL
consul_root/BASE/DESCRIPTION
consul_root/BASE/TITLE

# --- Обязательные параметры ---
consul_root/BASE/JWT/ACCESS_SECRET_KEY
consul_root/BASE/JWT/REFRESH_SECRET_KEY

consul_root/DB/POSTGRESQL/DATABASE
consul_root/DB/POSTGRESQL/HOST
consul_root/DB/POSTGRESQL/PASSWORD
consul_root/DB/POSTGRESQL/PORT
consul_root/DB/POSTGRESQL/USERNAME

consul_root/DB/REDIS/HOST
consul_root/DB/REDIS/PASSWORD
consul_root/DB/REDIS/PORT
consul_root/DB/REDIS/USERNAME

consul_root/S3/ACCESS_KEY
consul_root/S3/BUCKET
consul_root/S3/DIRECT_URL
consul_root/S3/HOST
consul_root/S3/PORT
consul_root/S3/REGION
consul_root/S3/SECRET_ACCESS_KEY
```

### Через переменные окружения

Также, можно указать некоторые параметры через переменные окружения:

- `CONSUL_ROOT` - необходимо для consul kv
- `DEBUG` - включить режим отладки (1, 0)

Если `DEBUG=0`, ожидаемый корневой маршрут `/api/v1`

Если `DEBUG=1`, повышенное логирование, `http 500` 
отображаются пользователю

Рекомендуется запускать локально в режиме `DEBUG=1`
## Запуск

### Зависимости

Для работы backend приложения необходимы следующие компоненты:

- PostgreSQL
- Redis
- Consul
- Minio (S3) - или любой другой S3 совместимый сервис

### Локально

Для запуска приложения локально, нужно выполнить следующие команды:

```bash
pip install -r requirements.txt
```

```bash
uvicorn src.app:app --proxy-headers --host 127.0.0.1 --port 8080
```
Используйте `http://127.0.0.1:8080/api/v1/docs` для доступа к Swagger документации.

### Docker

Для запуска приложения в docker, нужно выполнить следующие команды:

```bash
docker build -t milk-hackathon .
```

```bash
docker run -p 8080:8080 -e CONSUL_ROOT="consul_root" -e DEBUG=1 milk-hackathon
```

## Об архитектуре и технологиях

### Архитектурные решения

- **FastAPI** - быстрый, асинхронный и удобный фреймворк для написания REST API
- **SQLAlchemy** - мощная ORM для работы с базой данных

### Технологические решения

- **Docker** - для упрощения развертывания приложения
- **Consul** - для хранения конфигураций приложения
- **PostgreSQL** - для хранения данных приложения
- **Redis** - для хранения данных сессий авторизации
- **Minio** - S3 совместимый сервис для хранения файлов,
позволяющий легко масштабировать хранилище данных приложений.

_В случае повышения требований к резервированию данных,
можно легко перейти на любое совместимое S3 хранилище, в том числе 
и на Российские облачные сервисы, среди которых можно найти
много соответствующих требованиям 152-ФЗ._

### JWT авторизация

Для авторизации используется пара JWT токенов и индетификатор сессии.

При авторизации пользователя, сервер возвращает два токена:
- `access_token` - JWT токен с ограниченным временем жизни, который используется для доступа к ресурсам
- `refresh_token` - JWT токен с длинным временем жизни, который используется для обновления `access_token`
- `session_id` - идентификатор сессии, который используется для обновления `access_token`

Введение `session_id` позволяет избежать проблем с рефрешем токена в случае, если пользователь авторизован на нескольких устройствах.

Также, реализовано "бесшовное" обновление токенов при любом запросе к API.

В случае масштабирования приложения и выделения в микросервисы,
можно использовать отдельный маршрут для ручного обновления токенов.

### Организация базы данных

Схема базы данных:

![что-то пошло не так :(](https://imgur.con/&&&&&.png)


### Немного об инфраструктуре

Все сервисы запускаются в Docker контейнерах.

Для проксирования трафика используется Nginx.

Для обеспечения ci/cd используется TeamCity.

Агенты TeamCity запускаются в Docker контейнерах, при этом
с прокидыванием хостового докер демона в контейнеры.

Это позволяет непосредственно в агентах осуществлять действия по
развёртыванию приложения, например, с помощью `docker-compose` или `docker run`.

#### Стек технологий

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Traefik](https://traefik.io/)
- [TeamCity](https://www.jetbrains.com/teamcity/)

### Проксирование

Для проксирования запросов к API можно использовать nginx или любой другой веб-сервер.

Примеры конфигурации для некоторых из них (только среда `dev`):

#### Nginx

```
# Это конфиг только для dev env, для прода нужно заменять Access-Control-Allow-Origin хеадеры на конкретно по домену
map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
}

server {
    server_name example.com;

    listen 443 ssl;

    # ---- Backend REST API ---- #
    location /api/v1/ {

        proxy_pass http://127.0.0.1:8101/;

        # --------CORS-------#

        if ($request_method = 'OPTIONS') {
            # Tell client that this pre-flight info is valid for 20 days
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain charset=UTF-8';
            add_header 'Content-Length' 0;

            #add_header 'Access-Control-Allow-Origin' "https://example.com" always;
	        add_header Access-Control-Allow-Origin "$http_origin" always;
	        add_header 'Access-Control-Allow-Headers' "DNT, Authorization, Origin, X-Requested-With, X-Host, X-Request-Id, Timing-Allow-Origin, Content-Type, Accept, Content-Range, Range, Keep-Alive, User-Agent, If-Modified-Since, Cache-Control, Content-Type" always;
            add_header 'Access-Control-Request-Method' "GET, POST, PATCH, PUT, DELETE, OPTIONS" always;
            add_header 'Access-Control-Allow-Credentials' 'true' always;
            add_header X-Frame-Options SAMEORIGIN always;

            return 204;
        }

        #add_header 'Access-Control-Allow-Origin' "https://example.com" always;
	    add_header Access-Control-Allow-Origin "$http_origin" always;
	    add_header 'Access-Control-Allow-Headers' "DNT, Authorization, Origin, X-Requested-With, X-Host, X-Request-Id, Timing-Allow-Origin, Content-Type, Accept, Content-Range, Range, Keep-Alive, User-Agent, If-Modified-Since, Cache-Control, Content-Type" always;
        add_header 'Access-Control-Request-Method' "GET, POST, PATCH, PUT, DELETE, OPTIONS" always;
        add_header 'Access-Control-Allow-Credentials' 'true' always;
        add_header X-Frame-Options SAMEORIGIN always;
        # --------CORS-------#
    }
    
    proxy_http_version  1.1;
    proxy_set_header    Upgrade $http_upgrade;
    proxy_set_header    Connection $connection_upgrade;

    # ---- Frontend app ---- #
    location / {
        proxy_pass http://127.0.0.1:8102/;
    }
}
```

#### Traefik

Список меток для Docker контейнеров:

```
-l "traefik.enable=true"

-l "traefik.http.routers.milk-back-dev.entrypoints=https"
-l "traefik.http.routers.milk-back-dev.rule=Host(`example.com`) && PathPrefix(`/api/v1`)"
-l "traefik.http.routers.milk-back-dev.tls=true"

-l "traefik.http.routers.milk-back-dev.middlewares=milk-back-dev-cors@docker,milk-back-dev-strip-prefix@docker,milk-back-dev-ws@docker"

-l "traefik.http.middlewares.milk-back-dev-cors.headers.accesscontrolallowmethods=GET,OPTIONS,PUT,DELETE,POST"
-l "traefik.http.middlewares.milk-back-dev-cors.headers.accessControlAllowHeaders=Content-Type, Authorization"
-l "traefik.http.middlewares.milk-back-dev-cors.headers.accessControlalloworiginlistregex=^(https?://localhost(:\d+)?|https://example\\.com)$"
-l "traefik.http.middlewares.milk-back-dev-cors.headers.accesscontrolallowcredentials=true"
-l "traefik.http.middlewares.milk-back-dev-cors.headers.accesscontrolmaxage=100"
-l "traefik.http.middlewares.milk-back-dev-cors.headers.isdevelopment=true"
-l "traefik.http.middlewares.milk-back-dev-cors.headers.addvaryheader=true"

-l "traefik.http.middlewares.milk-back-dev-strip-prefix.stripprefix.prefixes=/api/v1"

-l "traefik.http.middlewares.milk-back-dev-ws.headers.customrequestheaders.X-Forwarded-Proto=https,wss"
```
