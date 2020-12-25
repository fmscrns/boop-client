import json
from flask import Flask, render_template, request, session, flash, redirect, url_for
from ... import admin_bp
from ..util.decorator import admin_session_required
from ..service.specie_service import SpecieService
from ..service.breed_service import BreedService
from ..form.specie_form import CreateSpecieForm, EditSpecieForm, DeleteSpecieForm
from ..form.breed_form import CreateBreedForm, EditBreedForm, DeleteBreedForm

@admin_bp.route("/control", methods=["GET", "POST"])
@admin_session_required
def control(current_user):
    return render_template("admin/control.html",
        page_title = "Admin Control",
        current_user = current_user
    )

@admin_bp.route("/species", methods=["GET", "POST"])
@admin_session_required
def species(current_user):
    return render_template("admin/species.html",
        page_title = "Configure Species",
        current_user = current_user,
        specie_list = json.loads(SpecieService.get_all(session["admin_booped_in"]).text)["data"],
        createSpecieForm = CreateSpecieForm(),
        editSpecieForm = EditSpecieForm(),
        deleteSpecieForm = DeleteSpecieForm()
    )

@admin_bp.route("/breeds", methods=["GET", "POST"])
@admin_session_required
def breeds(current_user):
    createBreedForm = CreateBreedForm()
    editBreedForm = EditBreedForm()
    deleteBreedForm = DeleteBreedForm()

    createBreedForm.parent_input.choices = [(specie["public_id"], specie["name"]) for specie in json.loads(SpecieService.get_all(session["admin_booped_in"]).text)["data"]]
    editBreedForm.parent_input.choices = [(specie["public_id"], specie["name"]) for specie in json.loads(SpecieService.get_all(session["admin_booped_in"]).text)["data"]]
    deleteBreedForm.parent_input.choices = [(specie["public_id"], specie["name"]) for specie in json.loads(SpecieService.get_all(session["admin_booped_in"]).text)["data"]]

    return render_template("admin/breeds.html",
        page_title = "Configure Breeds",
        current_user = current_user,
        breed_list = json.loads(BreedService.get_all(session["admin_booped_in"]).text)["data"],
        createBreedForm = createBreedForm,
        editBreedForm = editBreedForm,
        deleteBreedForm = deleteBreedForm
    )

@admin_bp.route("specie/create", methods=["POST"])
@admin_session_required
def create_specie(current_user):
    createSpecieForm = CreateSpecieForm()

    if createSpecieForm.validate_on_submit():
        create_specie = SpecieService.create(session["admin_booped_in"], request.form)

        if create_specie.ok:
            
            flash(json.loads(create_specie.text)["message"], "success")

            return redirect(url_for("admin.species"))

        flash(json.loads(create_specie.text)["message"], "danger")

    if createSpecieForm.errors:
        for key in createSpecieForm.errors:
            for message in createSpecieForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("admin.species"))

@admin_bp.route("specie/edit/<pid>", methods=["POST"])
@admin_session_required
def edit_specie(current_user, pid):
    editSpecieForm = EditSpecieForm()

    if editSpecieForm.validate_on_submit():
        edit_specie = SpecieService.edit(pid, session["admin_booped_in"], request.form)

        if edit_specie.ok:
            
            flash(json.loads(edit_specie.text)["message"], "success")

            return redirect(url_for("admin.species"))

        flash(json.loads(edit_specie.text)["message"], "danger")

    if editSpecieForm.errors:
        for key in editSpecieForm.errors:
            for message in editSpecieForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("admin.species"))

@admin_bp.route("specie/delete/<pid>", methods=["POST"])
@admin_session_required
def delete_specie(current_user, pid):
    deleteSpecieForm = DeleteSpecieForm()

    if deleteSpecieForm.validate_on_submit():
        delete_specie = SpecieService.delete(pid, session["admin_booped_in"], request.form)

        if delete_specie.ok:
            flash(json.loads(delete_specie.text)["message"], "success")

            return redirect(url_for("admin.species"))
        
        flash(json.loads(delete_specie.text)["message"], "danger")

    if deleteSpecieForm.errors:
        for key in deleteSpecieForm.errors:
            for message in deleteSpecieForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("admin.species"))

@admin_bp.route("breed/create", methods=["POST"])
@admin_session_required
def create_breed(current_user):
    createBreedForm = CreateBreedForm()
    createBreedForm.parent_input.choices = [(request.form.get("parent_input"), "")]

    if createBreedForm.validate_on_submit():
        create_specie = BreedService.create(session["admin_booped_in"], request.form)

        if create_specie.ok:
            
            flash(json.loads(create_specie.text)["message"], "success")

            return redirect(url_for("admin.breeds"))

        flash(json.loads(create_specie.text)["message"], "danger")

    if createBreedForm.errors:
        for key in createBreedForm.errors:
            for message in createBreedForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("admin.breeds"))

@admin_bp.route("breed/edit/<pid>", methods=["POST"])
@admin_session_required
def edit_breed(current_user, pid):
    editBreedForm = EditBreedForm()
    editBreedForm.parent_input.choices = [(request.form.get("parent_input"), "")]

    if editBreedForm.validate_on_submit():
        edit_specie = BreedService.edit(pid, session["admin_booped_in"], request.form)

        if edit_specie.ok:
            
            flash(json.loads(edit_specie.text)["message"], "success")

            return redirect(url_for("admin.breeds"))

        flash(json.loads(edit_specie.text)["message"], "danger")

    if editBreedForm.errors:
        for key in editBreedForm.errors:
            for message in editBreedForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("admin.breeds"))

@admin_bp.route("breed/delete/<pid>", methods=["POST"])
@admin_session_required
def delete_breed(current_user, pid):
    deleteBreedForm = DeleteBreedForm()
    deleteBreedForm.parent_input.choices = [(request.form.get("parent_input"), "")]

    if deleteBreedForm.validate_on_submit():
        delete_breed = BreedService.delete(pid, session["admin_booped_in"], request.form)

        if delete_breed.ok:
            flash(json.loads(delete_breed.text)["message"], "success")

            return redirect(url_for("admin.breeds"))
        
        flash(json.loads(delete_breed.text)["message"], "danger")

    if deleteBreedForm.errors:
        for key in deleteBreedForm.errors:
            for message in deleteBreedForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("admin.breeds"))