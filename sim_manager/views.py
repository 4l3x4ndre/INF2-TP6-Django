from django.shortcuts import render, get_object_or_404, redirect
from django.forms.models import model_to_dict

from .models import Simulation, MyUser
from .forms import UserProfileForm, SimuForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from pyfhn.fhn_runner import run_fhn_base
import matplotlib.pyplot as plt
from io import StringIO

from django.views.decorators.http import require_http_methods


# Create your views here.
def landing(request):
    return render(request, "base.html", locals())


@login_required(login_url="/account/login/")
def simulation_list(request):
    simulations = Simulation.objects.filter(user=request.user)

    return render(request, "simulation_list.html", {"user_sims": simulations, })


@login_required(login_url="/account/login/")
def edit_profile(request):
    envoi = False
    if request.method == "POST":
        user_profile_form = UserProfileForm(request.POST)
        if user_profile_form.is_valid() and user_profile_form.cleaned_data["email"]:
            current_user = User.objects.get(username=request.user.username)
            current_user.first_name = user_profile_form.cleaned_data["first_name"]
            current_user.last_name = user_profile_form.cleaned_data["last_name"]
            current_user.email = user_profile_form.cleaned_data["email"]
            current_user.save()
    else:
        user_profile_form = UserProfileForm(instance=request.user)
    return render(request, "edit_profile.html", {"form": user_profile_form})


@login_required(login_url="/account/login/")
def new_simu(request):
    # Construire le formulaire, soit avec les données postées,
    # soit vide si l'utilisateur accède pour la première fois
    # à la page.
    form = SimuForm(request.POST, request.FILES)
    if form.is_valid():

        params = form.cleaned_data
        print(params)
        newsim = Simulation(
            user=params["user"],
            alpha=params["alpha"],
            beta=params["beta"],
            gamma=params["gamma"],
            delta=params["delta"],
            epsilon=params["epsilon"],
        )
        newsim.save()
        return run_sim(request, newsim.id)
    return render(request, "newsimu.html", locals())


def run_sim(request, object_id):
    params = model_to_dict(get_object_or_404(Simulation, pk=object_id))
    params.pop("user")
    params.pop("id")
    res = run_fhn_base(params)
    f = plt.figure()
    plt.title("FHN Simulation")
    plt.xlabel("Time")
    plt.ylabel("Outputs")
    plot = plt.plot(res["t"], res["y"][0], res["t"], res["y"][1])
    plt.legend(["v", "w"])
    imgdata = StringIO()
    f.savefig(imgdata, format="svg")
    imgdata.seek(0)

    data = imgdata.getvalue()
    return render(request, "graphic.html", {"graphic": data})


@login_required(login_url="/login/")
def simulation_delete(request, object_id):
    sim = get_object_or_404(Simulation, pk=object_id)
    sim.delete()
    return HttpResponseRedirect(reverse_lazy("sim_list"))


def creer_utilisateur(req):
    error = ''
    if req.method == 'POST':
        user_creation_form = UserCreationForm(req.POST)

        # L'unicité de l'utilisateur est déjà vérifiée dans le model User
        if user_creation_form.is_valid():
            new_user = user_creation_form.save(commit=False)
            new_user.set_password(new_user.password)
            new_user.is_staff=True
            new_user.save()

            mygroup = Group.objects.get(name="default")
            mygroup.user_set.add(new_user)
            return redirect('user_info')
        else:
            error = 'Failed. Retry with different values.'
    else:
        user_creation_form = UserCreationForm()

    return render(req, 'creer_utilisateur.html', {'form': user_creation_form, 'error': error})


@require_http_methods(['GET'])
def user_info(req):
    users = User.objects.all()
    return render(req, 'user_info.html', {'users': users})


def logout_view(request):
    logout(request)
    return redirect('/')


@require_http_methods(['GET', 'POST'])
@login_required(login_url="/account/login/")
def login_view(req):
    """
    Fonction pour changer de mot de passe
    :param req: HTTPRequest
    :return:
    """
    if req.method=='POST':
        passw = MyUser(req.POST)
        current_user = User.objects.get(username=req.user.username)
        current_user.set_password(req.POST.get("password"))
        current_user.save()
        logout(req)
        return redirect('/')
    else:
        passw = MyUser()

    return render(req, 'edit_password.html', {'form': passw})
