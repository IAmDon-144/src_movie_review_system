from django.shortcuts import render, redirect
from .models import Movie, Category, Review, Reply
from profiles.models import Profile
from bs4 import BeautifulSoup
import requests
from sqlalchemy import null
from django.http import HttpResponse, JsonResponse
from .filters import PostFilter

# Create your views here.


def home(request):

    allMovies = Movie.objects.all()
    allCategory = Category.objects.all()
    myfilter = PostFilter(request.GET, allMovies)
    allMovies = myfilter.qs

    try:
        cusProfile = Profile.objects.get(user=request.user)
    except:
        cusProfile = "AnonymousUser"

    context = {
        "allMovie": allMovies,
        "allCategory": allCategory,
        "profile": cusProfile,
        'myfilter': myfilter,


    }
    return render(request, 'newsfeed.html', context)




def catagoryFilter(request,pk,title):

    allMovie = Movie.objects.filter(category=pk)
    try:
        cusProfile = Profile.objects.get(user=request.user)
    except:
        cusProfile = "AnonymousUser"

    context ={

        'allMovie':allMovie,
        'title':title,
        "profile":cusProfile

    }
    return render(request,'catagoryRes.html',context)




def getMovie(request, pk, title, code):

    allMovies = Movie.objects.all()
    myfilter = PostFilter(request.GET, allMovies)
    allMovies = myfilter.qs

    movie = Movie.objects.get(id=pk)
    try:
        cusProfile = Profile.objects.get(user=request.user)
    except:
        cusProfile = "AnonymousUser"

    allReview = movie.review_set.all()

    try:

        html_text = requests.get(
            'https://en.wikipedia.org/wiki/'+movie.title).text
        soup = BeautifulSoup(html_text, 'lxml')
        table = soup.find("table", class_="infobox vevent")

        rows = table.find_all('tr')
        keys = []
        values = []
        for row in rows[1:]:
            key = row.find_all('th')
            value = row.find_all('td')
            keyText = zip(key, value)

            notInclude = ['Countries', 'Based on', 'Language',
                          'Release dates', 'Productioncompanies', 'Country']

            for tr, td in keyText:
                if(tr.text not in notInclude):
                    keys.append(tr.text)
                    values.append(td.text)
        extraInfo = zip(keys, values)
    except:
        extraInfo = []

    context = {

        "movie": movie,
        'extraInfo': extraInfo,
        "allReview": allReview,
        "profile": cusProfile,
        'myfilter': myfilter,



    }
    return render(request, 'preview-movie.html', context)


def reviewPost(request, pk):
    user = request.user

    post = Movie.objects.get(id=pk)
    profile = Profile.objects.get(user=user)

    if request.method == 'POST' and request.POST['commnet-box'] != null:
        Review.objects.create(user=profile, post=post,
                              body=request.POST['commnet-box'])
        return redirect('preview-movie', pk=pk, code=post.code, title=post.title.replace(' ', '-')

                        )


def replyPost(request, pk):
    user = request.user

    post = Review.objects.get(id=pk)

    profile = Profile.objects.get(user=user)

    if request.method == 'POST' and request.POST['reply-box'] != null:
        Reply.objects.create(user=profile, comment=post,
                             body=request.POST['reply-box'])

        return redirect('see-replies', pk=pk)


def seeReplies(request, pk):
    review = Review.objects.get(id=pk)
    allReplies = review.reply_set.all()

    context = {
        "review": review,
        "allReplies": allReplies,
    }
    return render(request, 'allReplies.html', context)


def addLove(request):
    if request.method == 'POST':

        data = {
            'lvalue': 'Like',

        }
        profileID = request.POST['profileID']
        postID = request.POST['postID']

        profile = Profile.objects.get(id=profileID)
        post = Movie.objects.get(id=postID)

        if profile in post.liked.all():
            post.liked.remove(profile)
        else:
            post.liked.add(profile)
            data['lvalue'] = 'Unlike'

        return JsonResponse(data, safe=False)


def deleteReview(request, pk, ck):
    profile = Profile.objects.get(user=request.user)
    movie = Movie.objects.get(id=ck)

    comment = Review.objects.get(id=pk)
    if comment.user == profile:
        comment.delete()
        return redirect('preview-movie', pk=ck, code=movie.code, title=movie.title.replace(' ', '-'))

    else:
        return HttpResponse("You Are Not Authorized")


def showRatedlist(request):
    user = request.user

    if not request.user.is_authenticated:
        return redirect('/accounts/login.html')

    else:

        profile = Profile.objects.get(user=user)
        ratedList = []

        allMovie = Movie.objects.all()

        for movie in allMovie:
            if profile in movie.liked.all():
                ratedList.append(movie)

        context = {

            "ratedLists": ratedList
        }

        return render(request, 'rated.html', context)


def showTranding(request):
    allMovie = Movie.objects.all()
    try:
        cusProfile = Profile.objects.get(user=request.user)
    except:
        cusProfile = "AnonymousUser"

    movieID = []
    tranding = []

    for movie in allMovie:
        likeCount = movie.liked.all().count()
        tranding.append(likeCount)
        movieID.append(movie)

    zipped = list(zip(movieID, tranding))
    sorted_zipped = sorted(zipped, key=lambda x: x[1])
    sortedZippedReversed = (sorted_zipped[::-1])
    movie, liked = zip(*sortedZippedReversed)

    context = {

        "trandingList": movie[0:4],
        'profile': cusProfile
    }

    return render(request, 'tranding.html', context)



def about(request):
    return render(request, 'about.html',)


def help(request):
    return render(request, 'help.html',)


def contact(request):
    return render(request, 'contact.html',)
