from flask.json import jsonify
from app.main.form.post_form import DeletePostForm
import json
from flask import render_template, request, session, flash, redirect, url_for, abort
from ... import pet_bp
from ..util.decorator import session_required
from ..form.pet_form import AcceptPetForm, CreatePetForm, DeletePetOwnerForm, EditPetForm, DeletePetForm, FollowPetForm, UnfollowPetForm, CreatePetOwnerForm
from ..service.pet_service import PetService
from ..service.pet_service import PetService
from dateutil import parser

@pet_bp.route("/create", methods=["POST"])
@session_required
def create(current_user):
    createPetForm = CreatePetForm()

    createPetForm.group_input.choices = [(request.form.get("group_input"), "")]
    createPetForm.subgroup_input.choices = [(request.form.get("subgroup_input"), "")]

    if createPetForm.validate_on_submit():
        create_pet = PetService.create(request.form, request.files)
        if create_pet.ok:
            flash(json.loads(create_pet.text)["message"], "success")
            return redirect(url_for("user.pets", username=current_user["username"]))
        
        flash(json.loads(create_pet.text)["message"], "danger")
    
    if createPetForm.errors:
        for key in createPetForm.errors:
            for message in createPetForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("user.pets", username=current_user["username"]))

@pet_bp.route("/<pet_pid>/posts", methods=["GET", "POST"])
@pet_bp.route("/<pet_pid>", methods=["GET", "POST"])
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
            createPostForm = 1,
            deletePostForm = DeletePostForm(prefix="dptf"),
            deletePetForm = DeletePetForm(),
            createPetOwnerForm = CreatePetOwnerForm(prefix="cpof"),
            deletePetOwnerForm = DeletePetOwnerForm(prefix="dpof"),
            followPetForm = FollowPetForm(),
            unfollowPetForm = UnfollowPetForm()
        )
    else:
        abort(404)

@pet_bp.route("/<pet_pid>/media", methods=["GET", "POST"])
@session_required
def media(current_user, pet_pid):
    get_resp = PetService.get_by_pid(pet_pid)
    if get_resp.ok:
        this_pet = json.loads(get_resp.text)
        this_pet["birthday"] = parser.parse(this_pet["birthday"])
        
        return render_template("pet_profile.html",
            page_title = "Pet profile",
            current_user = current_user,
            this_pet = this_pet,
            uploadPhotoForm = 1,
            editPetForm = EditPetForm(prefix="epf"),
            deletePetForm = DeletePetForm(),
            createPetOwnerForm = CreatePetOwnerForm(prefix="cpof"),
            deletePetOwnerForm = DeletePetOwnerForm(prefix="dpof"),
            followPetForm = FollowPetForm(),
            unfollowPetForm = UnfollowPetForm()
        )
    else:
        abort(404)

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
            inviteFollowerForm = 1,
            editPetForm = EditPetForm(prefix="epf"),
            deletePetForm = DeletePetForm(),
            createPetOwnerForm = CreatePetOwnerForm(prefix="cpof"),
            deletePetOwnerForm = DeletePetOwnerForm(prefix="dpof"),
            followPetForm = FollowPetForm(),
            unfollowPetForm = UnfollowPetForm(),
            follower_list = json.loads(PetService.get_all_confirmed_pet_followers(session["booped_in"], this_pet["public_id"]).text)["data"] if this_pet["visitor_auth"] > 1 else []
        )
    else:
        abort(404)

@pet_bp.route("/<pet_pid>/followers/pending", methods=["GET", "POST"])
@session_required
def pending_followers(current_user, pet_pid):
    get_resp = PetService.get_by_pid(pet_pid)
    if get_resp.ok:
        this_pet = json.loads(get_resp.text)
        if this_pet["visitor_auth"] == 3:
            this_pet["birthday"] = parser.parse(this_pet["birthday"])

            return render_template("pet_profile.html",
                page_title = "Pet profile",
                current_user = current_user,
                this_pet = this_pet,
                inviteFollowerForm = 1,
                editPetForm = EditPetForm(prefix="epf"),
                deletePetForm = DeletePetForm(),
                createPetOwnerForm = CreatePetOwnerForm(prefix="cpof"),
                deletePetOwnerForm = DeletePetOwnerForm(prefix="dpof"),
                followPetForm = FollowPetForm(),
                unfollowPetForm = UnfollowPetForm(),
                acceptPetForm = AcceptPetForm(),
                follower_list = json.loads(PetService.get_all_pending_pet_followers(session["booped_in"], this_pet["public_id"]).text)["data"]
            )
        else:
            abort(403)
    else:
        abort(404)

