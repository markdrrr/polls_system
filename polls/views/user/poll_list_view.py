from datetime import date

from rest_framework.generics import ListAPIView

from polls.models import Poll
from polls.serializers import PollSerializer


class PollListAPIView(ListAPIView):
    """ Получение списка активных опросов """
    serializer_class = PollSerializer
    today = date.today()
    queryset = Poll.objects.filter(start_date__lte=today, finish_date__gt=today)
