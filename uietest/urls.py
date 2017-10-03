from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from registration.views import PDFDetailView, StudentSignupView, LandingView, ActivateStudentAccountView, NewLoginView
from django.conf import settings
from django.conf.urls.static import static
from exams.views import ProfileView


urlpatterns = [
    url(r'^profiledetail/', ProfileView.as_view()),
    url(r'^admin/changestatus/student/(?P<pk>[-\w]+)/(?P<phone>[-\w]+)',
        ActivateStudentAccountView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="home.html")),
    url(r'^accounts/profile/', LandingView.as_view()),
    url(r'^accounts/pdf/(?P<pk>[-\w]+)/(?P<phone>[-\w]+)',
        PDFDetailView.as_view()),
    url(r'^accounts/signup/', StudentSignupView.as_view()),
    url(r'^accounts/login/', NewLoginView.as_view()),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^tests/', include('exams.urls'))

]

if (settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
