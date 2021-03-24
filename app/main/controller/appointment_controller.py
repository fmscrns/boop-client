from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import appointment_bp
from ..util.decorator import session_required
from ..form.appointment_form import CreateAppointmentForm, EditAppointmentForm, DeleteAppointmentForm

@appointment_bp.route("/create", methods=["POST"])
@session_required
def create(current_user):
    createAppointmentForm = CreateAppointmentForm()
    asd = request.args.get("business_pid")
    print("pid = {}".format(asd))
    # createAppointmentForm.type_input.choices = [(request.form.get("type_input"), "")]
    # createAppointmentForm.pet_input.choices = [(request.form.get("pet_input"), "")]

    return render_template("appointment_details.html",
        page_title = "Appointment details",
        current_user = current_user
    )