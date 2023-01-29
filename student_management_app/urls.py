
from django.urls import path, include
from . import views, LoginViews

urlpatterns = [
    path('login/', LoginViews.loginPage, name="login"),
    path('doLogin/', LoginViews.doLogin, name="doLogin"),
    path('get_user_details/', LoginViews.get_user_details, name="get_user_details"),
    path('logout/', LoginViews.logout_user, name="logout_user"),
    # path('', views.students, name="students"),
    # path('students/', views.students, name="students"),
    path('', views.StudentDetailsView.as_view(), name="students"),
    path('students/', views.StudentDetailsView.as_view(), name="students"),
    path('students/add', views.add_student, name="add_student"),
    path('students/add/save/', views.add_student_save, name="add_student_save"),
    path('students/<student_id>/', views.view_student, name="view_student"),
    path('students/<student_id>/edit', views.edit_student, name="edit_student"),
    path('students/<student_id>/edit/save/', views.edit_student_save, name="edit_student_save"),    
    path('students/<student_id>/delete/', views.delete_student, name="delete_student"),
    path('students/<student_id>/tc/', views.print_tc, name="print_tc"),
    path('profile/', LoginViews.profile, name="profile"),
    path('profile/update/', LoginViews.profile_update, name="profile_update"),
]
