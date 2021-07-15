from app.main.service.comment_service import CommentService
import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort,jsonify
from ... import post_bp
from ..util.decorator import session_required
from ..service.post_service import PostService
from ..service.pet_service import PetService
from ..form.post_form import CreatePostForm, DeletePostForm, LikePostForm
from ..form.comment_form import CreateCommentForm, DeleteCommentForm

@post_bp.route("/<post_pid>", methods=["GET", "POST"])
@post_bp.route("/<post_pid>/comments", methods=["GET", "POST"])
@session_required
def comments(current_user, post_pid):
    get_resp = PostService.get_by_pid(post_pid)
    if get_resp.ok:
        this_post = json.loads(get_resp.text)
        return render_template("post_profile.html",
            page_title = "Post profile",
            current_user = current_user,
            this_post = this_post,
            deletePostForm = DeletePostForm(prefix="dptf"),
            createCommentForm = CreateCommentForm(),
            deleteCommentForm = DeleteCommentForm()
        )        
    else:
        abort(404)

@post_bp.route("/create", methods=["POST"])
@session_required
def create(current_user):
    createPostForm = CreatePostForm()
    createPostForm.subject_input.choices = [(subject["public_id"], subject["name"]) for subject in json.loads(PetService.get_all_by_user(session["booped_in"], current_user["public_id"] + "?tag_suggestions=1").text)["data"]]
    if createPostForm.validate_on_submit():
        create_post = PostService.create(request.form, request.files)

        if create_post.ok:
            resp = json.loads(create_post.text)
            flash(resp["message"], "success")

            if createPostForm.pinboard_input.data:
                return redirect(url_for("business.posts", business_pid=createPostForm.pinboard_input.data))
            elif createPostForm.confiner_input.data:
                return redirect(url_for("circle.posts", circle_pid=createPostForm.confiner_input.data))
            else:
                return redirect(url_for("user.posts", username=current_user["username"]))
        
        flash(json.loads(create_post.text)["message"], "danger")
    
    if createPostForm.errors:
        for key in createPostForm.errors:
            for message in createPostForm.errors[key]:
                flash(message, "danger")

    if createPostForm.pinboard_input.data:
        return redirect(url_for("business.posts", business_pid=createPostForm.pinboard_input.data))
    elif createPostForm.confiner_input.data:
        return redirect(url_for("circle.posts", circle_pid=createPostForm.confiner_input.data))
    else:
        return redirect(url_for("user.posts", username=current_user["username"]))

@post_bp.route("/<post_pid>/like", methods=["POST"])
@session_required
def like(current_user, post_pid):
    return jsonify(json.loads(PostService.like(post_pid).text))

@post_bp.route("/<post_pid>/delete", methods=["POST"])
@session_required
def delete(current_user, post_pid):
    deletePostForm = DeletePostForm(prefix="dptf")
    if deletePostForm.validate_on_submit():
        delete_post = PostService.delete(post_pid)

        if delete_post.ok:
            flash(json.loads(delete_post.text)["message"], "success")

            if deletePostForm.pinboard_input.data:
                return redirect(url_for("business.posts", business_pid=deletePostForm.pinboard_input.data))
            elif deletePostForm.confiner_input.data:
                return redirect(url_for("circle.posts", circle_pid=deletePostForm.confiner_input.data))
            else:
                return redirect(url_for("user.posts", username=current_user["username"]))
        
        flash(json.loads(delete_post.text), "danger")

    if deletePostForm.errors:
        for key in deletePostForm.errors:
            for message in deletePostForm.errors[key]:
                flash(message, "danger")

    return redirect(url_for("post.comments", post_pid=post_pid))

@post_bp.route("/", methods=["GET"])
@session_required
def get_all(current_user):
    return jsonify(
        json.loads(
            PostService.get_all_posts(request.args.get("pagination_no")).text
        )["data"]
    )

@post_bp.route("/bytoken", methods=["GET"])
@session_required
def get_all_by_user(current_user):
    return jsonify(
        json.loads(
            PostService.get_all_by_user(session["booped_in"], request.args.get("pagination_no")).text
        )["data"]
    )

@post_bp.route("/subject/<subject_pid>", methods=["GET"])
@session_required
def get_all_by_pet(current_user, subject_pid):
    return jsonify(
        json.loads(
            PostService.get_all_by_pet(session["booped_in"], subject_pid, request.args.get("w_media_only"), request.args.get("pagination_no")).text
        )["data"]
    )

@post_bp.route("/confiner/<confiner_pid>", methods=["GET"])
@session_required
def get_all_by_circle(current_user, confiner_pid):
    return jsonify(
        json.loads(
            PostService.get_all_by_circle(session["booped_in"], confiner_pid, request.args.get("w_media_only"), request.args.get("pagination_no")).text
        )["data"]
    )

@post_bp.route("/pinboard/<pinboard_pid>", methods=["GET"])
@session_required
def get_all_by_business(current_user, pinboard_pid):
    return jsonify(
        json.loads(
            PostService.get_all_by_business(session["booped_in"], pinboard_pid, request.args.get("w_media_only"), request.args.get("pagination_no")).text
        )["data"]
    )