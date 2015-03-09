from django.shortcuts import render

from rango.models import Category
from rango.models import Page
from rango.models import UserProfile
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query
from django.shortcuts import redirect
from django.contrib.auth.models import User
from rango.forms import UserForm, UserProfileForm



def index(request):

    request.session.set_test_cookie()

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)
    return response

def about(request):
    context_dict = {}
    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    if request.session.get('visits'):
        visits = request.session.get('visits')
    else:
        visits = 0
    context_dict['about_us'] = "This tutorial has been put together by Hamza Tanveer, 2105272T!"
    context_dict['visits'] = visits
    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    if not context_dict['query']:
        context_dict['query'] = category.name

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

def search(request):
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)

def profile(request, username):
    context_dict = {}
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)
    context_dict['user_name'] = user.username
    context_dict['user_email'] = user.email
    context_dict['userprofile'] = profile
    return render(request, 'rango/profile.html', context_dict)

def search_users(request):
    user_name = User.objects.all()
    return render(request, 'rango/search_users.html', {'users':user_name})

@login_required
def edit_profile(request):
    context_dict = {}
    if request.method == 'POST':
        user_profile_form = UserProfileForm(data=request.POST, instance=request.user.userprofile)
        if user_profile_form.is_valid():
            if request.user.is_authenticated():
                user_profile = UserProfile.objects.get(user_id=request.user.id)
                if 'picture' in request.FILES:
                    user_profile.picture = request.FILES['picture']
                if 'website' in user_profile_form.cleaned_data:
                    user_profile.website = user_profile_form.cleaned_data['website']

                user_profile.save()

            profile = UserProfile.objects.get(user=request.user)
            context_dict['user_name'] = request.user.username
            context_dict['user_email'] = request.user.email
            context_dict['userprofile'] = profile
            return render(request, 'rango/profile.html', context_dict)
    else:
        user_profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request,'rango/edit_profile.html',{'profile_form':user_profile_form})

def register_profile(request):
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST)
        if user_profile_form.is_valid():
            if request.user.is_authenticated():
                user_profile = user_profile_form.save(commit = False)
                user = User.objects.get(id=request.user.id)
                user_profile.user = request.user

            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
                user_profile.website = user_profile_form.cleaned_data['website']
                user_profile.save()
            return redirect('/rango/')
    else:
        user_profile_form = UserProfileForm()
    return render(request,'rango/profile_registration.html', {'profile_form': user_profile_form})