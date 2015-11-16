from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Thread, Comment
from .forms import ThreadModelForm, CommentModelForm

# This code is written for an assignment, whose directions state:

# The "Forum" is a single-page application with the following functionality:
# The app has a Welcome page with a list of Threads
# The Welcome page also has a form where visitors can anonymously create new Threads (no need for a User model or for signup / authentication / etc)
# Clicking a Thread should bring up the "Thread Detail View"
# The Thread Detail View should show the Thread's child Comments and a form to (anonymously) submit a new Comment

def index(request):
    """Main function that gets called when the user lands on the webpage"""

    # get forum thread objects, ordered by publication date
    forumthreads = Thread.objects.order_by('pub_date')

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ThreadModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ThreadModelForm()

    # render the page, passing a dict that holds the form as well as all threads
    return render(request, 'forum/index.html', {'myform': form, 'mythreads': forumthreads})
