from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
import urllib


class SocialLoginRedirect(RedirectView):
    permanent = False

    def get_redirect_url(self):
        return '/social/login/checkio/?' + urllib.urlencode({'next': self.request.GET.get('next', '/')})

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'checkio_forum.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^user/login/', SocialLoginRedirect.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('spirit.urls')),
)