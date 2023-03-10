from django.urls import path, re_path
from scripts.views import report, report_edit, report_show, script_list, source

urlpatterns = [
    path('report/ID<script_ID>', report, name='report'),
    path('list/', script_list, name='list'),
    re_path(r'report/script_id.*;id.*', report_edit),
    re_path(r'report/script_id.*', report_show),
    path('source/ID<script_ID>', source, name='source'),
]