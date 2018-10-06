from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import sexy_timtable.views

# Examples:
# url(r'^$', 'project_hosting.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', sexy_timtable.views.index, name='index'),
    url(r'^db', sexy_timtable.views.db, name='db'),
    path('admin/', admin.site.urls),
]
