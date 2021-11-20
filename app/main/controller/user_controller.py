import json
import os
from flask import render_template, flash, redirect, url_for, abort, jsonify, session, request
from itsdangerous import URLSafeTimedSerializer
from ... import user_bp
from ..service.user_service import UserService
from ..util.decorator import session_required
from ..form.user_form import EditAccountPasswordForm, EditAccountUsernameForm, EditProfileForm, EditPhotoForm, EditAccountEmailForm
from ..form.pet_form import CreatePetForm, FollowPetForm, UnfollowPetForm
from ..form.business_form import CreateBusinessForm, FollowBusinessForm, UnfollowBusinessForm
from ..service.specie_service import SpecieService
from ..service.breed_service import BreedService
from ..service.pet_service import PetService
from ..service.post_service import PostService
from ..service.business_service import BusinessService
from ..form.user_form import CreateUserTwoForm
from ..form.post_form import CreatePostForm, DeletePostForm
from ..service.businessType_service import BusinessTypeService
from ..form.circle_form import CreateCircleForm
from ..service.circleType_service import CircleTypeService
from ..service.circle_service import CircleService

@user_bp.route("/<username>/pets", methods=["GET", "POST"])
@user_bp.route("/<username>", methods=["GET", "POST"])
@session_required
def pets(current_user, username):
    get_resp = UserService.get_by_username(username)
    if get_resp.ok:
        editProfileForm = EditProfileForm(prefix="euf")
        editProfileForm.name_input.data = current_user["name"]
        createPetForm = CreatePetForm()
        createPetForm.group_input.choices = [(specie["public_id"], specie["name"]) for specie in json.loads(SpecieService.get_all(session["booped_in"]).text)["data"]]
        createPetForm.subgroup_input.choices = [(breed["public_id"], breed["name"]) for breed in json.loads(BreedService.get_by_specie(session["booped_in"], createPetForm.group_input.choices[0][0]).text)["data"]]
        this_user = json.loads(get_resp.text)
        return render_template("user_profile.html",
            page_title = "Profile",
            current_user = current_user,
            this_user = this_user,
            editProfileForm = editProfileForm if this_user["public_id"] == current_user["public_id"] else None,
            editPhotoForm = EditPhotoForm(prefix="epf") if this_user["public_id"] == current_user["public_id"] else None,
            editAccountEmailForm = EditAccountEmailForm(prefix="eaf") if this_user["public_id"] == current_user["public_id"] else None,
            createPetForm = createPetForm,
            followPetForm = FollowPetForm(),
            unfollowPetForm = UnfollowPetForm(),
            pet_list = json.loads(PetService.get_all_by_user(session["booped_in"], this_user["public_id"]).text)["data"]
        )
    else:
        abort(404)

@user_bp.route("/<username>/posts", methods=["GET", "POST"])
@session_required
def posts(current_user, username):
    if current_user["username"] == username:
        editProfileForm = EditProfileForm(prefix="euf")
        editProfileForm.name_input.data = current_user["name"]
        createPostForm = CreatePostForm()
        createPostForm.subject_input.choices = [(subject["public_id"], subject["name"]) for subject in json.loads(PetService.get_all_by_user(session["booped_in"], current_user["public_id"] + "?tag_suggestions=1").text)["data"]]
        return render_template("user_profile.html",
            page_title = "Profile",
            current_user = current_user,
            this_user = current_user,
            editProfileForm = editProfileForm,
            editPhotoForm = EditPhotoForm(prefix="epf"),
            editAccountEmailForm = EditAccountEmailForm(prefix="eaf"),
            createPostForm = createPostForm,
            deletePostForm = DeletePostForm(prefix="dptf")
        )
    else:
        abort(403)

@user_bp.route("/<username>/businesses", methods=["GET", "POST"])
@session_required
def businesses(current_user, username):
    if current_user["username"] == username:
        editProfileForm = EditProfileForm(prefix="euf")
        editProfileForm.name_input.data = current_user["name"]
        createBusinessForm = CreateBusinessForm()
        createBusinessForm.type_input.choices = [(_type["public_id"], _type["name"]) for _type in json.loads(BusinessTypeService.get_all(session["booped_in"]).text)["data"]]
        return render_template("user_profile.html",
            page_title = "Profile",
            current_user = current_user,
            this_user = current_user,
            editProfileForm = editProfileForm,
            editPhotoForm = EditPhotoForm(prefix="epf"),
            editAccountEmailForm = EditAccountEmailForm(prefix="eaf"),
            createBusinessForm = createBusinessForm,
            followBusinessForm = FollowBusinessForm(),
            unfollowPetForm = UnfollowBusinessForm(),
            business_list = json.loads(BusinessService.get_all_by_user(session["booped_in"], current_user["public_id"]).text)["data"]
        )
    else:
        abort(403)

