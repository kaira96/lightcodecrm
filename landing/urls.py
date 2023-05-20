from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('course-detail/<slug:slug>/', views.course_detail, name='course-detail'),
    path('employee_detail/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('personal_area/', views.personal_area, name='personal_area'),
    path('category/', views.category_view, name='tutorials'),
    path('category/<slug:slug>/', views.category_detail, name='tutorial-detail'),
    path('tutorial-content/<slug:slug>/', views.theme_view, name='tutorial-content'),
    path('content-view/<slug:slug>/', views.content_view, name='content_view'),
    path('add-category/', views.add_category, name='add_category'),
    path('add-article/', views.add_article, name='add_article'),
    path('registration/', views.register_view, name='registration'),
    path('authentication/', views.authentication_view, name='authentication'),
    path('logout/', views.logout_view, name='exit'),
    path('add-url-stream/', views.add_url_stream, name='add_url_stream'),
    path('article-list/', views.article_list, name='article_list'),
    path('article-detail/<int:pk>/', views.article_detail, name='article_detail'),
    path('article-delete/<int:pk>/', views.article_delete, name='article_delete'),
]
