from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie,Theater,Seat,Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator

def movie_list(request):
    search_query=request.GET.get('search')
    if search_query:
        movies=Movie.objects.filter(name__icontains=search_query)
    else:
        movies=Movie.objects.all()
            # Add pagination
        paginator = Paginator(movies, 2)  # Show 10 movies per page
        page_number = request.GET.get('page')  # Get the current page number from the request
        page_obj = paginator.get_page(page_number)
    return render(request, 'movies/movie_list.html', {'page_obj': page_obj})

def theater_list(request,movie_id):
    movie = get_object_or_404(Movie,id=movie_id)
    theaters=Theater.objects.filter(movie=movie)
    print("theaters",theaters)
    for theater in theaters:
        print("teater",theater)
        print("theater.dynamic_price()  ",theater.dynamic_price())
        theater.dynamic_price_display = theater.dynamic_price()  
        print("finally",theater)
    return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theaters})



@login_required(login_url='/login/')
def book_seats(request,theater_id):
    theaters=get_object_or_404(Theater,id=theater_id)
    seats=Seat.objects.filter(theater=theaters)
    if request.method=='POST':
        selected_Seats= request.POST.getlist('seats')
        error_seats=[]
        if not selected_Seats:
            return render(request,"movies/seat_selection.html",{'theater':theater,"seats":seats,'error':"No seat selected"})
        for seat_id in selected_Seats:
            seat=get_object_or_404(Seat,id=seat_id,theater=theaters)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters
                )
                seat.is_booked=True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)
        if error_seats:
            error_message=f"The following seats are already booked:{',',join(error_seats)}"
            return render(request,'movies/seat_selection.html',{'theater':theater,"seats":seats,'error':"No seat selected"})
        return redirect('profile')
    return render(request,'movies/seat_selection.html',{'theaters':theaters,"seats":seats})




