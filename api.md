Функционал для пользователей системы:
GET /user/polls
Получение списка активных опросов:
```
[
    {
        id,             # Число
        name,           # Строка
        description,    # Строка
        start_date,     # Формат DD.MM.YYYY
        finish_date     # Формат DD.MM.YYYY
    },
]
```
GET /user/polls/(id)
Получение подробной информации об одном опросе, с вопросами и ответами. Тело ответа:
```
{
    id, 
    name,           # Строка
    description,    # Строка
    start_date,     # Формат DD.MM.YYYY
    finish_date,     # Формат DD.MM.YYYY
    questions: [
        {
            id,
            text,           # Текст вопроса
            type,           # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
            options: [      # Список вариантов (только для типов CHOICE, MULTIPLE_CHOICE)
                { index, text },
            ]
        },
    ]
}
```

POST user/polls/(poll_id)
Прохождение опроса пользователем, добавляем новый ответ:
```
{
    user_id,     # Идентификатор пользователя
    answers: {
        'question_id': 'Text answer',     
    }
}
```
GET /user/polls_from_user/(user_id)
Получение пройденных пользователем опросов с детализацией по ответам:
```
[
    {
        id,                 # Идентификатор заполненного опроса
        submitTime,         # Дата и время прохождения опроса, формат YYYY-MM-DDThh:mm:ss
        poll_id,             # Идентификатор опроса
        answers: [
            {
                question_id,              # Идентификатор вопроса
                question_type,            # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
                question_text,            # Текст вопроса
                answer_text,              # Текст ответа
            },
        ]
    },
]
```

Функционал для администратора системы:
GET /admin/polls
Получение списка всех опросов. Тело ответа:

```
[
    {
        id,
        name,
        description,
        start_date,
        finish_date
    },
]
```
POST /admin/polls
Создание нового опроса. Тело запроса:

```
{
    name,
    description,
    start_date,
    finish_date 
}
```
Тело ответа:

```
{
    id, name, description, start_date, finish_date
}
```
GET /admin/polls/(id)
Получение подробной информации об одном опросе, с вопросами и ответами. Тело ответа:

```
{
    id, 
    name,
    description,
    start_date,
    finish_date
    questions: [
        {
            id,
            text,
            type,
            choice: [
                {
                    votes,
                    choice_text
                },
            ]
        },
    ]
}
```

DELETE /admin/polls/(id)
Удаление опроса.

PATCH /admin/polls/(id)
Редактирование опроса. Тело запроса (все поля опциональные):

```
{
    name,
    description,
    finish_date
}
```
Формат ответа:

```
{
    id, name, description, start_date, finish_date
}
```

POST /admin/polls/(id)/questions
Добавление нового вопроса к опросу id:

```
{
    text,
    type,          
    choise: [
        'Вариант 1',
        'Вариант 2',
    ]
}
```
Тело ответа:

```
{
    id,
    text,
    type,
    choice: [
                {
                    votes,
                    choice_text
                },
    ]
}
```
GET /admin/polls/(poll_id)/questions/(question_id)
Подробная информация об одном вопросе. Тело ответа:

```
{
    id,
    text,         
    type,           
    choice: [
                {
                    votes,
                    choice_text
                },
    ]
}
```

DELETE /admin/polls/(poll_id)/questions/(question_id)
Удаление вопроса из опроса.

PATCH /admin/polls/(pollId)/questions/(questionId)
Изменение существующего вопроса. Тело запроса (все поля опциональные):

```
{
    text,           # Текст вопроса
    type,           # Тип вопроса: TEXT, CHOICE, MULTIPLE_CHOICE
    choice: [      # Список вариантов (только для типов CHOICE, MULTIPLE_CHOICE)
        'Вариант 1',
        'Вариант 2',
    ]
}
```
Тело ответа:

```
{
    id,
    text,
    type,
    choice: [
                {
                    votes,
                    choice_text
                },
    ]
}
```