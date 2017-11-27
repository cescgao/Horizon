# -*-encoding: utf-8 -*-
#
# @author gaoyuan
#
# Jan 2016


from django.conf.urls import url, include


urlpatterns = [
    url(r'^account/', include('sigma_account.frontend_urls')),
    url(r'', include('sigma_home.frontend_urls')),
    url(r'^project/', include('sigma_project.frontend_urls')),
]


urlpatterns += [
    url(r'^api/account/', include('sigma_account.backend_urls')),
    url(r'^api/home/', include('sigma_home.backend_urls')),
    url(r'^api/projects/', include('sigma_project.backend_urls')),
]
