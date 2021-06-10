import json
from flask import Flask, render_template, request, session, flash, redirect, url_for
from ... import admin_bp
from ..util.decorator import admin_session_required
from ..service.specie_service import SpecieService
from ..service.breed_service import BreedService
from ..service.businessType_service import BusinessTypeService
from ..form.specie_form import CreateSpecieForm, EditSpecieForm, DeleteSpecieForm
from ..form.businessType_form import CreateBusinessTypeForm, EditBusinessTypeForm, DeleteBusinessTypeForm
from ..form.breed_form import CreateBreedForm, EditBreedForm, DeleteBreedForm
from ..service.circleType_service import CircleTypeService
from ..form.circleType_form import CreateCircleTypeForm, EditCircleTypeForm, DeleteCircleTypeForm



@admin_bp.route("/control", methods=["GET", "POST"])
@admin_session_required
def control(current_user):
    return render_template("admin/control.html",
        page_title = "Admin Control",
        current_user = current_user
    )

@admin_bp.route("/business_types", methods=["GET", "POST"])
@admin_session_required
def business_types(current_user):
    asd = json.loads(BusinessTypeService.get_all(session["admin_booped_in"]).text)["data"]
    print(asd)
    return render_template("admin/business_types.html",
        page_title = "Configure Business Types",
        current_user = current_user,
        businessType_list = asd,
        createBusinessTypeForm = CreateBusinessTypeForm(),
        editBusinessTypeForm = EditBusinessTypeForm(),
        deleteBusinessTypeForm = DeleteBusinessTypeForm()
    )

@admin_bp.route("/circle_types", methods=["GET", "POST"])
@admin_session_required
def circle_types(current_user):
    asd = json.loads(CircleTypeService.get_all(session["admin_booped_in"]).text)["data"]
    print(asd)
    return render_template("admin/circle_types.html",
        page_title = "Configure Circle Types",
        current_user = current_user,
        circleType_list = asd,
        createCircleTypeForm = CreateCircleTypeForm(),
        editCircleTypeForm = EditCircleTypeForm(),
        deleteCircleTypeForm = DeleteCircleTypeForm()
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
    createBreedForm = CreateBreedForm(prefix="cbf")
    editBreedForm = EditBreedForm(prefix="ebf")
    deleteBreedForm = DeleteBreedForm(prefix="dbf")
    createBreedForm.parent_input.choices = [(specie["public_id"], specie["name"]) for specie in json.loads(SpecieService.get_all(session["admin_booped_in"]).text)["data"]]
    editBreedForm.parent_input.choices = [(specie["public_id"], specie["name"]) for specie in json.loads(SpecieService.get_all(session["admin_booped_in"]).text)["data"]]
    deleteBreedForm.parent_input.choices = [(specie["public_id"], specie["name"]) for specie in json.loads(SpecieService.get_all(session["admin_booped_in"]).text)["data"]]
    breed_list = BreedService.get_all(session["admin_booped_in"])
    if breed_list.ok:
        breed_list = json.loads(breed_list.text)["data"]
    return render_template("admin/breeds.html",
        page_title = "Configure Breeds",
        current_user = current_user,
        breed_list = breed_list,
        createBreedForm = createBreedForm,
        editBreedForm = editBreedForm,
        deleteBreedForm = deleteBreedForm
    )

@admin_bp.route("/business_type/create", methods=["POST"])
@admin_session_required
def create_businessType(current_user):
    createBusinessTypeForm = CreateBusinessTypeForm()

    if createBusinessTypeForm.validate_on_submit():
        create_businessType = BusinessTypeService.create(session["admin_booped_in"], request.form)

        if create_businessType.ok:
            
            flash(json.loads(create_businessType.text)["message"], "success")

            return redirect(url_for("admin.business_types"))

        flash(json.loads(create_businessType.text)["message"], "danger")

    if createBusinessTypeForm.errors:
        for key in createBusinessTypeForm.errors:
            for message in createBusinessTypeForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("admin.business_types"))

@admin_bp.route("/business_type/edit/<pid>", methods=["POST"])
@admin_session_required
def edit_businessType(current_user, pid):
    editBusinessTypeForm = EditBusinessTypeForm()

    if editBusinessTypeForm.validate_on_submit():
        edit_businessType = BusinessTypeService.edit(pid, session["admin_booped_in"], request.form)

        if edit_businessType.ok:
            
            flash(json.loads(edit_businessType.text)["message"], "success")

            return redirect(url_for("admin.business_types"))

        flash(json.loads(edit_businessType.text)["message"], "danger")

    if editBusinessTypeForm.errors:
        for key in editBusinessTypeForm.errors:
            for message in editBusinessTypeForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("admin.business_types"))

@admin_bp.route("/business_type/delete/<pid>", methods=["POST"])
@admin_session_required
def delete_businessType(current_user, pid):
    deleteBusinessTypeForm = DeleteBusinessTypeForm()

    if deleteBusinessTypeForm.validate_on_submit():
        delete_businessType = BusinessTypeService.delete(pid, session["admin_booped_in"], request.form)

        if delete_businessType.ok:
            flash(json.loads(delete_businessType.text)["message"], "success")

            return redirect(url_for("admin.business_types"))
        
        flash(json.loads(delete_businessType.text)["message"], "danger")

    if deleteBusinessTypeForm.errors:
        for key in deleteBusinessTypeForm.errors:
            for message in deleteBusinessTypeForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("admin.business_types"))


