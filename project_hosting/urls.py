from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import sexy_timetable.views

# Examples:
# url(r'^$', 'project_hosting.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    # url(r'^$', sexy_timetable.views.index, name='index'),
    url(r'^db', sexy_timetable.views.db, name='db'),
    # url(r'^signup/$', sexy_timetable.views.signup, name='signup'),
    url(r'^/$', sexy_timetable.views.signup, name='signup'),
    path('admin/', admin.site.urls),
]
