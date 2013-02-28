from django.conf.urls.defaults import *

urlpatterns = patterns('',
    ('^$', 'core.views.appstart'),
    ('^addapp/$', 'core.views.callback_app_start'),
    ('^removeapp/$', 'core.views.callback_app_start'),
    ('^friends_info/$', 'core.views.friends_info'),
    ('^gadget/$', 'core.views.gadget'),
)