@user_bp.route("/<username>/circles", methods=["GET", "POST"])
@session_required
def circles(current_user, username):
    if current_user["username"] == username:
        editProfileForm = EditProfileForm(prefix="euf")
        editProfileForm.name_input.data = current_user["name"]
        createCircleForm = CreateCircleForm()
        createCircleForm.type_input.choices = [(_type["public_id"], _type["name"]) for _type in json.loads(CircleTypeService.get_all(session["booped_in"]).text)["data"]]
        return render_template("user_profile.html",
            page_title = "Profile",
            current_user = current_user,
            this_user = current_user,
            editProfileForm = editProfileForm,
            editPhotoForm = EditPhotoForm(prefix="epf"),
            editAccountEmailForm = EditAccountEmailForm(prefix="eaf"),
            createCircleForm = createCircleForm,
            circle_list = json.loads(CircleService.get_all_by_user(session["booped_in"], current_user["public_id"]).text)["data"]
        )
    else:
        abort(403)

@user_bp.route("/", methods=["GET"])
@session_required
def search(current_user):
    list = json.loads(
        UserService.search(
            request.args.get("value"),
            request.args.get("same_followed_pets"),
            request.args.get("same_breed_preferences"),
            request.args.get("pagination_no")
        ).text
    )
    if list.get("data"):
        return jsonify(
            dict(
                People = list["data"]
            )
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

@user_bp.route("/<user_pid>/edit/profile", methods=["POST"])
@session_required
def edit_profile(current_user, user_pid):
    editProfileForm = EditProfileForm(prefix="euf")

    if editProfileForm.validate_on_submit():
        edit_user = UserService.edit_profile(user_pid, session["booped_in"], request.form)

        if edit_user.ok:
            resp = json.loads(edit_user.text)
            flash(resp["message"], "success")

            return redirect(url_for("user.pets", username=current_user["username"]))
        
        flash(json.loads(edit_user.text)["message"], "danger")
    
    if editProfileForm.errors:
        for key in editProfileForm.errors:
            for message in editProfileForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("user.pets", username=current_user["username"]))

@user_bp.route("/<user_pid>/edit/photo", methods=["POST"])
@session_required
def edit_photo(current_user, user_pid):
    editPhotoForm = EditPhotoForm(prefix="epf")

    if editPhotoForm.validate_on_submit():
        edit_user = UserService.edit_photo(user_pid, session["booped_in"], request.files)

        if edit_user.ok:
            resp = json.loads(edit_user.text)
            flash(resp["message"], "success")

            return redirect(url_for("user.pets", username=current_user["username"]))
        
        flash(json.loads(edit_user.text)["message"], "danger")
    
    if editPhotoForm.errors:
        for key in editPhotoForm.errors:
            for message in editPhotoForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("user.pets", username=current_user["username"]))

@user_bp.route("/<user_pid>/edit/account/email", methods=["POST"])
@session_required
def edit_account_email(current_user, user_pid):
    editAccountEmailForm = EditAccountEmailForm(prefix="eaef")

    if editAccountEmailForm.validate_on_submit():
        edit_user = UserService.edit_account(user_pid, session["booped_in"], request.form)

        if edit_user.ok:
            resp = json.loads(edit_user.text)
            flash(resp["message"], "success")

            return redirect(url_for("settings.account_email"))
        
        flash(json.loads(edit_user.text)["message"], "danger")
    
    if editAccountEmailForm.errors:
        for key in editAccountEmailForm.errors:
            for message in editAccountEmailForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("settings.account_email"))

@user_bp.route("/<user_pid>/edit/account/username", methods=["POST"])
@session_required
def edit_account_username(current_user, user_pid):
    editAccountUsernameForm = EditAccountUsernameForm(prefix="eauf")

    if editAccountUsernameForm.validate_on_submit():
        edit_user = UserService.edit_account(user_pid, session["booped_in"], request.form)

        if edit_user.ok:
            resp = json.loads(edit_user.text)
            flash(resp["message"], "success")

            return redirect(url_for("settings.account_username"))
        
        flash(json.loads(edit_user.text)["message"], "danger")
    
    if editAccountUsernameForm.errors:
        for key in editAccountUsernameForm.errors:
            for message in editAccountUsernameForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("settings.account_username"))

@user_bp.route("/<user_pid>/edit/account/password", methods=["POST"])
@session_required
def edit_account_password(current_user, user_pid):
    editAccountPasswordForm = EditAccountPasswordForm(prefix="eapf")

    if editAccountPasswordForm.validate_on_submit():
        edit_user = UserService.edit_account(user_pid, session["booped_in"], request.form)

        if edit_user.ok:
            resp = json.loads(edit_user.text)
            flash(resp["message"], "success")

            return redirect(url_for("settings.account_password"))
        
        flash(json.loads(edit_user.text)["message"], "danger")
    
    if editAccountPasswordForm.errors:
        for key in editAccountPasswordForm.errors:
            for message in editAccountPasswordForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("settings.account_password"))