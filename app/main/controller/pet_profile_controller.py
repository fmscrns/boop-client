import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import pet_profile_bp
from ..service.user_service import UserService
from ..util.decorator import session_required
from ..form.pet_form import CreatePetForm, EditPetForm, DeletePetForm
from ..service.pet_service import PetService
from ..service.breed_service import BreedService
from ..service.pet_service import PetService
from dateutil import parser

@pet_profile_bp.route("/<pet_pid>", methods=["GET", "POST"])
@pet_profile_bp.route("/<pet_pid>/posts", methods=["GET", "POST"])
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
            deletePetForm = DeletePetForm()
        )
    else:
        abort(404)

@pet_profile_bp.route("pet/edit/<pid>", methods=["POST"])
@session_required
def edit_pet(current_user, pid):
    editPetForm = EditPetForm(prefix="epf")

    if editPetForm.validate_on_submit():
        edit_pet = PetService.edit(pid, session["booped_in"], request.form, request.files)

        if edit_pet.ok:
            resp = json.loads(edit_pet.text)
            flash(resp["message"], "success")

            return redirect(url_for("pet_profile.posts", pet_pid=pid))
        
        flash(json.loads(edit_pet.text)["message"], "danger")
    
    if editPetForm.errors:
        for key in editPetForm.errors:
            for message in editPetForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("pet_profile.posts", pet_pid=pid))

@pet_profile_bp.route("pet/delete/<pid>", methods=["POST"])
@session_required
def delete_pet(current_user, pid):
    deletePetForm = DeletePetForm()
    owner_username = json.loads(PetService.get_by_pid(pid).text)["owner_username"]
    if deletePetForm.validate_on_submit():
        delete_pet = PetService.delete(pid, request.form)

        if delete_pet.ok:
            flash(json.loads(delete_pet.text)["message"], "success")

            return redirect(url_for("user_profile.pets", username=owner_username))
        
        flash(json.loads(delete_pet.text), "danger")

    if deletePetForm.errors:
        for key in deletePetForm.errors:
            for message in deletePetForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("pet_profile.posts", pet_pid=pid))