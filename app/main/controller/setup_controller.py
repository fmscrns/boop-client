import os
from flask.helpers import url_for
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import redirect
from app.main.form.user_form import EditUserForm
from app.main.service.circleType_service import CircleTypeService
from app.main.service.businessType_service import BusinessTypeService
from app.main.form.preference_form import CreatePreferenceForm
import json
from app.main.service.breed_service import BreedService
from app.main.service.specie_service import SpecieService
from app.main.form.pet_form import CreatePetForm
from flask import render_template, session
from ... import setup_bp
from ..util.decorator import session_required

@setup_bp.route("/", methods=["GET"])
def setup():
    return render_template("setup.html")

@setup_bp.route("/preference/token=<token>", methods=["GET", "POST"])
@session_required
def preference(current_user, token):
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
    try:
        token = serializer.loads(token, salt="setup_one")
        print("TOKEN : {}".format(token))

    except Exception:
        return redirect(url_for("home.feed"))


    createPreferenceForm = CreatePreferenceForm()
    createPreferenceForm.specie_group_input.choices = [(specie["public_id"], specie["name"]) for specie in json.loads(SpecieService.get_all(session["booped_in"]).text)["data"]]
    createPreferenceForm.business_type_input.choices = [(_type["public_id"], _type["name"]) for _type in json.loads(BusinessTypeService.get_all(session["booped_in"]).text)["data"]]
    createPreferenceForm.circle_type_input.choices = [(_type["public_id"], _type["name"]) for _type in json.loads(CircleTypeService.get_all(session["booped_in"]).text)["data"]]
    return render_template("setup.html",
        page_title = "Setup",
        current_user = current_user,
        createPreferenceForm = createPreferenceForm
    )

@setup_bp.route("/pet", methods=["GET", "POST"])
@session_required
def pet(current_user):
    createPetForm = CreatePetForm()
    createPetForm.group_input.choices = [(specie["public_id"], specie["name"]) for specie in json.loads(SpecieService.get_all(session["booped_in"]).text)["data"]]
    createPetForm.subgroup_input.choices = [(breed["public_id"], breed["name"]) for breed in json.loads(BreedService.get_by_specie(session["booped_in"], createPetForm.group_input.choices[0][0]).text)["data"]]
    return render_template("setup.html",
        page_title = "Setup",
        current_user = current_user,
        createPetForm = createPetForm
    )

@setup_bp.route("/profile", methods=["GET", "POST"])
@session_required
def profile(current_user):
    return render_template("setup.html",
        page_title = "Setup",
        current_user = current_user,
        editUserForm = EditUserForm()
    )