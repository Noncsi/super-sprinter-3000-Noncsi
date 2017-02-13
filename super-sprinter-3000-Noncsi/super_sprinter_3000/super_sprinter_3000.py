# all the imports
import os
from peewee import *
from super_sprinter_3000.connectdatabase import ConnectDatabase
from super_sprinter_3000.models import *
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, current_app


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'super_sprinter_3000.db'),
    SECRET_KEY='development key',))


def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.create_tables([Entries], safe=True)


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/')
@app.route('/list')
def list_story():
    entries = Entries.select().order_by(Entries.id.desc())
    return render_template('list.html', entries=entries)


@app.route('/story')
def show_story():
    return render_template('form.html')


@app.route('/story/add_story', methods=['POST'])
def add_entry():
    new_entry = Entries.create(story_title=request.form['story_title'],
                               user_story=request.form['user_story'],
                               acceptance_criteria=request.form['acceptance_criteria'],
                               business_value=request.form['business_value'],
                               estimation_time=request.form['estimation_time'],
                               status=request.form['status'])
    new_entry.save()
    flash("A new Story has been successfully saved")
    return redirect(url_for('list_story'))


@app.route('/story/<story_id>')
def edit_story(story_id):
    entry = Entries.select().where(Entries.id == story_id).get()
    return render_template('form.html', entry=entry)


@app.route('/story/edit/<story_id>', methods=['POST'])
def update_story(story_id):
    entry = Entries.select().where(Entries.id == story_id).get()
    entry.story_title = request.form["story_title"]
    entry.user_story = request.form["user_story"]
    entry.acceptance_criteria = request.form["acceptance_criteria"]
    entry.business_value = request.form["business_value"]
    entry.estimation_time = request.form["estimation_time"]
    entry.status = request.form["status"]
    entry.save()
    return redirect(url_for('list_story'))


@app.route('/story/delete/<story_id>')
def delete_story(story_id):
    delete_entry = Entries.delete().where(Entries.id == story_id)
    delete_entry.execute()
    return redirect(url_for('list_story'))
