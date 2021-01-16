from django.urls import path, re_path
from scripts.views import report, report_edit, script_list


urlpatterns = [
    path('report/int<script_id>', report, name='report'),
    path('list/', script_list, name='list'),
    re_path(r'report/script_id.*', report_edit),
]