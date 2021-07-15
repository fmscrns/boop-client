from app.main.service.businessType_service import BusinessTypeService
from app.main.service.specie_service import SpecieService
from app.main.service.breed_service import BreedService
from app.main.service.circleType_service import CircleTypeService
import json
from app.main.form.preference_form import CreateBusinessPreferenceForm, CreateCirclePreferenceForm, CreatePetPreferenceForm
from app.main.form.user_form import EditAccountEmailForm, EditAccountUsernameForm, EditAccountPasswordForm
from flask import render_template, session
from ... import settings_bp
from ..util.decorator import session_required

@settings_bp.route("/", methods=["GET", "POST"])
@settings_bp.route("/account", methods=["GET", "POST"])
@settings_bp.route("/account/email", methods=["GET", "POST"])
@session_required
def account_email(current_user):
    editAccountEmailForm = EditAccountEmailForm(prefix="eaef")
    editAccountEmailForm.email_input.data = current_user["email"]
    return render_template("settings.html",
        page_title = "Settings",
        settings_title = "Edit account",
        current_user = current_user,
        editAccountEmailForm = editAccountEmailForm,
        emailActive = "bg-primary text-white"
    )

@settings_bp.route("/account/username", methods=["GET", "POST"])
@session_required
def account_username(current_user):
    editAccountUsernameForm = EditAccountUsernameForm(prefix="eauf")
    editAccountUsernameForm.username_input.data = current_user["username"]
    return render_template("settings.html",
        page_title = "Settings",
        settings_title = "Edit account",
        current_user = current_user,
        editAccountUsernameForm = editAccountUsernameForm,
        usernameActive = "bg-primary text-white"
    )

@settings_bp.route("/account/password", methods=["GET", "POST"])
@session_required
def account_password(current_user):
    return render_template("settings.html",
        page_title = "Settings",
        settings_title = "Edit account",
        current_user = current_user,
        editAccountPasswordForm = EditAccountPasswordForm(prefix="eapf"),
        passwordActive = "bg-primary text-white"
    )

@settings_bp.route("/preferences", methods=["GET", "POST"])
@settings_bp.route("/preferences/pet", methods=["GET", "POST"])
@session_required
def preferences_pet(current_user):
    createPetPreferenceForm = CreatePetPreferenceForm(prefix="cppf")
    specie_list = json.loads(SpecieService.get_all(session["booped_in"]).text)["data"]
    createPetPreferenceForm.specie_group_input.choices = [(specie["public_id"], specie["name"]) for specie in specie_list]
    createPetPreferenceForm.specie_group_input.data = [specie["public_id"] for specie in specie_list if specie["is_preferred"] != 0]
    for specie_pid in createPetPreferenceForm.specie_group_input.data:
        createPetPreferenceForm.breed_subgroup_input.choices += [(breed["public_id"], breed["name"], {"parent-pid" : breed["parent_id"]}) for breed in json.loads(BreedService.get_by_specie(session["booped_in"], specie_pid).text)["data"]]    
    createPetPreferenceForm.breed_subgroup_input.data = [breed["public_id"] for breed in json.loads(BreedService.get_all(session["booped_in"], preferred_only=True).text)["data"]]

    return render_template("settings.html",
        page_title = "Settings",
        settings_title = "Configure preferences",
        current_user = current_user,
        createPetPreferenceForm = createPetPreferenceForm,
        petPrefActive = "bg-primary text-white"
    )

@settings_bp.route("/preferences/business", methods=["GET", "POST"])
@session_required
def preferences_business(current_user):
    createBusinessPreferenceForm = CreateBusinessPreferenceForm(prefix="cbpf")
    businessType_list = json.loads(BusinessTypeService.get_all(session["booped_in"]).text)["data"]
    createBusinessPreferenceForm.business_type_input.choices = [(_type["public_id"], _type["name"], {}) for _type in businessType_list]
    createBusinessPreferenceForm.business_type_input.data = [_type["public_id"] for _type in businessType_list if _type["is_preferred"] != 0]
    return render_template("settings.html",
        page_title = "Settings",
        settings_title = "Configure preferences",
        current_user = current_user,
        createBusinessPreferenceForm = createBusinessPreferenceForm,
        businessPrefActive = "bg-primary text-white"
    )

@settings_bp.route("/preferences/circle", methods=["GET", "POST"])
@session_required
def preferences_circle(current_user):
    createCirclePreferenceForm = CreateCirclePreferenceForm(prefix="ccpf")
    circleType_list = json.loads(CircleTypeService.get_all(session["booped_in"]).text)["data"]
    createCirclePreferenceForm.circle_type_input.choices = [(_type["public_id"], _type["name"], {}) for _type in circleType_list]
    createCirclePreferenceForm.circle_type_input.data = [_type["public_id"] for _type in circleType_list if _type["is_preferred"] != 0]
    
    return render_template("settings.html",
        page_title = "Settings",
        settings_title = "Configure preferences",
        current_user = current_user,
        createCirclePreferenceForm = createCirclePreferenceForm,
        circlePrefActive = "bg-primary text-white"
    )