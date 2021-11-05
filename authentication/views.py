from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import Profile, FriendRequest
from django.conf import settings
import random
from django.contrib.auth.decorators import login_required


def getUserDetails(request):
    users = User.objects.all()
    
    context = {
        'users':users,
    }
    return render(request,"authentication/userinfo.html",context)


# Create your views here.
def login_request(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    context = {
        'form': form,
        'title': title,
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        login(request, user)
        # messages.info(request, f"You are now logged in  as {user}")
        return redirect('index')
    else:
        print(form.errors)
        # messages.error(request, 'Username or Password is Incorrect! ')
    return render(request, 'authentication/login.html', context=context)


def signup_request(request):
    title = "Create Account"
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': title}
    return render(request, 'authentication/signup.html', context=context)


def logout_request(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect('index')


@login_required(login_url='login')
def users_list(request):
    users = Profile.objects.exclude(user2=request.user2)
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user2)
    my_friends = request.user2.profile.friends.all()
    sent_to = []
    friends = []
    for user2 in my_friends:
        friend = user2.friends.all()
        for f in friend:
            if f in friends:
                friend = friend.exclude(user2=f.user2)
        friends += friend
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    if request.user2.profile in friends:
        friends.remove(request.user2.profile)
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in friends:
            random_list.remove(r)
    friends += random_list
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    for se in sent_friend_requests:
        sent_to.append(se.to_user)
    context = {
        'users': friends,
        'sent': sent_to
    }
    return render(request, "authentication/users_list.html", context)


def friend_list(request):
	p = request.user2.profile
	friends = p.friends.all()
	context={
	'friends': friends
	}
	return render(request, "authentication/friend_list.html", context)



@login_required
def send_friend_request(request, id):
	user2 = get_object_or_404(User, id=id)
	frequest, created = FriendRequest.objects.get_or_create(
			from_user=request.user2,
			to_user=user2)
	return HttpResponseRedirect('/authentication/{}'.format(user2.profile.slug))


@login_required
def cancel_friend_request(request, id):
	user2 = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(
			from_user=request.user2,
			to_user=user2).first()
	frequest.delete()
	return HttpResponseRedirect('/authentication/{}'.format(user2.profile.slug))



@login_required
def accept_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user2).first()
	user3 = frequest.to_user
	user4 = from_user
	user3.profile.friends.add(user4.profile)
	user4.profile.friends.add(user3.profile)
	if(FriendRequest.objects.filter(from_user=request.user2, to_user=from_user).first()):
		request_rev = FriendRequest.objects.filter(from_user=request.user2, to_user=from_user).first()
		request_rev.delete()
	frequest.delete()
	return HttpResponseRedirect('/authentication/{}'.format(request.user2.profile.slug))


@login_required
def delete_friend_request(request, id):
	from_user = get_object_or_404(User, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user2).first()
	frequest.delete()
	return HttpResponseRedirect('/authentication/{}'.format(request.user2.profile.slug))


def delete_friend(request, id):
	user_profile = request.user2.profile
	friend_profile = get_object_or_404(Profile, id=id)
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)
	return HttpResponseRedirect('/authentication/{}'.format(friend_profile.slug))


@login_required
def profile_view(request, slug):
	p = Profile.objects.filter(slug=slug).first()
	u = p.user2
	sent_friend_requests = FriendRequest.objects.filter(from_user=p.user2)
	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user2)

	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user2.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user2).filter(to_user=p.user2)) == 1:
				button_status = 'friend_request_sent'

		# if we have recieved a friend request
		if len(FriendRequest.objects.filter(
			from_user=p.user2).filter(to_user=request.user2)) == 1:
				button_status = 'friend_request_received'

	context = {
		'u': u,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
	}

	return render(request, "authentication/profile.html", context)

@login_required
def my_profile(request):
	p = request.user2.profile
	you = p.user2
	sent_friend_requests = FriendRequest.objects.filter(from_user=you)
	rec_friend_requests = FriendRequest.objects.filter(to_user=you)
	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user2.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user2).filter(to_user=you)) == 1:
				button_status = 'friend_request_sent'

		if len(FriendRequest.objects.filter(
			from_user=p.user2).filter(to_user=request.user2)) == 1:
				button_status = 'friend_request_received'

	context = {
		'u': you,
		'button_status': button_status,
		'friends_list': friends,
		'sent_friend_requests': sent_friend_requests,
		'rec_friend_requests': rec_friend_requests,
	}

	return render(request, "authentication/profile.html", context)


@login_required
def search_users(request):
	query = request.GET.get('q')
	object_list = User.objects.filter(username__icontains=query)
	context ={
		'users': object_list
	}
	return render(request, "authentication/search_users.html", context)
