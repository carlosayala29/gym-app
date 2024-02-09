from flask import *
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired
from flask_sqlalchemy import *
from sqlalchemy import * 


app = Flask(__name__)

with app.app_context():


    app.config['SECRET_KEY'] = 'my secret key'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)


    class InputForm(FlaskForm):
        exercise = StringField('Exercise', validators=[DataRequired()])
        sets = IntegerField('Sets', validators=[DataRequired()])
        reps = IntegerField('Reps', validators=[DataRequired()])
        submit = SubmitField('Submit')

    class Workout(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        exercise = db.Column(db.String, nullable=False)
        sets = db.Column(db.Integer, nullable=False)
        reps = db.Column(db.Integer, nullable=False)
        date = db.Column(db.String, nullable=False)


    #db.drop_all()
    db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/workouts')
    def workouts():
        workout = Workout.query.all()
        return render_template('workouts.html', workout = workout)

    @app.route('/input_workout', methods=['GET', 'POST'])
    def input_workout():
        form = InputForm()
        if form.validate_on_submit():
            exercise = form.exercise.data
            sets = form.sets.data
            reps = form.reps.data
            from datetime import datetime

            current_date = datetime.now()

            formatted_date = current_date.strftime("%Y-%m-%d %H:%M")
            # manage data
            new_workout = Workout(exercise=exercise, sets=sets, reps=reps, date = formatted_date)

            db.session.add(new_workout)
            db.session.commit()
            

            return redirect(url_for('index'))

        return render_template('input_workout.html', form=form)

    if __name__ == '__main__':
        app.run(debug=True)
