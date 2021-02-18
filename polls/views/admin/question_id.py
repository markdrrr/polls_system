from django.http import Http404
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from polls.models import Question, Choice
from polls.serializers import QuestionSerializer, ChoiceSerializer
from polls.views.admin.api_view import AdminAPIView


class AdminQuestionId(AdminAPIView):
    def get(self, request, poll_id, question_id):
        """ Получение вопроса по id """
        try:
            question = Question.objects.get(id=question_id)
            result = QuestionSerializer(question).data
            result['choice'] = ChoiceSerializer(question.choice_set.all(), many=True).data
            print(result)
            return Response(result)

        except Question.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def delete(self, request, poll_id, question_id):
        """ Удаление вопроса по id """
        try:
            Question.objects.get(id=question_id).delete()
            return Response('Deleted')
        except Question.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def patch(self, request, poll_id, question_id):
        """ Изменение вопроса по id """
        try:

            question = Question.objects.get(id=question_id)
            data = request.data

            # проверяем запрос на волидность
            if not 'choice' in data:
                raise Exception('options are missing')
            if type(data['choice']) != list or len(data['choice']) < 2:
                raise Exception('Invalid choice')
            if 'text' in data:
                question.text = data['text']
            question.save()

            # удаляем старые варианты ответа к вопросу
            Choice.objects.filter(question=question).delete()

            # создаем новые варианты ответа
            index = 1
            for choice_text in data['choice']:
                Choice(text=choice_text, index=index, question=question).save()
                index += 1

            result = QuestionSerializer(question).data
            result['choice'] = ChoiceSerializer(question.choice_set.all(), many=True).data
            return Response(result)

        except Question.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)
