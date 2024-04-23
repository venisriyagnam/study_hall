from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from UBStudyHallApp.models import *
from django.contrib.auth.models import User
from .models import *
from django.utils import timezone
from datetime import timedelta, datetime
from django.shortcuts import get_object_or_404

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            # Correct username and password, log the user in
            login(request, user)
            user_role = UserRole.objects.get(username = username)
            print(user_role)
            if user_role:
                if user_role.user_role == 'admin':
                    return redirect('/ubstudyhall/studyhall-reservations/')
            # Redirect to a success page
            return redirect('/ubstudyhall/home/')  # Replace '/success/' with your desired success URL
        else:
            # Return an 'invalid login' error message
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        # Logic to handle registration form submission
        # Extract form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        Points.objects.create(username = username, points = 0)
        user_role = UserRole.objects.create(username = username)

        # Perform additional operations like sending a verification email, etc.
        # For example:
        # send_verification_email(email)

        # Redirect the user to a login page after successful registration
        return redirect('/ubstudyhall/login')

    return render(request, 'register.html')

def forgot_password(request):
    if request.method == 'POST':
        # Logic to handle forgot password form submission
        # Extract the email from the form
        email = request.POST.get('email')

        # Here, you'd implement logic to validate the email and reset the password
        # This might involve generating a unique token, sending a reset link to the user's email, etc.
        # For example, sending a reset link via email could be done like this:
        # send_mail(
        #     'Password Reset',
        #     'Here is your password reset link: <reset_link>',
        #     'from@example.com',
        #     [email],
        #     fail_silently=False,
        # )

        # Redirect the user to a page indicating that a password reset link has been sent
        return render(request, 'password_reset_sent.html')

    return render(request, 'forgot_password.html')

def home(request):
    # Add logic here to fetch the user's username if they're logged in
    # For example, if you're using Django's built-in authentication
    username = ''
    if request.user.is_authenticated:
        username = request.user.username

    return render(request, 'home.html', {'username': username})  

def reserve(request):
    # Fetch all available rooms that are not reserved
    print(request.user)
    all_rooms = {}
    available_rooms = []
    reservation_time = ''
    reservation_date = ''
    timings = []

    for hour in range(5, 24):
        start_time = f"{hour % 12 if hour % 12 != 0 else 12}:00{'am' if hour < 12 else 'pm'}"
        end_time = f"{(hour + 1) % 12 if (hour + 1) % 12 != 0 else 12}:00{'am' if (hour + 1) < 12 else 'pm'}"
        timings.append(f"{start_time} - {end_time}")

    all_rooms = Room.objects.values()
    print(request.POST)
    if request.POST:
        print('came here')
        post_data = request.POST
        reservation_time = post_data['reservation_time']
        reservation_date = post_data['reservation_date']
        reserved_rooms = list(Reserve.objects.filter(reserve_date = post_data['reservation_date'], \
                    reserve_timestamp = post_data['reservation_time']).values_list('room_id', flat = True))
        
        total_rooms = list(Room.objects.values_list('room_number', flat = True))
        available_rooms = [i for i in total_rooms if i not in reserved_rooms]
        print(available_rooms)
        print(total_rooms)
        print(reserved_rooms)
        print(post_data.keys())
        post_data = dict(post_data)
        if 'reservation_id' in post_data.keys():
            return render(request, 'modify_html.html', {'all_rooms':all_rooms, 'timings': timings, \
                'available_rooms': available_rooms, 'reservation_time':reservation_time, \
                'reservation_date': reservation_date, 'user':request.user, 'reservation_id':post_data['reservation_id'][0]})

        else:
            print('came here')
            return render(request, 'reserve_room.html', {'all_rooms':all_rooms, 'timings': timings, \
                'available_rooms': available_rooms, 'reservation_time':reservation_time, \
                'reservation_date': reservation_date, 'user':request.user})

    
    return render(request, 'reserve_room.html', {'all_rooms':all_rooms, 'timings': timings, \
                'available_rooms': available_rooms, 'reservation_time':reservation_time, \
                'reservation_date': reservation_date, 'user':request.user})

