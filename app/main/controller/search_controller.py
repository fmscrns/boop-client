from app.main.service.specie_service import SpecieService
import json
from app.main.form.search_form import SearchPeopleForm, SearchPetForm
from flask import render_template, abort
from flask.globals import request, session
from flask.helpers import url_for
from ... import search_bp
from ..util.decorator import session_required

@search_bp.route("/all", methods=["GET", "POST"])
@session_required
def all(current_user):
    search_value = request.args.get("value")

    if search_value:
        return render_template("search.html",
            page_title = "Search",
            current_user = current_user,
            allActive = "bg-primary text-white",
            search_value = search_value,
            pets_url = url_for("pet.search"),
            people_url = url_for("user.search")
        )
    else:
        abort(404)

@search_bp.route("/pets", methods=["GET", "POST"])
@session_required
def pets(current_user):
    search_value = request.args.get("value")
    searchPetForm = SearchPetForm(prefix="spf")
    searchPetForm.group_input.choices = [(0, "All", {"param-str": ""})] + [(specie["public_id"], specie["name"], {"param-str": "&group_id=" + specie["public_id"]}) for specie in json.loads(SpecieService.get_all(session["booped_in"]).text)["data"]]
    if search_value:
        return render_template("search.html",
            page_title = "Search",
            current_user = current_user,
            petsActive = "bg-primary text-white",
            search_value = search_value,
            pets_url = url_for("pet.search"),
            people_url = "",
            searchPetForm = searchPetForm
        )
    else:
        abort(404)

@search_bp.route("/people", methods=["GET", "POST"])
@session_required
def people(current_user):
    search_value = request.args.get("value")
    searchPeopleForm = SearchPeopleForm(prefix="spplf")
    if search_value:
        return render_template("search.html",
            page_title = "Search",
            current_user = current_user,
            peopleActive = "bg-primary text-white",
            search_value = search_value,
            pets_url = "",
            people_url = url_for("user.search"),
            searchPeopleForm = searchPeopleForm
        )
    else:
        abort(404)

# @search_bp.route("/posts", methods=["GET", "POST"])
# @session_required
# def posts(current_user):
#     return render_template("search.html",
#         page_title = "Search",
#         current_user = current_user,
#         postsActive = "bg-primary text-white"
#     )

# @search_bp.route("/businesses", methods=["GET", "POST"])
# @session_required
# def businesses(current_user):
#     return render_template("search.html",
#         page_title = "Search",
#         current_user = current_user,
#         businessesActive = "bg-primary text-white"
#     )

# @search_bp.route("/circles", methods=["GET", "POST"])
# @session_required
# def circles(current_user):
#     return render_template("search.html",
#         page_title = "Search",
#         current_user = current_user,
#         circlesActive = "bg-primary text-white"
#     )