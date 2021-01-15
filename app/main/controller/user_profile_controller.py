import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import user_profile_bp
from ..service.user_service import UserService
from ..util.decorator import session_required
from ..form.user_form import EditUserForm
from ..form.pet_form import CreatePetForm
from ..form.business_form import CreateBusinessForm
from ..service.specie_service import SpecieService
from ..service.breed_service import BreedService
from ..service.pet_service import PetService
from ..service.business_service import BusinessService


@user_profile_bp.route("/<username>", methods=["GET", "POST"])
@user_profile_bp.route("/<username>/pets", methods=["GET", "POST"])
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

@user_profile_bp.route("user/edit/<pid>", methods=["POST"])
@session_required
def edit_user(current_user, pid):
    editUserForm = EditUserForm(prefix="euf")

    if editUserForm.validate_on_submit():
        edit_user = UserService.edit(pid, session["booped_in"], request.form, request.files)

        if edit_user.ok:
            resp = json.loads(edit_user.text)
            flash(resp["message"], "success")

            return redirect(url_for("user_profile.pets", username=resp["payload"]))
        
        flash(json.loads(edit_user.text)["message"], "danger")
    
    if editUserForm.errors:
        for key in editUserForm.errors:
            for message in editUserForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("user_profile.pets", username=current_user["username"]))

@user_profile_bp.route("pet/create", methods=["POST"])
@session_required
def create_pet(current_user):
    createPetForm = CreatePetForm()

    createPetForm.group_input.choices = [(request.form.get("group_input"), "")]
    createPetForm.subgroup_input.choices = [(request.form.get("subgroup_input"), "")]

    if createPetForm.validate_on_submit():
        create_pet = PetService.create(request.form, request.files)

        if create_pet.ok:
            resp = json.loads(create_pet.text)
            flash(resp["message"], "success")

            return redirect(url_for("user_profile.pets", username=resp["payload"]))
        
        flash(json.loads(create_pet.text), "danger")
    
    if createPetForm.errors:
        for key in createPetForm.errors:
            for message in createPetForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("user_profile.pets", username=current_user["username"]))

@user_profile_bp.route("/<username>", methods=["GET", "POST"])
@user_profile_bp.route("/<username>/businesses", methods=["GET", "POST"])
@session_required
def businesses(current_user, username):
    get_resp = UserService.get_by_username(username)
    if get_resp.ok:
        editUserForm = EditUserForm(prefix="euf")
        editUserForm.name_input.data = current_user["name"]
        editUserForm.username_input.data = current_user["username"]
        editUserForm.email_input.data = current_user["email"]
        createBusinessForm = CreateBusinessForm()

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

@user_profile_bp.route("business/create", methods=["POST"])
@session_required
def create_business(current_user):
    createBusinessForm = CreateBusinessForm()

    if createBusinessForm.validate_on_submit():
        create_business = BusinessService.create(request.form, request.files)

        if create_business.ok:
            resp = json.loads(create_business.text)
            flash(resp["message"], "success")

            return redirect(url_for("user_profile.businesses", username=resp["payload"]))
        
        flash(json.loads(create_business.text), "danger")
    
    if createBusinessForm.errors:
        for key in createBusinessForm.errors:
            for message in createBusinessForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("user_profile.businesses", username=current_user["username"]))