from rest_framework.exceptions import ParseError
from rest_framework.response import Response

from polls.models import Poll
from polls.serializers import PollSerializer
from polls.views.admin.api_view import AdminAPIView


class AdminPolls(AdminAPIView):
    def get(self, request):
        """ Получаем список опросов """
        return Response(PollSerializer(Poll.objects.all(), many=True).data)

    def post(self, request):
        """ Создаем объект опроса """
        try:
            new_poll = PollSerializer(data=request.data)
            print(new_poll)
            new_poll.is_valid(raise_exception=True)
            print(new_poll.is_valid(raise_exception=True))
            data = new_poll.validated_data
            print(data)
            if data['start_date'] > data['finish_date']:
                raise Exception('Invalid finish_date')

            newPoll = Poll(**data)
            newPoll.save()
            return Response(PollSerializer(newPoll).data)
        except Exception as ex:
            raise ParseError(ex)
