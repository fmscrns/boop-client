from app.main.service.comment_service import CommentService
import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort,jsonify
from ... import breed_bp
from ..util.decorator import session_required
from ..service.breed_service import BreedService

@breed_bp.route("/parent/<parent_pid>", methods=["GET"])
@session_required
def get_by_specie(current_user, parent_pid):
    return jsonify(
        json.loads(
            BreedService.get_by_specie(session["booped_in"], parent_pid).text
        )["data"]
    )