from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='main_page'),
    path("select2/", include("django_select2.urls")),
    path('user-ban/', views.user_ban, name='user_ban'),
    path('question-list/', views.QuestionList.as_view(), name='question_list'),
    path('topic-detail/<slug:slug>/', views.topic_detail_views, name='topic_detail'),
    path('question-detail/<int:pk>/', views.question_detail_view, name='question_detail'),
    path('banned-list/', views.banned_list_view, name='banned_list'),
    path('user-delete/<int:pk>', views.user_delete, name='user_delete'),
    path('question-delete/<int:pk>', views.question_delete, name='question_delete'),
    path('comment-delete/<int:pk>', views.comment_delete, name='comment_delete'),
]
