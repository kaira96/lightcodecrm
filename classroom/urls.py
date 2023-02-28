from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('class/<int:id>/', views.render_class, name='render_class'),
    path('unenroll_class/<int:classroom_id>/', views.unenroll_class, name='unenroll_class'),
    path('delete_class/<int:classroom_id>/', views.delete_class, name='delete_class'),
    path('create_class_request/', views.create_class_request, name='create_class_request'),
    path('join_class_request/', views.join_class_request, name='join_class_request'),
    path('create_assignment/<int:classroom_id>/', views.create_assignment, name='create_assignment'),
    path('assignment_summary/<int:assignment_id>/', views.assignment_summary, name='assignment_summary'),
    path('delete_assignment/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    # path('submit_assignment_request/<int:assignment_id>/', views.submit_assignment_request, name='submit_assignment_request'),
    path('mark_submission_request/<int:submission_id>/', views.mark_submission, name='mark_submission'),
    path('sending_a_task/<int:pk>/', views.sending_a_task, name='sending_a_task'),
    # path('group_list/<int:pk>/', views.group_list, name='group_list'),
    # path('add_student/<int:pk>/', views.add_student, name='add_student'),
]
