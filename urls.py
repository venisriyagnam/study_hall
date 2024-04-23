from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('home/', views.home, name='home'),
    path('reserve/',views.reserve, name = 'reserve'),
    path('room-reserve/', views.room_reserve, name = 'room_reserve'),
    path('past-reservations/', views.past_reservations, name = 'past_reservations'),
    path('reservation-cancel/',views.reservation_cancel, name = 'reservation_cancel'),
    path('modify-html/', views.modify_html, name = 'modify_html'),
    path('modify-reservation/', views.modify_reservation, name = 'modify_reservation'),
    path('points/', views.points, name = 'points'),
    path('about-us/', views.about_us, name = 'about_us'),
    path('studyhall-reservations/', views.admin_view, name = 'admin_view'),
    path('contact-us/', views.contact_us, name = 'contact_us'),
    path('all-feedbacks/', views.all_feedbacks, name = 'all_feedbacks'),
]