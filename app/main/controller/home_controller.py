from flask import Flask, render_template, request, session, flash, redirect, url_for
from ... import home_bp
from ..util.decorator import session_required


@home_bp.route("/feed", methods=["GET", "POST"])
@session_required
def feed(current_user):
    return render_template("feed.html",
        page_title = "Feed",
        current_user = current_user
    )