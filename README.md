<!-- PROJECT LOGO -->
<div align="center">
  <h2>hitalent-test</h2>

  <h3 align="center">README тестового задания</h3>

  <p align="center">
    FastApi-приложение: сервис бронирования столиков в ресторане
  </p>
</div>

<a name="readme-top"></a>

<hr>

<!-- ABOUT THE PROJECT -->
## About The Project

Разработать REST API для бронирования столиков в ресторане.
Сервис должен позволять создавать, просматривать и удалять брони, а также управлять столиками и временными слотами.

### Функциональные требования:

#### Модели:
* Table – столик в ресторане:
  - id: int
  - name: str (например, "Table 1")
  - seats: int (количество мест)
  - location: str (например, "зал у окна", "терраса")

* Reservation – бронь:
  - id: int
  - customer_name: str
  - table_id: int (FK на Table)
  - reservation_time: datetime
  - duration_minutes: int

#### Методы API:
* Столики:
  - GET /tables/ — список всех столиков
  - POST /tables/ — создать новый столик
  - DELETE /tables/{id} — удалить столик

* Брони:
  - GET /reservations/ — список всех броней
  - POST /reservations/ — создать новую бронь
  - DELETE /reservations/{id} — удалить бронь


#### Логика бронирования:
* Нельзя создать бронь, если в указанный временной слот столик уже занят (пересечение по времени и table_id).
* Бронь может длиться произвольное количество минут.
* Валидации должны обрабатываться на уровне API (например, конфликт брони должен выдавать ошибку с пояснением).
 
### Технические требования
* Использовать FastAPI как основной фреймворк.
* Работа с БД через SQLAlchemy или SQLModel.
* Использовать PostgreSQL.
* Использовать Alembic для миграций.
* Приложение должно быть обернуто в Docker.
* Использовать docker-compose для запуска всех компонентов.
* Структура проекта должна быть модульной: routers/, models/, schemas/, services/, и т.п.
* Код должен быть легко расширяемым.
* Приветствуется: логгирование, покрытие базовых сценариев тестами (на pytest).

### Built With

* [![FastApi][FastApi-badge]][FastApi-url]
* [![Postgres][Postgres-badge]][Postgres-url]
* [![SQLAlchemy][SQLAlchemy-badge]][SQLAlchemy-url]
* [![Docker][Docker-badge]][Docker-url]


<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Скопировать проект в репозиторий на локальной машине (HTTPS или SSH)
  ```sh
  git clone https://github.com/SuperLalka/hitalent-test
  ```
  ```sh
  git clone git@github.com:SuperLalka/hitalent-test.git
  ```

### Installation

Для запуска проекта достаточно собрать и запустить контейнеры Docker.
Миграция базы данных и загрузка фикстур будут применены автоматически.

```sh
docker-compose -f docker-compose.yml up -d --build
```

Запуск тестов:
```sh
docker-compose -f test.yml up --build
```


### Documentation

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[FastApi-badge]: https://img.shields.io/badge/fastapi-%23009688.svg?style=for-the-badge&logo=fastapi&logoColor=white
[FastApi-url]: https://fastapi.tiangolo.com/
[Postgres-badge]: https://img.shields.io/badge/postgresql-%234169E1.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/
[SQLAlchemy-badge]: https://img.shields.io/badge/sqlalchemy-%23D71F00.svg?style=for-the-badge&logo=sqlalchemy&logoColor=white
[SQLAlchemy-url]: https://www.sqlalchemy.org/
[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
