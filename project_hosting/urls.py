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
    # url(r'^db', sexy_timetable.views.db, name='db'),
    url(r'^signup$', sexy_timetable.views.UserFormView.as_view(), name='signup'),
    url(r'^signup_success$', sexy_timetable.views.signup_success, name='signup_success'),
    path('admin/', admin.site.urls),
]
