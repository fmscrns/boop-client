from flask import Flask, render_template, abort
from ... import home_bp
from ..util.decorator import session_required
from ..service.pet_service import PetService
from ..service.post_service import  PostService
from ..service.user_service import *
from ..form.post_form import CreatePostForm, DeletePostForm
import json
from dateutil import parser


@home_bp.route("/feed", methods=["GET", "POST"])
@session_required
def feed(current_user):
    all_post_request = PostService.get_all_posts()
    createPostForm = CreatePostForm()
    createPostForm.subject_input.choices = [(subject["public_id"], subject["name"]) for subject in json.loads(PetService.get_all_by_user(session["booped_in"], current_user["public_id"] + "?tag_suggestions=1").text)["data"]]
    if all_post_request.ok:
        return render_template("feed.html",
            page_title = "Feed",
            current_user = current_user,
            createPostForm = createPostForm,
            deletePostForm = DeletePostForm(prefix="dptf"),
            all_Posts = json.loads(all_post_request.text)["data"]
        )
    else:
        abort(404)
    