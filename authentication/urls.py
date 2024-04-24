from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_page,name="register" ),
    path('register_take_photo/<int:id>/',views.take_photo,name="register_photo" ),
    path('save_image/', views.save_image, name='save_image'),
    path('home/',views.home,name="home" ),
    path('login_verify/',views.login_verify,name="login" ),
    path('photo_verify/<int:id>/',views.photo_verify,name="photo_verify" ),
    path('web_feed/<int:id>/',views.web_feed,name="web_feed" ),
    path('ballot_collection/<int:id>/',views.ballot_collection,name="ballot_collection" ),
    path('verify_face/<int:id>/',views.verify_face,name="verify_face" ),
    path('logout/',views.logout,name="logout" ),


]