@admin_bp.route("/circle_type/create", methods=["POST"])
@admin_session_required
def create_circleType(current_user):
    createCircleTypeForm = CreateCircleTypeForm()

    if createCircleTypeForm.validate_on_submit():
        create_circleType = CircleTypeService.create(session["admin_booped_in"], request.form)

        if create_circleType.ok:
            
            flash(json.loads(create_circleType.text)["message"], "success")

            return redirect(url_for("admin.circle_types"))

        flash(json.loads(create_circleType.text)["message"], "danger")

    if createCircleTypeForm.errors:
        for key in createCircleTypeForm.errors:
            for message in createCircleTypeForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("admin.circle_types"))

@admin_bp.route("/circle_type/edit/<pid>", methods=["POST"])
@admin_session_required
def edit_circleType(current_user, pid):
    editCircleTypeForm = EditCircleTypeForm()

    if editCircleTypeForm.validate_on_submit():
        edit_circleType = CircleTypeService.edit(pid, session["admin_booped_in"], request.form)

        if edit_circleType.ok:
            
            flash(json.loads(edit_circleType.text)["message"], "success")

            return redirect(url_for("admin.circle_types"))

        flash(json.loads(edit_circleType.text)["message"], "danger")

    if editCircleTypeForm.errors:
        for key in editCircleTypeForm.errors:
            for message in editCircleTypeForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("admin.circle_types"))

@admin_bp.route("/circle_type/delete/<pid>", methods=["POST"])
@admin_session_required
def delete_circleType(current_user, pid):
    deleteCircleTypeForm = DeleteCircleTypeForm()

    if deleteCircleTypeForm.validate_on_submit():
        delete_circleType = CircleTypeService.delete(pid, session["admin_booped_in"], request.form)

        if delete_circleType.ok:
            flash(json.loads(delete_circleType.text)["message"], "success")

            return redirect(url_for("admin.circle_types"))
        
        flash(json.loads(delete_circleType.text)["message"], "danger")

    if deleteCircleTypeForm.errors:
        for key in deleteCircleTypeForm.errors:
            for message in deleteCircleTypeForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("admin.circle_types"))

@admin_bp.route("/specie/create", methods=["POST"])
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
                flash(message, "danger")

    return redirect(url_for("admin.species"))

@admin_bp.route("/specie/edit/<pid>", methods=["POST"])
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
                flash(message, "danger")

    return redirect(url_for("admin.species"))

@admin_bp.route("/specie/delete/<pid>", methods=["POST"])
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
                flash(message, "danger")

    return redirect(url_for("admin.species"))

@admin_bp.route("/breed/create", methods=["POST"])
@admin_session_required
def create_breed(current_user):
    createBreedForm = CreateBreedForm(prefix="cbf")
    createBreedForm.parent_input.choices = [(request.form.get("cbf-parent_input"), "")]

    if createBreedForm.validate_on_submit():
        create_specie = BreedService.create(session["admin_booped_in"], request.form)

        if create_specie.ok:
            
            flash(json.loads(create_specie.text)["message"], "success")

            return redirect(url_for("admin.breeds"))

        flash(json.loads(create_specie.text)["message"], "danger")

    if createBreedForm.errors:
        for key in createBreedForm.errors:
            for message in createBreedForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("admin.breeds"))

@admin_bp.route("/breed/edit/<pid>", methods=["POST"])
@admin_session_required
def edit_breed(current_user, pid):
    editBreedForm = EditBreedForm(prefix="ebf")
    editBreedForm.parent_input.choices = [(request.form.get("ebf-parent_input"), "")]

    if editBreedForm.validate_on_submit():
        edit_specie = BreedService.edit(pid, session["admin_booped_in"], request.form)

        if edit_specie.ok:
            
            flash(json.loads(edit_specie.text)["message"], "success")

            return redirect(url_for("admin.breeds"))

        flash(json.loads(edit_specie.text)["message"], "danger")

    if editBreedForm.errors:
        for key in editBreedForm.errors:
            for message in editBreedForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("admin.breeds"))

@admin_bp.route("/breed/delete/<pid>", methods=["POST"])
@admin_session_required
def delete_breed(current_user, pid):
    deleteBreedForm = DeleteBreedForm(prefix="dbf")
    deleteBreedForm.parent_input.choices = [(request.form.get("dbf-parent_input"), "")]

    if deleteBreedForm.validate_on_submit():
        delete_breed = BreedService.delete(pid, session["admin_booped_in"], request.form)

        if delete_breed.ok:
            flash(json.loads(delete_breed.text)["message"], "success")

            return redirect(url_for("admin.breeds"))
        
        flash(json.loads(delete_breed.text)["message"], "danger")

    if deleteBreedForm.errors:
        for key in deleteBreedForm.errors:
            for message in deleteBreedForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("admin.breeds"))