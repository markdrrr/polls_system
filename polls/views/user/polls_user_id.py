import json

from rest_framework.response import Response
from rest_framework.views import APIView

from polls.models import UserPoll, Answer
from polls.serializers import PollsByUserIDSerializer


class PollsUserID(APIView):
    def get(self, request, id):
        """ Получение пройденных пользователем опросов с детализацией по ответам """
        result = []
        qs = UserPoll.objects.filter(userId=id).select_related('poll')
        for el in qs:
            context = PollsByUserIDSerializer(el).data
            context['poll_id'] = el.poll_id
            answers = Answer.objects.filter(user_poll=el.pk)
            context['answers'] = []
            for answer in answers:
                answer_text = answer.answer_text
                # проверяем если типо вопроса множественный выбор, передаем ответ json'ом
                if answer.question_type == 'MULTIPLE_CHOICE':
                    answer_text = json.loads(answer.answer_text)

                context['answers'].append({
                    'question_id': answer.question.id,
                    'question_type': answer.question_type,
                    'question_text': answer.question.text,
                    'answer_text': answer_text
                })
            result.append(context)
        return Response(result)
