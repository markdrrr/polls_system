from django.db import models

_choices = [('TEXT', 'TEXT'), ('CHOICE', 'CHOICE'), ('MULTIPLE_CHOICE', 'MULTIPLE_CHOICE')]


class Poll(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    start_date = models.DateField(auto_now_add=True)
    finish_date = models.DateField()

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.name


class Question(models.Model):
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    type = models.CharField(
        max_length=20,
        choices=_choices,
    )
    text = models.TextField()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'

    def __str__(self):
        return f'{self.choice_text}'


class Answer(models.Model):
    user_poll = models.ForeignKey('UserPoll', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    question_type = models.CharField(
        max_length=20,
        choices=_choices,
    )
    answer_text = models.TextField()

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'

    def __str__(self):
        return f'{self.question} {self.answer_text}'


class UserPoll(models.Model):
    userId = models.IntegerField(db_index=True)
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE)
    submitTime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заполненный опрос'
        verbose_name_plural = 'Заполненные опросы'

    def __str__(self):
        return f'userId {self.userId} {self.poll}'
