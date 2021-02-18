from datetime import date

from django.http import Http404
from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from polls.models import Poll
from polls.serializers import PollSerializer, ChoiceSerializer, QuestionSerializer
from polls.views.admin.api_view import AdminAPIView


class AdminPollId(AdminAPIView):
    def get(self, request, id):
        """ Получение опроса по id """
        try:
            poll = Poll.objects.get(id=id)
            result = PollSerializer(poll).data
            result['questions'] = []
            for question in poll.question_set.all():
                context = QuestionSerializer(question).data
                if question.hasOptionType:
                    context['choice'] = ChoiceSerializer(question.option_set.all(), many=True).data
                result['questions'].append(context)

            return Response(result)

        except Poll.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def delete(self, request, id):
        """ Удаление опроса по id """
        try:
            Poll.objects.get(id=id).delete()
            return Response('Deleted')
        except Poll.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def patch(self, request, id):
        """ Изменение опроса по id """
        try:
            poll = Poll.objects.get(id=id)
            data = request.data
            if 'name' in data:
                poll.name = data['name']
            if 'description' in data:
                poll.description = data['description']
            if 'finish_date' in data:
                poll.finish_date = date.fromisoformat(data['finish_date'])

            if poll.start_date > poll.finish_date:
                raise Exception('Invalid finish_date')

            poll.save()
            return Response(PollSerializer(poll).data)

        except Poll.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)
