from django.contrib.auth import authenticate, login, logout
from django.db.models import Max
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea, HiddenInput
from django.contrib.auth.decorators import login_required

from .models import *

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
        widgets = {
            'description': Textarea(attrs={'cols':80, 'row':20}),
        }

def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.all()
    })

@login_required(login_url='/login')
def listing(request, listing):
    listings = Listing.objects.get(id=listing)
    max_val = listings.bids.aggregate(Max('bid')) ['bid__max']

    if max_val != None:
        highest_condition = max_val + 1
        winner = listings.bids.get(bid=max_val)
    else:
        highest_condition = listings.starting_bid + 1
        winner = "None"

    if request.user.is_authenticated:
        username = User.objects.get(username=request.user)
    else:
        username = "Stranger"

    if request.method == "POST":
        if username not in listings.interested_buyers.all():
            listings.interested_buyers.add(username)
        else:
            listings.interested_buyers.remove(username)

    return render(request, "auctions/listing.html", {
        'listings': listings, 
        'username': username,
        'bidding': listings.bids.all(),
        'bids': listings.bids.all().count(), 
        'highest': highest_condition ,
        'winner': winner,
        'condition': username not in listings.interested_buyers.all(), 
        'comments': listings.comments.all()
    })

@login_required(login_url='/login')
def new(request):
    form = ListingForm(request.POST)

    if form.is_valid():
        if request.user.is_authenticated:
            new = form.save(commit=False)
            new.user = request.user
            new.save()
            return HttpResponseRedirect(reverse("listing", kwargs={'listing':new.id}))
        
    return render(request, "auctions/new.html", {
        'form': form
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all()
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def watchlist(request):
    if request.user.is_authenticated:
        username = User.objects.get(username=request.user)
        return render(request, "auctions/index.html", {
            'listings': username.watchlist.all(),
            'watchlist': True
        })


@login_required(login_url='/login')
def bid(request, listing):
    if request.POST:
        bid = request.POST["bid"]
        if request.user.is_authenticated:
            username = User.objects.get(username=request.user)
        listings = Listing.objects.get(id=listing)
        new_bid = Bids(bid=bid, user=username, listing=listings)
        new_bid.save()

    return HttpResponseRedirect(reverse("listing", kwargs={'listing':listing}))


@login_required(login_url='/login')
def comment(request, listing):
    if request.POST:
        comment = request.POST["comment"]
        if request.user.is_authenticated:
            username = User.objects.get(username=request.user)
        listings = Listing.objects.get(id=listing)
        new_comment = Comments(comment=comment, user=username, listing=listings)
        new_comment.save()

    return HttpResponseRedirect(reverse("listing", kwargs={'listing':listing}))


def category(request, category):

    category_name = Category.objects.get(name=category)

    return render (request, "auctions/category.html", {
        'category_name': category,
        'category': category_name.listings.all()
    })


@login_required(login_url='/login')
def close(request, listing):
    if request.POST:
        the_listing = Listing.objects.get(id=listing)
        the_listing.is_active = False
        the_listing.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing':listing}))