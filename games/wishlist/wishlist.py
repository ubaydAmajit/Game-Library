from flask import Blueprint, session, request, render_template, flash, url_for, redirect
import games.wishlist.services as services
import games.adapters.repository as repo
from games.auth.authentication import login_required

wishlist_blueprint = Blueprint(
    'wishlist_bp', __name__
)


@wishlist_blueprint.route('/wishlist/add', methods=["POST"])
@login_required
def wishlist_add():
    user_id = session["username"]
    game_id = request.form.get('game_id')

    try:
        services.add_game_to_wishlist(user_id, game_id, repo.repo_instance)
        flash('Game added to wishlist!', 'success')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('wishlist_bp.wishlist'))


@wishlist_blueprint.route('/wishlist/remove', methods=["POST"])
@login_required
def wishlist_remove():
    user_id = session["username"]
    game_id = request.form.get('game_id')
    try:
        services.remove_game_from_wishlist(user_id, game_id, repo.repo_instance)
        flash('Game removed from wishlist!', 'success')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('wishlist_bp.wishlist'))


@wishlist_blueprint.route('/wishlist/', methods=["GET"])
@login_required
def wishlist():
    user_id = session["username"]
    wishlist_games = services.get_user_wishlist(user_id, repo.repo_instance)
    return render_template("wishlist.html", wishlist_games=wishlist_games)
