from django.urls import path
from rest_framework import routers

from . import views


app_name = 'api'

router = routers.DefaultRouter()
router.register('service', views.ServiceView, basename='service')
router.register('administration', views.AdministrationView, basename='administration')
router.register('department', views.DepartmentView, basename='department')
router.register('group', views.GroupView, basename='group')
routers_urls = router.urls


urlpatterns = [
    path('management-struct/', views.management_struct_view, name='management_struct_view'),
    path('employee/', views.EmployeeCreateListView.as_view(), name='employee_list_create'),
    path(
        'employee/<int:pk>/',
        views.EmployeeRetrieveUpdateDeleteView.as_view(),
        name='employee_retrieve_update_delete',
    ),
]

urlpatterns += routers_urls
