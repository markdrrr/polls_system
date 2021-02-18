import json
from datetime import date

from django.http import Http404
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.views import APIView

from polls.models import Poll, UserPoll, Answer, Question
from polls.serializers import PollSerializer, QuestionSerializer, ChoiceSerializer


class PollId(APIView):
    def get(self, request, id):
        """ Получаем детализацию опроса по id """
        try:
            today = date.today()
            poll = Poll.objects.get(id=id)

            # проверяем опрос на акутальность по датам
            if poll.start_date > today or poll.finish_date < today:
                raise Poll.DoesNotExist()

            result = PollSerializer(poll).data
            result['questions'] = []

            # добавляем в контекст вопросы связаные с этим опросом
            for question in poll.question_set.all():
                context = QuestionSerializer(question).data
                context['choice'] = ChoiceSerializer(question.choice_set.all(), many=True).data
                result['questions'].append(context)

            return Response(result)

        except Poll.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)

    def post(self, request, id):
        """ Добавляем новый ответ """
        try:
            today = date.today()
            poll = Poll.objects.get(id=id)

            # проверяем опрос на акутальность по датам
            if poll.start_date > today or poll.finish_date < today:
                raise Poll.DoesNotExist()

            # проверяем тело запроса на наличие нужных параметров
            if not 'userId' in request.data:
                raise Exception('userId is missing')
            if not type(request.data['userId']) is int:
                raise Exception('Invalid userId')
            if not 'answers' in request.data:
                raise Exception('answers are missing')
            if not type(request.data['answers']) is dict:
                raise Exception('Invalid answers')

            userId = request.data['userId']
            answerDict = request.data['answers']

            # проверяем участвовал ли переданный userId в этом опросе
            if UserPoll.objects.filter(userId=userId, poll=poll).count() > 0:
                raise Exception('This user already has submitted to this poll')

            def makeAnswer(question: Question) -> Answer:
                """
                Создаем объект ответа из полученного вопроса.
                :param question: принимает объект Question.
                :return: возвращает объект Answer.
                """
                # проверяем есть ли этот вопрос в полученном POST запросе
                if not str(question.id) in answerDict:
                    raise Exception('Answer to question %d is missing' % question.id)

                answerData = answerDict[str(question.id)]
                answer = Answer(
                    question=question,
                    question_type=question.type,
                )

                invalidAnswerException = Exception('Invalid answer to question %d' % question.id)
                invalidIndexException = Exception('Invalid option index in answer to question %d' % question.id)

                if question.type == 'TEXT':
                    if not type(answerData) is str:
                        raise invalidAnswerException
                    answer.answer_text = answerData

                if question.type == 'CHOICE':
                    if not type(answerData) is int:
                        raise invalidAnswerException
                    choice = question.choice_set.filter(index=answerData).first()
                    if choice:
                        answer.answer_text = choice.text
                    else:
                        raise invalidIndexException

                if question.type == 'MULTIPLE_CHOICE':
                    if not type(answerData) is list:
                        raise invalidAnswerException
                    choice_list = question.choice_set.all()
                    result_list = []
                    # с помощью генератора получаем отмеченые варианты
                    for index in answerData:
                        choice_found = next((o for o in choice_list if o.index == index), None)
                        if choice_found:
                            result_list.append(choice_found.text)
                        else:
                            raise invalidIndexException
                    answer.answer_text = json.dumps(result_list)
                return answer

            # получаем список объектов Ответов
            answer_list = [makeAnswer(question) for question in poll.question_set.all()]
            print(answer_list)
            if len(answer_list) != poll.question_set.count():
                raise Exception('Not enough answers')

            userpoll = UserPoll(userId=userId, poll=poll)
            userpoll.save()
            for answer in answer_list:
                answer.user_poll = userpoll
                answer.save()

            return Response('Accepted')

        except Poll.DoesNotExist:
            raise Http404()
        except Exception as ex:
            raise ParseError(ex)
