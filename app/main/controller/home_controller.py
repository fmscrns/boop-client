from flask import Flask, render_template, request, session, flash, redirect, url_for, abort
from ... import home_bp
from ..util.decorator import session_required
from ..service.business_service import BusinessService
from ..service.post_service import  PostService
from ..service.user_service import *
from ..form.post_form import CreatePostForm
from dateutil import parser
import json


# @home_bp.route("/feed", methods=["GET", "POST"])
# @session_required
# def feed(current_user):
#     return render_template("feed.html",
#         page_title = "Feed",
#         current_user = current_user
#     )


@home_bp.route("/feed", methods=["GET", "POST"])
@session_required
def feed(current_user):
    all_post_request = PostService.get_all_posts()
    if all_post_request.ok:
        all_Posts = json.loads(all_post_request.text)["data"]

        createPostForm = CreatePostForm()
        # print(type(all_Posts))


        return render_template("feed.html",
            page_title = "Feed",
            current_user = current_user,
            createPostForm = createPostForm,
            all_Posts = all_Posts
        )
    else:
        abort(404)
    # all_Posts = PostService.get_all_posts()
    # createPostForm = CreatePostForm()
    # print(all_Posts)
    
    # return render_template("feed.html",
    # page_title = "Feed",
    # current_user = current_user,
    # createPostForm = createPostForm,
    # all_Posts = all_Posts
    # )
    