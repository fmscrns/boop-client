from app.main.form.pet_form import FollowPetForm
from app.main.service.circle_service import CircleService
from app.main.service.business_service import BusinessService
from flask import render_template
from ... import home_bp
from ..util.decorator import session_required
from ..service.pet_service import PetService
from ..service.user_service import *
from ..form.post_form import CreatePostForm, DeletePostForm
import json
from dateutil import parser

@home_bp.route("/feed", methods=["GET", "POST"])
@session_required
def feed(current_user):
    print(current_app.url_map)
    createPostForm = CreatePostForm()
    createPostForm.subject_input.choices = [(subject["public_id"], subject["name"]) for subject in json.loads(PetService.get_all_by_user(session["booped_in"], current_user["public_id"] + "?tag_suggestions=1").text)["data"]]
    return render_template("feed.html",
        page_title = "Feed",
        current_user = current_user,
        createPostForm = createPostForm,
        deletePostForm = DeletePostForm(prefix="dptf"),
        followPetForm = FollowPetForm()
        # pet_suggestion_list = json.loads(PetService.get_by_preference(1).text)["data"],
        # business_sugestion_list = json.loads(BusinessService.get_by_preference(1).text)["data"],
        # circle_sugestion_list = json.loads(CircleService.get_by_preference(1).text)["data"]
    )