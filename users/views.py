from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .forms import UserRegisterForm, UserUpdateForm
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from movies.models import Movie , Booking,Theater
from django.core.paginator import Paginator
def home(request):
    # Retrieve all movies
    movies = Movie.objects.all()

    # Create a list of movies and their timings
    movie_data = []
    for movie in movies:
        timings = Theater.objects.filter(movie=movie).values('name', 'time')
        movie_data.append({'movie': movie, 'timings': list(timings)})

    # Paginate the movie data
    paginator = Paginator(movie_data, 2)  # Adjust '2' to the desired number of items per page
    page_number = request.GET.get('page')
    page_movies = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_movies': page_movies})


def register(request):
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('profile')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('/')
    else:
        form=AuthenticationForm()
    return render(request,'users/login.html',{'form':form})

@login_required
def profile(request):
    bookings= Booking.objects.filter(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'u_form': u_form,'bookings':bookings})

@login_required
def reset_password(request):
    if request.method == 'POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'users/reset_password.html',{'form':form})