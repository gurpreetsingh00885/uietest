from django.conf.urls import url, include
from django.contrib import admin

from registration.views import StudentSignupView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/signup/', StudentSignupView.as_view()),
    url(r'^accounts/', include('allauth.urls')),
]
