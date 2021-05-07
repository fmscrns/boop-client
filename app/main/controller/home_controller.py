from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import home_bp
from ..util.decorator import session_required
from ..service.business_service import BusinessService
from ..service.user_service import *
from dateutil import parser
import json


@home_bp.route("/feed", methods=["GET", "POST"])
@session_required
def feed(current_user):
    asd = json.loads(BusinessService.get_by_pid(session["booped_in"]).text)
    print(asd)
    return render_template("feed.html",
        page_title = "Feed",
        current_user = current_user,
        business_list = asd
    )
    # return render_template("feed.html",
    #     page_title = "Feed",
    #     current_user = current_user,
    # )

    