def room_reserve(request):
    if request.POST:
        post_data = request.POST
        print(post_data)
        room_number = [int(i.split('reserve_')[1]) for i in post_data.keys() if 'reserve_' in i]
        room_number = room_number[0] if room_number else None
        room_reserve = Reserve.objects.filter(reserve_date = post_data['reservation_date'], \
                    reserve_timestamp = post_data['reservation_time'], room_id = room_number, \
                    user_name = str(request.user))

        if not room_reserve:
            room_reserve = Reserve.objects.create(reserve_date = post_data['reservation_date'], \
                    reserve_timestamp = post_data['reservation_time'], room_id = room_number, \
                    user_name = str(request.user))
            points = Points.objects.filter(username = str(request.user)).values()
            if points:
                points = points[0]['points'] + 10
                Points.objects.filter(username = str(request.user)).update(points = points)
            else:
                Points.objects.create(username = str(request.user), points = 10)

        return render(request, 'reserved_successfully.html')
    return redirect('/ubstudyhall/reserve/')

def past_reservations(request):
    username = str(request.user)

    # Get the current date and time
    current_date = datetime.now().date()
    current_time = datetime.now().time()

    # Fetch all reservations for the current user
    all_reservations = Reserve.objects.filter(user_name=username)

    # Separate past and upcoming reservations based on date and time
    past_reservations = []
    upcoming_reservations = []
    
    for reservation in all_reservations:
        # Convert the stored time string to a datetime.time object
        print(reservation.reserve_timestamp)
        reserve_time = datetime.strptime(((reservation.reserve_timestamp).split(' - '))[0], '%I:%M%p').time()
        reserve_date = datetime.strptime(reservation.reserve_date, '%Y-%m-%d').date()

        # Check if the reservation date is in the past or future
        if reserve_date < current_date:
            past_reservations.append(reservation)
        elif reserve_date == current_date:
            # Check if the reservation time is in the past or future
            if reserve_time <= current_time:
                past_reservations.append(reservation)
            else:
                upcoming_reservations.append(reservation)
        else:
            upcoming_reservations.append(reservation)

    # Pass the past and upcoming reservations data to the template
    return render(
        request,
        'past_reservations.html',
        {'past_reservations': past_reservations, 'upcoming_reservations': upcoming_reservations}
    )

def reservation_cancel(request):
    if request.POST:
        post_data = request.POST
        print(post_data)
        reservation = get_object_or_404(Reserve, pk=int(post_data['reservation_id']))
        reservation.delete()
        user = Points.objects.get(username = str(request.user))
        if user.points >= 10:
            user.points -= 10
        user.save()
        return render(request, 'reservation_deleted.html')

    return redirect('/ubstudyhall/past_reservations/')

def modify_html(request):

    if request.POST:
        post_data = dict(request.POST)
        del post_data['csrfmiddlewaretoken']
        for key, value in post_data.items():
            post_data[key] = value[0]
        print(post_data)
        timings = []

        for hour in range(5, 24):
            start_time = f"{hour % 12 if hour % 12 != 0 else 12}:00{'am' if hour < 12 else 'pm'}"
            end_time = f"{(hour + 1) % 12 if (hour + 1) % 12 != 0 else 12}:00{'am' if (hour + 1) < 12 else 'pm'}"
            timings.append(f"{start_time} - {end_time}")
        post_data['timings'] = timings
        return render(request, 'modify_html.html', post_data)

    return redirect('/ubstudyhall/past_reservations/')

def modify_reservation(request):
    if request.POST:
        post_data = request.POST
        print(post_data)
        room_number = 0
        for i in post_data.keys():
            if 'reserve_' in i:
                room_number = int(i.split('reserve_')[1])
        modify_reservation = Reserve.objects.filter(reserve_id=int(post_data['reservation_id'])).update(reserve_date=post_data['reservation_date'], \
            reserve_timestamp=post_data['reservation_time'], room_id = room_number)

    return redirect('/ubstudyhall/past-reservations/')

def points(request):
    points = Points.objects.filter(username = str(request.user))
    if not points:
        points = Points.objects.create(username = str(request.user))
    points = Points.objects.filter(username = str(request.user)).values()[0]
    points = {'username':points['username'], 'points':points['points']}
    return render(request, 'points.html', points)

def about_us(request):
    return render(request, 'about_us.html', {'user':request.user})

def admin_view(request):
    all_reservations = Reserve.objects.all()
    return render(request, 'admin_view.html', {'user':request.user, 'all_reservations':all_reservations})

def contact_us(request):
    if request.method == 'POST':
        print(request.POST)
        post_data = request.POST
        username = post_data['name']
        email = post_data['email']
        message = post_data['message']
        feedback = Feedback.objects.create(username = username, email = email, message = message)
        return render(request, 'feedback_successful.html')

    return render(request, 'contact_us.html', {'user':request.user})

def all_feedbacks(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback.html', {'user':request.user, 'all_feedbacks':feedbacks})