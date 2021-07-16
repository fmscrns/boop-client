import json
from flask import request, flash, redirect, url_for
from ... import preference_bp
from ..util.decorator import session_required
from ..service.preference_service import PreferenceService
from ..form.preference_form import CreateBusinessPreferenceForm, CreateCirclePreferenceForm, CreatePetPreferenceForm

@preference_bp.route("/create/pet", methods=["POST"])
@session_required
def create_pet(current_user):
    createPetPreferenceForm = CreatePetPreferenceForm(prefix="cppf")
    createPetPreferenceForm.specie_group_input.choices = [(specie_pid, "", {}) for specie_pid in request.form.getlist("cppf-specie_group_input")]
    createPetPreferenceForm.breed_subgroup_input.choices = [(breed_pid, "", {}) for breed_pid in request.form.getlist("cppf-breed_subgroup_input")]

    if createPetPreferenceForm.validate_on_submit():
        create_preference = PreferenceService.create(request.form)

        if create_preference.ok:
            resp = json.loads(create_preference.text)
            flash(resp["message"], "success")
            return redirect(url_for("settings.preferences_pet"))
        
        flash(json.loads(create_preference.text)["message"], "danger")
    
    if createPetPreferenceForm.errors:
        for key in createPetPreferenceForm.errors:
            for message in createPetPreferenceForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("settings.preferences_pet"))

@preference_bp.route("/create/business", methods=["POST"])
@session_required
def create_business(current_user):
    createBusinessPreferenceForm = CreateBusinessPreferenceForm(prefix="cbpf")
    createBusinessPreferenceForm.business_type_input.choices = [(type_pid, "") for type_pid in request.form.getlist("cbpf-business_type_input")]
    if createBusinessPreferenceForm.validate_on_submit():
        create_preference = PreferenceService.create(request.form)

        if create_preference.ok:
            resp = json.loads(create_preference.text)
            flash(resp["message"], "success")
            return redirect(url_for("settings.preferences_business"))
        
        flash(json.loads(create_preference.text)["message"], "danger")
    
    if createBusinessPreferenceForm.errors:
        for key in createBusinessPreferenceForm.errors:
            for message in createBusinessPreferenceForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("settings.preferences_business"))

@preference_bp.route("/create/circle", methods=["POST"])
@session_required
def create_circle(current_user):
    createCirclePreferenceForm = CreateCirclePreferenceForm(prefix="ccpf")
    createCirclePreferenceForm.circle_type_input.choices = [(type_pid, "") for type_pid in request.form.getlist("ccpf-circle_type_input")]
    if createCirclePreferenceForm.validate_on_submit():
        create_preference = PreferenceService.create(request.form)

        if create_preference.ok:
            resp = json.loads(create_preference.text)
            flash(resp["message"], "success")
            return redirect(url_for("settings.preferences_circle"))
        
        flash(json.loads(create_preference.text)["message"], "danger")
    
    if createCirclePreferenceForm.errors:
        for key in createCirclePreferenceForm.errors:
            for message in createCirclePreferenceForm.errors[key]:
                flash("{}: {}".format(key.split("_")[0], message), "danger")

    return redirect(url_for("settings.preferences_circle"))