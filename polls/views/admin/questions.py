from django.http import Http404
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from polls.models import Poll, Question, Choice
from polls.serializers import QuestionSerializer, ChoiceSerializer
from polls.views.admin.api_view import AdminAPIView


class AdminQuestions(AdminAPIView):
    """ Создание объекта вопроса """
    def post(self, request, id):
        try:
            poll = Poll.objects.get(id=id)
            qs = QuestionSerializer(data=request.data)
            qs.is_valid(raise_exception=True)
            pd = dict(qs.validated_data)
            print('pd', pd)
            pd['poll'] = poll
            new_question = Question(**pd)
            new_question.save()

            require_choice = new_question.type
            new_choice_list = []
            if require_choice:
                if not 'choice' in request.data:
                    raise Exception('choice are missing')
                if type(request.data['choice']) != list or len(request.data['choice']) < 2:
                    raise Exception('Invalid choice')

                # создаем варианты ответа на вопрос
                index = 1
                for choice_text in request.data['choice']:
                    new_choice_list.append(Choice(
                        text=choice_text,
                        index=index
                    ))
                    index += 1

            # проходим по вариантам и создаем запись в бд
            if require_choice:
                for new_choice in new_choice_list:
                    new_choice.question = new_question
                    new_choice.save()

            result = QuestionSerializer(new_question).data
            if require_choice:
                result['choice'] = [ChoiceSerializer(o).data for o in new_choice_list]

            return Response(result)

        except Poll.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)
