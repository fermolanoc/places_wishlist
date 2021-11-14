from django.shortcuts import render, redirect, get_object_or_404
from django.conf.urls import url
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


@login_required
def place_list(request):
    """ If this is a POST request , the user clicked the Add button in the form.
    Check if the new place is valid, if so, save a new place into DB and redirect to this same page.
    This creates a GET request to this same route.

    If NOT a POST route, or place is not valid, display the page with  a list of places and a form to add a new Place
    """

    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False)  # create a new Place from the form
        place.user = request.user  # associate the place with the logged-in user
        if form.is_valid():  # check against DB constraints, for example are required fields present?
            place.save()  # saves to DB
            # redirect to GET view with name place_list - which is the same view
            return redirect('place_list')

    # If not a POST, or the form is not valid, render the page
    # with the form to add a new Place, and list of places
    places = Place.objects.filter(user=request.user).filter(
        visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


@login_required
def places_visited(request):
    # Get all places that have been visited by current user, and order them by name to be shown on screen
    visited = Place.objects.filter(user=request.user).filter(
        visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        # only let a user edit their own places
        if (place.user == request.user):
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()\

    return redirect('place_list')  # take back to homepage


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # Does this place belong to the user?
    if place.user != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        # instance is the model object to update with the form data

        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            # temp error version, needs improvement
            messages.error(request, form.errors)
        return redirect('place_details', place_pk=place_pk)

    else:  # Get place details
        if place.visited:
            # pre-populate with data from this Place instance
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_details.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_details.html', {'place': place})


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    # let a user deletes own places
    if place.user == request.user:
        place.delete()
        # return to homepage after deleting a Place
        return redirect('place_list')
    else:
        return HttpResponseForbidden()
