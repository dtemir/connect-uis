from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Profile, Post, UpvotePost, Follow

from .email_verification import send_verification, check_verification

@login_required(login_url="signin")
def index(request):
    """
    Display the landing page
    * show all posts made
    """
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)

    posts = Post.objects.all()
    user_profiles = Profile.objects.all()

    return render(request, "index.html", {"user_profile": user_profile, "posts": posts, "user_profiles": user_profiles})


@login_required(login_url="signin")
def settings(request):
    """
    Displays the settings page
    * change picture
    * change bio
    * change location
    """
    user_profile = Profile.objects.get(user=request.user)
    user = User.objects.get(username=request.user.username)

    if request.method == "POST":

        # update profile image if given
        user_profile.profileimg = (
            request.FILES.get("image")
            if request.FILES.get("image") is not None
            else user_profile.profileimg
        )

        # update user first and last name
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]


        # update profile bio and location
        user_profile.bio = request.POST["bio"]
        user_profile.location = request.POST["location"]

        user_profile.save()
        user.save()

    return render(request, "settings.html", {"user_profile": user_profile, "user": user, "bio": user_profile.bio, "location": user_profile.location})


@login_required(login_url="signin")
def upload(request):
    """
    Posts a post
    * Upload a picture
    * Provide caption
    """
    if request.method == "POST":
        image = request.FILES.get("image")
        title = request.POST["title"]
        caption = request.POST["caption"]

        profile = Profile.objects.get(
            user=User.objects.get(username=request.user.username)
        )
        post = Post.objects.create(profile=profile, image=image, title=title, caption=caption)
        post.save()

        return redirect("/")
    else:
        return redirect("/")


@login_required(login_url="signin")
def upvote(request):
    """
    Upvotes a post
    * Increase upvote counter
    * Decrease upvote counter
    """
    profile = Profile.objects.get(
            user=User.objects.get(username=request.user.username)
        )
    post_id = request.GET.get("post_id")

    post = Post.objects.get(post_id=post_id)

    # Check if the current user has already upvoted the post before
    upvote_filter = UpvotePost.objects.filter(post=post, profile=profile).first()

    # The user didn't upvote the post before
    if upvote_filter == None:
        # Create a new upvote
        upvote = UpvotePost.objects.create(post=post, profile=profile)
        upvote.save()

        # Register an upvote
        post.upvotes += 1
        post.save()

        return redirect("/")

    # The user upvoted the post before, remove upvote
    else:
        # Delete the upvote
        upvote_filter.delete()

        # Decrement the number of upvotes on the post
        post.upvotes -= 1
        post.save()

        return redirect("/")


@login_required(login_url="signin")
def follow(request):
    """
    Follows other users
    * Create a Follow object between
    current user and someone else's profile
    """
    if request.method == "POST":
        follower = request.POST["follower"]
        followed = request.POST["followed"]

        # Find whether there is a following between the follower and the followed
        follower_filter = Follow.objects.filter(
            follower=follower, followed=followed
        ).first()

        # The current user is not following the user yet
        if follower_filter == None:
            new_follower = Follow.objects.create(follower=follower, followed=followed)
            new_follower.save()
            return redirect("/profile/" + str(followed))
        # The current user is already following the user
        else:
            follower_filter.delete()
            return redirect("/profile/" + str(followed))
    else:
        return redirect("/")


@login_required(login_url="signin")
def profile(request, pk):
    """
    Shows profile
    * Show all posts made by user
    * Show number of posts
    * Show number of followers
    * Show number of followed
    """
    # User who is currently viewing the profile page
    user = request.user
    # Current profile whose page is being viewed
    profile = Profile.objects.get(user=User.objects.get(username=pk))

    # Get all posts posted by the profile user
    user_posts = Post.objects.filter(profile=profile)

    button_text = "Follow"
    if Follow.objects.filter(follower=user, followed=profile).first():
        button_text = "Unfollow"

    followers = len(Follow.objects.filter(followed=pk))
    following = len(Follow.objects.filter(follower=pk))

    context = {
        "user": user,
        "user_profile": profile,
        "user_posts": user_posts,
        "user_num_posts": len(user_posts),
        "button_text": button_text,
        "user_followers": followers,
        "user_following": following,
    }

    return render(request, "profile.html", context)


def verify(request):
    """
    Verify that the UIS email provided is working
    by sending a Twillio & SendGrid API verification code
    """
    print(request.POST)
    if "code" in request.POST:
        code = request.POST["code"]
        decision = check_verification(code)
        print(decision)
    else:
        email = request.POST["email"]
        send_verification(email)
        return redirect("verify")

data = {}   
def signup(request):
    """
    Allows the user to sign up to use the site
    * Provide first name, last name, username, email, password
    """

    if request.method == "POST":

        if "first_name" in request.POST:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            password2 = request.POST["password2"]

            if password == password2:
                # Email was already used to register
                if User.objects.filter(email=email).exists():
                    messages.info(request, "Email taken")
                    return redirect("signup")
                # Username was already used to register
                elif User.objects.filter(username=username).exists():
                    messages.info(request, "Username taken")
                    return redirect("signup")
                else:
                    data["first_name"] = first_name
                    data["last_name"] = last_name
                    data["username"] = username
                    data["email"] = email
                    data["password"] = password

                    send_verification(email)
                    return render(request, "verify.html")
            else:
                messages.info(request, "Passwords don't match")
                return redirect("signup")
        
        elif "code" in request.POST:
            code = request.POST["code"]
            decision = check_verification(data["email"], code)

            if decision:
                user = User.objects.create_user(
                    username=data["username"], email=data["email"], password=data["password"], first_name=data["first_name"], last_name=data["last_name"]
                )
                user.save()
                # Log in the user and setting to settings
                user_login = auth.authenticate(username=data["username"], password=data["password"])
                auth.login(request, user_login)

                # Create a Profile object
                profile = Profile.objects.create(user=user)
                profile.save()

                return redirect("/")
            else:
                return render(request, "verify.html")

    else:
        return render(request, "signup.html")


def signin(request):
    """
    Allow the user to sign in to the site
    * Proivde username and password
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        # User authenticated
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        # User is not authenticated
        else:
            messages.info(request, "Credentials Invalid")
            return redirect("signin")
    else:
        return render(request, "signin.html")


@login_required(login_url="signin")
def logout(request):
    """
    Logs out the user
    """
    auth.logout(request)
    return redirect("signin")
