from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Thread, Comment
from .forms import ThreadModelForm, CommentModelForm
import datetime, pytz
# import json

# This code is written for an assignment, whose directions state:

# The "Forum" is a single-page application with the following functionality:
# The app has a Welcome page with a list of Threads
# The Welcome page also has a form where visitors can anonymously create new Threads (no need for a User model or for signup / authentication / etc)
# Clicking a Thread should bring up the "Thread Detail View"
# The Thread Detail View should show the Thread's child Comments and a form to (anonymously) submit a new Comment

def justTesting(request):
    return HttpResponse("Hello, world")

def index(request):
    """Main function that gets called when the user lands on the webpage"""

    # get forum thread objects, ordered by publication date
    forumthreads = Thread.objects.order_by('pub_date')

    # this code block uses a page refresh after form submission
    # instead, we're going to use ajax

    # from: https://docs.djangoproject.com/en/1.8/topics/forms/
    # if this is a POST request we need to process the form data
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = ThreadModelForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         # process the data in form.cleaned_data as required
    #         # ...
    #         # redirect to a new URL:
    #         return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    # else:
    #    form = ThreadModelForm()

    form = ThreadModelForm()

    # render the page, passing a dict that holds the form as well as all threads
    return render(request, 'forum/index.html', {'myform': form, 'mythreads': forumthreads})

def create_post(request):
    """Function to create thread (or post), called by javascript AJAX"""

    # modified from: https://realpython.com/blog/python/django-and-ajax-form-submissions/

    if request.method == 'POST':

        # get data
        mytitle = request.POST.get('mytitle')
        myusername = request.POST.get('myusername')
        mydescription = request.POST.get('mydescription')

        # save in database
        post = Thread(pub_date = datetime.datetime.now(pytz.timezone('US/Eastern')), username = myusername, title = mytitle, description = mydescription)
        post.save()

        # create response data dict
        response_data = {
			    'title': mytitle,
			    'description': mydescription,
			    'username': myusername,
			}

        # return HttpResponse( json.dumps(response_data), content_type="application/json")
        return JsonResponse(response_data)

    else:
    
        # return HttpResponse( json.dumps({"nothing": "fail"}), content_type="application/json")
        return JsonResponse({"nothing": "to see here!"})
