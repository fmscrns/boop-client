import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import user_bp
from ..service.user_service import UserService
from ..util.decorator import session_required
from ..form.user_form import EditUserForm
from ..form.pet_form import CreatePetForm
from ..form.business_form import CreateBusinessForm
from ..service.specie_service import SpecieService
from ..service.breed_service import BreedService
from ..service.pet_service import PetService
from ..service.post_service import PostService
from ..service.business_service import BusinessService
from ..form.user_form import CreateUserTwoForm
from ..form.post_form import CreatePostForm
from ..service.businessType_service import BusinessTypeService

@user_bp.route("/<username>", methods=["GET", "POST"])
@user_bp.route("/<username>/pets", methods=["GET", "POST"])
@session_required
def pets(current_user, username):
    get_resp = UserService.get_by_username(username)
    if get_resp.ok:
        editUserForm = EditUserForm(prefix="euf")
        editUserForm.name_input.data = current_user["name"]
        editUserForm.username_input.data = current_user["username"]
        editUserForm.email_input.data = current_user["email"]
        createPetForm = CreatePetForm()
        createPetForm.group_input.choices = [(specie["public_id"], specie["name"]) for specie in json.loads(SpecieService.get_all(session["booped_in"]).text)["data"]]
        createPetForm.subgroup_input.choices = [(breed["public_id"], breed["name"]) for breed in json.loads(BreedService.get_by_specie(session["booped_in"], createPetForm.group_input.choices[0][0]).text)["data"]]

        this_user = json.loads(get_resp.text)
        return render_template("user_profile.html",
            page_title = "Profile",
            current_user = current_user,
            this_user = this_user,
            editUserForm = editUserForm,
            createPetForm = createPetForm,
            pet_list = json.loads(PetService.get_all_by_user(session["booped_in"], this_user["public_id"]).text)["data"]
        )
    else:
        abort(404)

@user_bp.route("/<username>", methods=["GET", "POST"])
@user_bp.route("/<username>/posts", methods=["GET", "POST"])
@session_required
def posts(current_user, username):
    get_resp = UserService.get_by_username(username)
    if get_resp.ok:
        editUserForm = EditUserForm(prefix="euf")
        editUserForm.name_input.data = current_user["name"]
        editUserForm.username_input.data = current_user["username"]
        editUserForm.email_input.data = current_user["email"]
        createPostForm = CreatePostForm()
        this_user = json.loads(get_resp.text)
        return render_template("user_profile.html",
            page_title = "Profile",
            current_user = current_user,
            this_user = this_user,
            editUserForm = editUserForm,
            createPostForm = createPostForm,
            post_list = json.loads(PostService.get_all_by_user(session["booped_in"], this_user["public_id"]).text)["data"]
        )
    else:
        abort(404)

@user_bp.route("/<username>", methods=["GET", "POST"])
@user_bp.route("/<username>/businesses", methods=["GET", "POST"])
@session_required
def businesses(current_user, username):
    get_resp = UserService.get_by_username(username)
    if get_resp.ok:
        editUserForm = EditUserForm(prefix="euf")
        editUserForm.name_input.data = current_user["name"]
        editUserForm.username_input.data = current_user["username"]
        editUserForm.email_input.data = current_user["email"]
        
        createBusinessForm = CreateBusinessForm()
        createBusinessForm.type_input.choices = [(_type["public_id"], _type["name"]) for _type in json.loads(BusinessTypeService.get_all(session["booped_in"]).text)["data"]]
        this_user = json.loads(get_resp.text)

        return render_template("user_profile.html",
            page_title = "Profile",
            current_user = current_user,
            this_user = this_user,
            editUserForm = editUserForm,
            createBusinessForm = createBusinessForm,
            business_list = json.loads(BusinessService.get_all_by_user(session["booped_in"], this_user["public_id"]).text)["data"]
        )
    else:
        abort(404)

@user_bp.route("/create", methods=["POST"])
def create():
    createUserTwoForm = CreateUserTwoForm()
    createUserTwoForm.confirm_password_input.data = createUserTwoForm.password_input.data
    if createUserTwoForm.validate_on_submit():
        api_resp = UserService.create(request.form)

        if api_resp.ok:
            session["booped_in"] = json.loads(api_resp.text)["Authorization"]

            flash(json.loads(api_resp.text)["message"], "success")
            return redirect(url_for("home.feed"))

        flash(json.loads(api_resp.text)["message"], "danger")
        return redirect(url_for("gateway.signup_one"))

    flash("Please try again.", "danger")
    return redirect(url_for("gateway.signup_one"))

@user_bp.route("/<user_pid>/edit", methods=["POST"])
@session_required
def edit(current_user, pid):
    editUserForm = EditUserForm(prefix="euf")

    if editUserForm.validate_on_submit():
        edit_user = UserService.edit(pid, session["booped_in"], request.form, request.files)

        if edit_user.ok:
            resp = json.loads(edit_user.text)
            flash(resp["message"], "success")

            return redirect(url_for("user.pets", username=resp["payload"]))
        
        flash(json.loads(edit_user.text)["message"], "danger")
    
    if editUserForm.errors:
        for key in editUserForm.errors:
            for message in editUserForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("user.pets", username=current_user["username"]))