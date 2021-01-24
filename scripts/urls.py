from django.urls import path, re_path
from scripts.views import report, report_edit_1, script_list, nowy_form


urlpatterns = [
    path('report/int<script_id>', report, name='report'),
    path('list/', script_list, name='list'),
    re_path(r'report/script_id.*', report_edit_1),
    path('nowy_form/', nowy_form),
]