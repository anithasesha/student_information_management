
from django.urls import path, include
from . import views, LoginViews
from .views import StudentDetailsFilterView

urlpatterns = [
    path('', LoginViews.loginPage, name="login"),
    path('doLogin/', LoginViews.doLogin, name="doLogin"),
    path('get_user_details/', LoginViews.get_user_details, name="get_user_details"),
    path('logout_user/', LoginViews.logout_user, name="logout_user"),
    # path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('add_student/', views.add_student, name="add_student"),
    path('add_student_save/', views.add_student_save, name="add_student_save"),
    path('edit_student/<student_id>', views.edit_student, name="edit_student"),
    path('edit_student_save/', views.edit_student_save, name="edit_student_save"),    
    path('delete_student/<student_id>/', views.delete_student, name="delete_student"),
    path('print_tc/<student_id>/', views.print_tc, name="print_tc"),
    path('admin_profile/', LoginViews.admin_profile, name="admin_profile"),
    path('admin_profile_update/', LoginViews.admin_profile_update, name="admin_profile_update"),
    path('students/', StudentDetailsFilterView.as_view(), name='student_list')
]
