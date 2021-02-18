from django.urls import path, include

from .views.admin.poll_id import AdminPollId
from .views.admin.polls import AdminPolls
from .views.admin.question_id import AdminQuestionId
from .views.admin.questions import AdminQuestions
from .views.user.poll_Id import PollId
from .views.user.poll_list_view import PollListAPIView
from .views.user.polls_user_id import PollsUserID

urlpatterns = [
    path('user/polls', PollListAPIView.as_view(), name='polls'),
    path('user/polls/<int:id>', PollId.as_view(), name='polls'),
    path('user/polls_from_user/<int:user_id>', PollsUserID.as_view(), name='polls_from_user'),
    path('admin/polls', AdminPolls.as_view()),
    path('admin/polls/<int:id>', AdminPollId.as_view()),
    path('admin/polls/<int:id>/questions', AdminQuestions.as_view()),
    path('admin/polls/<int:poll_id>/questions/<int:question_id>', AdminQuestionId.as_view()),
]