@pet_bp.route("/<pet_pid>/owner/create", methods=["POST"])
@session_required
def create_owner(current_user, pet_pid):
    createPetOwnerForm = CreatePetOwnerForm(prefix="cpof")
    if createPetOwnerForm.validate_on_submit():
        create_pet_owner = PetService.create_owner(pet_pid, session["booped_in"], request.form)

        if create_pet_owner.ok:
            flash(json.loads(create_pet_owner.text)["message"], "success")

            return redirect(url_for("pet.posts", pet_pid=pet_pid))
        
        flash(json.loads(create_pet_owner.text)["message"], "danger")
    
    if createPetOwnerForm.errors:
        for key in createPetOwnerForm.errors:
            for message in createPetOwnerForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("pet.posts", pet_pid=pet_pid))

@pet_bp.route("/<pet_pid>/owner/delete", methods=["POST"])
@session_required
def delete_owner(current_user, pet_pid):
    deletePetOwnerForm = DeletePetOwnerForm(prefix="dpof")
    if deletePetOwnerForm.validate_on_submit():
        delete_pet_owner = PetService.delete_owner(pet_pid, session["booped_in"], request.form)

        if delete_pet_owner.ok:
            flash(json.loads(delete_pet_owner.text)["message"], "success")

            if json.loads(delete_pet_owner.text)["single_owner_removed"] == 1:
                return redirect(url_for("user.pets", username=current_user["username"]))
            else:
                return redirect(url_for("pet.posts", pet_pid=pet_pid))
        
        flash(json.loads(delete_pet_owner.text)["message"], "danger")
    
    if deletePetOwnerForm.errors:
        for key in deletePetOwnerForm.errors:
            for message in deletePetOwnerForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("pet.posts", pet_pid=pet_pid))

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
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("pet.posts", pet_pid=pet_pid))

@pet_bp.route("/<pet_pid>/delete", methods=["POST"])
@session_required
def delete(current_user, pet_pid):
    deletePetForm = DeletePetForm()
    if deletePetForm.validate_on_submit():
        delete_pet = PetService.delete(pet_pid, request.form)

        if delete_pet.ok:
            flash(json.loads(delete_pet.text)["message"], "success")
            return redirect(url_for("user.pets", username=current_user["username"]))
        
        flash(json.loads(delete_pet.text), "danger")

    if deletePetForm.errors:
        for key in deletePetForm.errors:
            for message in deletePetForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("pet.posts", pet_pid=pet_pid))

@pet_bp.route("/<pet_pid>/follow", methods=["POST"])
@session_required
def follow(current_user, pet_pid):
    is_async = request.args.get("is_async")
    if is_async is None:
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
                    flash("{}: {}".format(key.split("_")[0], message), "danger")
        return redirect(url_for("pet.posts", pet_pid=pet_pid))

    return jsonify(json.loads(PetService.follow(pet_pid).text))

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
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("pet.posts", pet_pid=pet_pid))

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
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("pet.pending_followers", pet_pid=pet_pid))

@pet_bp.route("/preference", methods=["GET"])
@session_required
def get_all_by_preference(current_user):
    list = json.loads(
        PetService.get_by_preference(request.args.get("pagination_no")).text
    )
    if list.get("data"):
        return jsonify(list["data"])
    else:
        return jsonify([])

@pet_bp.route("/search", methods=["GET"])
@session_required
def search(current_user):
    list = json.loads(
        PetService.search(
            request.args.get("value"),
            request.args.get("group_id"),
            request.args.get("subgroup_id"),
            request.args.get("status"),
            request.args.get("pagination_no")
        ).text
    )
    if list.get("data"):
        return jsonify(
            dict(
                Pet = list["data"]
            )
        )
    else:
        abort(404)