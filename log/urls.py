
from django.urls import path
from .views import sign_in, post_logged, logout, signup, post_signup, create, post_create, reset, postReset, firebase_facebook


urlpatterns = [
    path('', sign_in, name='sign'),
    path('post_logged', post_logged, name='home-page'),
    path('signup', signup, name='sign-up'),
    path('post_signup', post_signup, name='post_signup'),
    path('create', create, name='create'),
    path('post_create', post_create, name='post_create'),
    path('reset/', reset),
    path('postReset/', postReset),
    path('facebook', firebase_facebook, name='facebook'),

    # path('logout', logout, name='logout'),
]

# c2f4b099f7a5eb5ab00927c9e0a34bc5
# 1693469637779315