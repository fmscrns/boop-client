import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import pet_bp
from ..service.user_service import UserService
from ..util.decorator import session_required
from ..form.pet_form import AcceptPetForm, CreatePetForm, EditPetForm, DeletePetForm, FollowPetForm, UnfollowPetForm
from ..service.pet_service import PetService
from ..service.breed_service import BreedService
from ..service.pet_service import PetService
from dateutil import parser

@pet_bp.route("/<pet_pid>", methods=["GET", "POST"])
@pet_bp.route("/<pet_pid>/posts", methods=["GET", "POST"])
@session_required
def posts(current_user, pet_pid):
    get_resp = PetService.get_by_pid(pet_pid)
    if get_resp.ok:
        this_pet = json.loads(get_resp.text)
        this_pet["birthday"] = parser.parse(this_pet["birthday"])
        
        return render_template("pet_profile.html",
            page_title = "Pet profile",
            current_user = current_user,
            this_pet = this_pet,
            editPetForm = EditPetForm(prefix="epf"),
            deletePetForm = DeletePetForm(),
            followPetForm = FollowPetForm(),
            unfollowPetForm = UnfollowPetForm()
        )
    else:
        abort(404)

@pet_bp.route("/create", methods=["POST"])
@session_required
def create(current_user):
    createPetForm = CreatePetForm()

    createPetForm.group_input.choices = [(request.form.get("group_input"), "")]
    createPetForm.subgroup_input.choices = [(request.form.get("subgroup_input"), "")]

    if createPetForm.validate_on_submit():
        create_pet = PetService.create(request.form, request.files)

        if create_pet.ok:
            resp = json.loads(create_pet.text)
            flash(resp["message"], "success")

            return redirect(url_for("user.pets", username=resp["payload"]))
        
        flash(json.loads(create_pet.text), "danger")
    
    if createPetForm.errors:
        for key in createPetForm.errors:
            for message in createPetForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("user.pets", username=current_user["username"]))

@pet_bp.route("/<pet_pid>/edit", methods=["POST"])
@session_required
def edit(current_user, pet_pid):
    editPetForm = EditPetForm(prefix="epf")

    if editPetForm.validate_on_submit():
        edit_pet = PetService.edit(pet_pid, session["booped_in"], request.form, request.files)

        if edit_pet.ok:
            resp = json.loads(edit_pet.text)
            flash(resp["message"], "success")

            return redirect(url_for("pet.posts", pet_pid=pet_pid))
        
        flash(json.loads(edit_pet.text)["message"], "danger")
    
    if editPetForm.errors:
        for key in editPetForm.errors:
            for message in editPetForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("pet.posts", pet_pid=pet_pid))

@pet_bp.route("/<pet_pid>/delete", methods=["POST"])
@session_required
def delete(current_user, pet_pid):
    deletePetForm = DeletePetForm()
    owner_username = json.loads(PetService.get_by_pid(pet_pid).text)["owner_username"]
    if deletePetForm.validate_on_submit():
        delete_pet = PetService.delete(pet_pid, request.form)

        if delete_pet.ok:
            flash(json.loads(delete_pet.text)["message"], "success")

            return redirect(url_for("user.pets", username=owner_username))
        
        flash(json.loads(delete_pet.text), "danger")

    if deletePetForm.errors:
        for key in deletePetForm.errors:
            for message in deletePetForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("pet.posts", pet_pid=pet_pid))

@pet_bp.route("/<pet_pid>/follow", methods=["POST"])
@session_required
def follow(current_user, pet_pid):
    followPetForm = FollowPetForm()
    if followPetForm.validate_on_submit():
        follow_pet = PetService.follow(pet_pid)

        if follow_pet.ok:
            resp = json.loads(follow_pet.text)
            flash(resp["message"], "success")

            return redirect(url_for("pet.posts", pet_pid=pet_pid))
        
        flash(json.loads(follow_pet.text)["message"], "danger")

    if followPetForm.errors:
        for key in followPetForm.errors:
            for message in followPetForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("pet.posts", pet_pid=pet_pid))

@pet_bp.route("/<pet_pid>/unfollow", methods=["POST"])
@session_required
def unfollow(current_user, pet_pid):
    unfollowPetForm = UnfollowPetForm()
    if unfollowPetForm.validate_on_submit():
        unfollow_pet = PetService.unfollow(pet_pid, request.form)

        if unfollow_pet.ok:
            resp = json.loads(unfollow_pet.text)
            flash(resp["message"], "success")

            return redirect(url_for("pet.posts", pet_pid=pet_pid))
        
        flash(json.loads(unfollow_pet.text)["message"], "danger")

    if unfollowPetForm.errors:
        for key in unfollowPetForm.errors:
            for message in unfollowPetForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("pet.posts", pet_pid=pet_pid))

@pet_bp.route("/<pet_pid>/followers", methods=["GET", "POST"])
@pet_bp.route("/<pet_pid>/followers/confirmed", methods=["GET", "POST"])
@session_required
def confirmed_followers(current_user, pet_pid):
    get_resp = PetService.get_by_pid(pet_pid)
    if get_resp.ok:
        this_pet = json.loads(get_resp.text)
        this_pet["birthday"] = parser.parse(this_pet["birthday"])

        return render_template("pet_profile.html",
            page_title = "Pet profile",
            current_user = current_user,
            this_pet = this_pet,
            editPetForm = EditPetForm(prefix="epf"),
            deletePetForm = DeletePetForm(),
            followPetForm = FollowPetForm(),
            unfollowPetForm = UnfollowPetForm(),
            inviteFollowerForm = 1,
            follower_list = json.loads(PetService.get_all_confirmed_pet_followers(session["booped_in"], this_pet["public_id"]).text)["data"]
        )
    else:
        abort(404)

@pet_bp.route("/<pet_pid>/followers/pending", methods=["GET", "POST"])
@session_required
def pending_followers(current_user, pet_pid):
    get_resp = PetService.get_by_pid(pet_pid)
    if get_resp.ok:
        this_pet = json.loads(get_resp.text)
        this_pet["birthday"] = parser.parse(this_pet["birthday"])

        return render_template("pet_profile.html",
            page_title = "Pet profile",
            current_user = current_user,
            this_pet = this_pet,
            editPetForm = EditPetForm(prefix="epf"),
            deletePetForm = DeletePetForm(),
            followPetForm = FollowPetForm(),
            unfollowPetForm = UnfollowPetForm(),
            inviteFollowerForm = 1,
            acceptPetForm = AcceptPetForm(),
            follower_list = json.loads(PetService.get_all_pending_pet_followers(session["booped_in"], this_pet["public_id"]).text)["data"]
        )
    else:
        abort(404)

@pet_bp.route("/<pet_pid>/accept", methods=["POST"])
@session_required
def accept(current_user, pet_pid):
    acceptPetForm = AcceptPetForm()
    if acceptPetForm.validate_on_submit():
        accept_pet = PetService.accept(pet_pid, request.form)

        if accept_pet.ok:
            resp = json.loads(accept_pet.text)
            flash(resp["message"], "success")

            return redirect(url_for("pet.pending_followers", pet_pid=pet_pid))
        
        flash(json.loads(accept_pet.text)["message"], "danger")

    if acceptPetForm.errors:
        for key in acceptPetForm.errors:
            for message in acceptPetForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("pet.pending_followers", pet_pid=pet_pid))