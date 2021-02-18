from rest_framework import serializers

from polls.models import Poll, _choices


class PollSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    start_date = serializers.DateField(format='%d.%m.%Y')
    finish_date = serializers.DateField(format='%d.%m.%Y')

    class Meta:
        model = Poll
        fields = '__all__'


class PollsByUserIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    submitTime = serializers.DateTimeField(format='%d.%m.%YT%H:%M:%S')


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    type = serializers.ChoiceField(choices=_choices)
    text = serializers.CharField(max_length=200)


class ChoiceSerializer(serializers.Serializer):
    votes = serializers.IntegerField(default=0)
    choice_text = serializers.CharField(max_length=200)
