import games.adapters.repository as repo
from games.description.services import get_game
from games.reviews.reviews import ReviewForm
from games.reviews import services as review_services
from games.auth.authentication import login_required
from flask import Blueprint, session, render_template, url_for, redirect
import games.wishlist.services as services

description_blueprint = Blueprint(
    'description_bp', __name__
)


@description_blueprint.route("/description/<game_id>", methods=['GET', 'POST'])
@login_required
def description(game_id):
    user_id = session["username"]
    game = get_game(int(game_id), repo.repo_instance)
    form = ReviewForm()
    # reviews_per_user = review_services.reviews_per_user_limit(game_id, user_id, repo.repo_instance)
    # print(reviews_per_user)
    reviews = review_services.get_reviews_for_game(game_id, repo.repo_instance)  # Fetch reviews for the game
    print(reviews)
    average_rating = review_services.calculate_average_rating(game, repo.repo_instance)  # Calculate average rating
    wishlist_games = services.get_user_wishlist(user_id, repo.repo_instance)
    wishlist_game_ids = [game.game_id for game in wishlist_games]
    # if form.validate_on_submit():
    #     return redirect(url_for('description_bp.description'))  # Redirect after handling form submission

    return render_template('gameDescription.html',
                           game=game,
                           form=form,
                           reviews=reviews,
                           average_rating=average_rating,
                           wishlist_game_ids=wishlist_game_ids)
