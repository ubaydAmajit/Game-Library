from flask import Blueprint, request, render_template, session, url_for, redirect, flash
import games.profile.services as services
import games.adapters.repository as repo
from games.auth.authentication import login_required

profile_blueprint = Blueprint(
    'profile_bp', __name__
)


@profile_blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    username = session.get('username')  # Get the username from the session
    if not username:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('auth_bp.login'))
    user = services.get_username(username, repo.repo_instance)  # Use the get_user service function
    reviews = services.get_reviews_by_user(username, repo.repo_instance)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('home_bp.home'))

    sort_option = request.args.get('sort', default='newest', type=str)
    if sort_option == "newest":
        reviews.reverse()


    return render_template(
        'profile.html',
        user=user,
        reviews=reviews,
        sort_option=sort_option
    )
