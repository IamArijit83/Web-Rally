from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserActivity


def landing(request):
    print("👋 Landing page called")

    if request.user.is_authenticated:
        print("🔁 Redirecting to home because user is authenticated")
        return redirect('home')
    
    print("✅ Rendering landing.html")
    return render(request, 'tracker/landing.html')





# ✅ Home page view - handles form and saves to DB
@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        transport = request.POST.get('transport')
        meal = request.POST.get('meal')
        energy = request.POST.get('energy')
        meat_amount = request.POST.get('meat_amount')

        score = 0
        suggestions = []

        # 🚗 Transport scoring
        if transport in ['car', 'cab']:
            score += 50
            suggestions.append("Try using public transport or carpooling when possible.")
        elif transport in ['bus', 'auto']:
            score += 20
            suggestions.append("Biking or walking short distances can lower your footprint.")
        elif transport in ['bike', 'rickshaw', 'erickshaw']:
            score += 10
        elif transport in ['bicycle', 'walk']:
            score += 0
        elif transport == 'electric_vehicle':
            score += 5

        # 🍱 Meal scoring
        if meal == 'meat':
            score += 40
            suggestions.append("Reducing meat consumption can significantly cut emissions.")
            if meat_amount:
                try:
                    score += int(meat_amount) * 0.1
                except ValueError:
                    pass
        elif meal == 'vegetarian':
            score += 20
            suggestions.append("Switching to plant-based meals occasionally helps too.")
        elif meal == 'vegan':
            score += 10
            suggestions.append("You're already making a big impact by going vegan!")

        # ❄️ Energy usage
        if energy:
            try:
                score += int(energy) * 5
                if int(energy) > 2:
                    suggestions.append("Reducing AC or heater usage can save energy.")
            except ValueError:
                pass

        # ✅ Save to DB INSIDE the view function
        UserActivity.objects.create(
            user=request.user,
            transport=transport,
            meal=meal,
            meat_amount=int(meat_amount) if meat_amount else None,
            energy=int(energy) if energy else 0,
            carbon_score=score
        )

        # 💾 Store in session
        request.session['user_data'] = {
            'username': request.user.username,
            'transport': transport,
            'meal': meal,
            'meat_amount': meat_amount,
            'energy': energy,
            'carbon_score': int(score),
            'suggestions': suggestions
        }

        return redirect('user_details')

    return render(request, 'tracker/home.html', {'user': request.user})


# ✅ Results summary
@login_required(login_url='login')
def user_details(request):
    data = request.session.get('user_data', None)
    if not data:
        messages.error(request, "No data available. Please submit the form first.")
        return redirect('home')
    return render(request, 'tracker/user_details.html', data)


# ✅ Signup
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please try a different one.")
            return render(request, 'tracker/signup.html')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, 'tracker/signup.html')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, "Account created successfully! You are now logged in.")
        return redirect('home')

    return render(request, 'tracker/signup.html')


# ✅ Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'tracker/login.html')

    return render(request, 'tracker/login.html')


# ✅ Logout
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')



@login_required
def history_view(request):
    activities = UserActivity.objects.filter(user=request.user).order_by('-submitted_at')
    return render(request, 'tracker/history.html', {'activities': activities})


@login_required
def analytics_view(request):
    activities = UserActivity.objects.filter(user=request.user).order_by('submitted_at')
    dates = [a.submitted_at.strftime("%Y-%m-%d") for a in activities]
    scores = [a.carbon_score for a in activities]
    return render(request, 'tracker/analytics.html', {
        'dates': dates,
        'scores': scores
    })

from .models import Feedback

@login_required
def feedback_view(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        rating = int(request.POST.get('rating', 5))
        Feedback.objects.create(user=request.user, comment=comment, rating=rating)
        return render(request, 'tracker/feedback.html', {'message': 'Thanks for your feedback!'})
    return render(request, 'tracker/feedback.html')
