from flask import Blueprint, request, render_template, session, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, validators, SubmitField
import games.reviews.services as services
import games.adapters.repository as repo
from games.auth.authentication import login_required

reviews_blueprint = Blueprint('reviews_bp', __name__)


class ReviewForm(FlaskForm):
    rating = IntegerField('Rating (0-5)', [validators.InputRequired(), validators.NumberRange(min=0, max=5)])
    comment = TextAreaField('Comment', [
        validators.Length(min=0, max=500, message="Your Review Should Be Between 1 to 500 Characters")
    ])
    submit = SubmitField('Submit')


@reviews_blueprint.route('/write_review/<int:game_id>', methods=['GET', 'POST'])
@login_required
def write_review(game_id):
    game = repo.repo_instance.get_game(game_id)
    if not game:
        return redirect(url_for('home_bp.home'))

    form = ReviewForm(request.form)
    user = session["username"]

    if form.validate_on_submit():
        # Use the service to add the review.
        success = services.add_review_for_game(
            user=user,
            game=game,
            rating=form.rating.data,
            comment=form.comment.data,
            repo=repo.repo_instance
        )

        if success:
            flash('Review added successfully', 'success')
        else:
            flash('There was an issue adding the review', 'error')

        return redirect(url_for('reviews_bp.game_reviews', game_id=game_id))

    return render_template('write_review.html', form=form, game=game)


@reviews_blueprint.route('/game_reviews/<int:game_id>')
@login_required
def game_reviews(game_id):
    game = repo.repo_instance.get_game(game_id)
    if not game:
        return redirect(url_for('home_bp.home'))

    reviews = services.get_reviews_for_game(game_id, repo.repo_instance)
    average_rating = services.calculate_average_rating(game_id, repo.repo_instance)
    print(reviews)
    return render_template('gameDescription.html', game=game, reviews=reviews, average_rating=average_rating)





