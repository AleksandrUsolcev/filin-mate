# filin-mate
![Python version](https://img.shields.io/badge/python-3.9-yellow) ![Django version](https://img.shields.io/badge/django-4.1-red) ![Aiogram version](https://img.shields.io/badge/aiogram-2.22-blue)

Дневник основных показателей здоровья реализованный посредством асинхронного телеграм-бота и rest-api.

В текущих реалиях при наблюдении у врачей многим пациентам на дом часто назначают ведение дневника артериального давления и пульса. Заполнять такой дневник как правило приходится вручную, что впоследствии затрудняет анализ показателей лечащим врачом, попутно отнимая уйму ценного рабочего времени. Помимо затраченного времени отсутствует возможность оперативно реагировать на показания, в случае отклонения их от нормы. Решить эти проблемы и не только призван данный проект.

Со стороны пользователя доступна возможность заносить посредством бота следующие показатели здоровья: пульс, артериальное давление, температура тела, сатурация, уровень сахара в крови, вес, рост, время сна. Так же можно оценить свое физическое или психологическое состояние и оставить небольшую текстовую заметку. Помимо указанных показателей можно добавить свой тип через админку.

В комплекте имеется простой парсер погоды с OpenWeatherMap, по-умолчанию каждые полчаса сохраняющий данные о температуре, виде осадков, давлении и влажности. На текущий момент в целях не нагружать запросами api данные о погоде берутся по Москве, но при желании можно указать любую другую локацию (подробнее в разделе настроек). Собранные данные о погоде могут пригодится в дальнейшем анализе таких показателей как пульс и артериальное давление.

## Планы по доработке

Бот:
- выгрузка данных в формате csv;
- формирование различных графиков на основе запрашиваемых данных;
- запрос геолокации пациента;
- отключаемые уведомления о необходимости внесения показателей;
- уведомления в случае отклонения от нормы показателей здоровья.

Web:
- личный кабинет пациента;
- рабочая страница врача со списком подопечных пациентов и их показателей;
- инструментарий для удобного анализа показателей здоровья.

## Технологии

- Python 3.9+
- [django](https://github.com/django/django) 4.1
- [django-rest-framework](https://github.com/encode/django-rest-framework)
  3.13
- [Simple JWT](https://github.com/jazzband/djangorestframework-simplejwt) 5.2.0
- [AIOGram](https://github.com/aiogram/aiogram) 2.22
- [Dateutil](https://github.com/dateutil/dateutil) 2.8

## Запуск проекта

Клонировать репозиторий и перейти в filin-mate/docker/

```bash
git clone https://github.com/AleksandrUsolcev/filin-mate.git
cd filin-mate/docker/
``` 

Клонировать [образец](/docker/example.env) файла переменного окружения и заполнить

```bash
cp example.env .env
nano .env
``` 

- **POSTGRES_PASSWORD** - придумать пароль DB
- **FILIN_TOKEN** - токен api, пока не трогаем, его мы получим на следующих шагах
- **TELEGRAM_TOKEN** - получаем при [создании](https://telegram.me/BotFather) бота в телеграме
- **WEATHER_TOKEN** - по умолчанию в настройках отключен парсинг погоды и если в нем нет никакой необходимости WEATHER_TOKEN можно не указывать. Получить токен погоды можно зарегистрировавшись на [OpenWeatherMap](https://openweathermap.org/). Обязательно следует ознакомиться с информацией по лимитам запросов.
- **WEATHER_PARSE** - добавить (значение указываем любое) если у нас есть токен с [OpenWeatherMap](https://openweathermap.org/)

Развернуть docker контейнеры (пока без бота)

```
docker-compose up -d db web nginx
``` 

Создать суперпользователя

```bash
docker-compose exec web python manage.py createsuperuser
```

Получить токен*, указав данные суперпользователя

```bash
docker-compose exec web python manage.py token <email> <password>
``` 

**Данная команда так же обновляет уже созданный токен. Посмотреть актуальный токен можно перейдя в админке на УЗ суперпользователя .../project-admin/users/user/*

В созданном ранее .env файле копируем в значение **FILIN_TOKEN** полученный токен суперпользователя

Пересобираем и запускаем контейнеры

```
docker-compose up -d --build
``` 

## Настройки бота

Файл настроек - **[settings.py](/telegram_bot/settings.py)**

**DIFF_TIME** - интервал (мин.) добавления новых показателей здоровья

**WEATHER_PARSE** - вкл/откл парсинг погоды при запуске бота

**WEATHER_PARSE_INTERVAL** - интервал парсинга погоды (мин.)

**LATITUDE** и **LONGITUDE** - широта и долгота, с координатами для парсинга погоды. В дальнейших обновлениях отпадут из за ненадобности и при парсинге будет идти обращение к указанным пациентами координатам

**STATS_TYPES** - словарь с типами показателей здоровья и их настройками по умолчанию. При добавлении своих типов показателей следует его обновить, т.к. с его ключей берутся команды для бота

**STATS_TYPES_FILL_ON_START** - вкл/откл автодобавление типов данных из **STATS_TYPES** при запуске бота

**LOGS_NAME** - имя файла логов

## Автор

[Александр Усольцев](https://github.com/AleksandrUsolcev)
