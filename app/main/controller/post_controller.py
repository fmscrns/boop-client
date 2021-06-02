import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import post_bp
from ..util.decorator import session_required
from ..service.post_service import PostService
from ..form.post_form import CreatePostForm, DeletePostForm
from dateutil import parser

@post_bp.route("/<post_pid>", methods=["GET", "POST"])
@post_bp.route("/<post_pid>/comments", methods=["GET", "POST"])
@session_required
def comments(current_user, post_pid):
    get_resp = PostService.get_by_pid(post_pid)
    if get_resp.ok:
        this_post = json.loads(get_resp.text)
        this_post["registered_on"] = parser.parse(this_post["registered_on"])
        
        return render_template("post_profile.html",
            page_title = "Post profile",
            current_user = current_user,
            this_post = this_post,
            deletePostForm = DeletePostForm()
        )
    else:
        abort(404)

@post_bp.route("/create", methods=["POST"])
@session_required
def create(current_user):
    createPostForm = CreatePostForm()

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
                return redirect(url_for("user.posts", username=resp["payload"]))
        
        flash(json.loads(create_post.text), "danger")
    
    if createPostForm.errors:
        for key in createPostForm.errors:
            for message in createPostForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    if createPostForm.pinboard_input.data:
        return redirect(url_for("business.posts", business_pid=createPostForm.pinboard_input.data))
    elif createPostForm.confiner_input.data:
        return redirect(url_for("circle.posts", circle_pid=createPostForm.confiner_input.data))
    else:
        return redirect(url_for("user.posts", username=resp["payload"]))

@post_bp.route("/<post_pid>/delete", methods=["POST"])
@session_required
def delete(current_user, post_pid):
    deletePostForm = DeletePostForm()
    creator_username = json.loads(PostService.get_by_pid(post_pid).text)["creator_username"]
    if deletePostForm.validate_on_submit():
        delete_post = PostService.delete(post_pid)

        if delete_post.ok:
            flash(json.loads(delete_post.text)["message"], "success")

            return redirect(url_for("user.posts", username=creator_username))
        
        flash(json.loads(delete_post.text), "danger")

    if deletePostForm.errors:
        for key in deletePostForm.errors:
            for message in deletePostForm.errors[key]:
                flash("{}: {}".format(key, message), "danger")

    return redirect(url_for("post.comments", post_pid=pid))