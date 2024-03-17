API для создания пользователей и их задач.
Функции:
- регистрация пользователя по имени и паролю;
- вход в систему по имени и паролю;
- выдача пользователю jwt;
- аутентификация по jwt;
- создание задачи;
- вывод всех задач пользователя;
- вывод всех пользователей;
- вывод параметров пользователя.
База данных реализована по схеме service -> unit of work -> repository -> sqlalchemy -> postgres.