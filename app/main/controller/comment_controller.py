from app.main.service.comment_service import CommentService
import json
from flask import Flask, request, session, flash, redirect, url_for, jsonify
from ... import comment_bp
from ..util.decorator import session_required
from ..form.comment_form import CreateCommentForm, DeleteCommentForm

@comment_bp.route("/create", methods=["POST"])
@session_required
def create(current_user):
    createCommentForm = CreateCommentForm()
    if createCommentForm.validate_on_submit():
        create_comment = CommentService.create(request.form, request.files)

        if create_comment.ok:
            resp = json.loads(create_comment.text)
            flash(resp["message"], "success")

            return redirect(url_for("post.comments", post_pid=createCommentForm.parent_input.data))
        
        flash(json.loads(create_comment.text), "danger")
    
    if createCommentForm.errors:
        for key in createCommentForm.errors:
            for message in createCommentForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("post.comments", post_pid=createCommentForm.parent_input.data))

@comment_bp.route("/<comment_pid>/delete", methods=["POST"])
@session_required
def delete(current_user, comment_pid):
    deleteCommentForm = DeleteCommentForm()
    if deleteCommentForm.validate_on_submit():
        delete_comment = CommentService.delete(comment_pid)

        if delete_comment.ok:
            flash(json.loads(delete_comment.text)["message"], "success")

            return redirect(url_for("post.comments", post_pid=deleteCommentForm.parent_input.data))
        
        flash(json.loads(delete_comment.text), "danger")

    if deleteCommentForm.errors:
        for key in deleteCommentForm.errors:
            for message in deleteCommentForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("post.comments", post_pid=deleteCommentForm.parent_input.data))

@comment_bp.route("/parent/<parent_pid>", methods=["GET"])
@session_required
def get_all_by_post(current_user, parent_pid):
    return jsonify(
        json.loads(
            CommentService.get_all_by_post(session["booped_in"], parent_pid, request.args.get("pagination_no")).text
        )["data"]
    )