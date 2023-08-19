#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import dateutil.parser
import babel
from datetime import datetime
from flask import (Flask, render_template, request,
                   flash, redirect, url_for)
from flask_moment import Moment
from flask_migrate import Migrate
from forms import VenueForm, ArtistForm, ShowForm
from config import Config
from models import (db, Venue, Artist, Show)

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
    data = Venue.query.order_by('city', 'state', 'name').all()
    results = []

    for venue in data:
        found = False
        for area in results:
            if area['city'] == venue.city and area['state'] == venue.state:
                found = True
                area['venues'].append({
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": 0
                })
                break
        
        if not found:
            results.append({
                "city": venue.city,
                "state": venue.state,
                "venues": [{
                    "id": venue.id,
                    "name": venue.name,
                    "num_upcoming_shows": 0
                }]
            })

    return render_template('pages/venues.html', results=results)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    name_venues = request.form.get('search_term')
    response = Venue.query.filter(Venue.name.ilike('%' + name_venues + '%'))
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    data = Venue.query.filter_by(id=venue_id).first()

    upcoming_shows = []
    past_shows = []
    for show in data.shows:
        if show.start_time > datetime.now():
            upcoming_shows.append(show)
        else:
            past_shows.append(show)
    data.upcoming_shows = upcoming_shows
    data.past_shows = past_shows

    split_genres = []
    for item in data.genres.split(','):
        split_genres.append(item.translate({ord(i): None for i in '{",}'}))

    data.genres = split_genres

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue_form():
    form = VenueForm(request.form, meta={'csrf': False})
    if form.validate_on_submit():
        venue = Venue(name=form.name.data, city=form.city.data,
                    state=form.state.data, phone=form.phone.data,
                    address=form.address.data,
                    genres=form.genres.data, facebook_link=form.facebook_link.data,
                    image_link=form.image_link.data, website=form.website.data)
    
        form.name.data = ''
        form.city.data = ''
        form.state.data = ''
        form.address.data = ''
        form.phone.data = ''
        form.image_link.data = ''
        form.facebook_link.data = ''
        
        db.session.add(venue)
        db.session.commit()
        return redirect(url_for('venues'))
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/<int:venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
    venue = Venue.query.filter_by(venue_id).first()
    form = VenueForm()
    return render_template('forms/delete_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/delete', methods=['POST'])
def delete_venue_submit(venue_id):
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
    return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
    name_artist = request.form.get('search_artist')
    response = Artist.query.filter(name=name_artist)
    return render_template('pages/search_artist.html', results=response, search_artist=request.form.get('search_artist', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    response = Artist.query.filter_by(id=artist_id).first()
    past_show_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now())
    past_shows = []
    for show in past_show_query:
        past_shows.append(show)

    upcomming_show_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now())
    upcomming_shows = []
    for show in upcomming_show_query:
        upcomming_shows.append(show)

    split_genres = []
    for item in response.genres.split(','):
        split_genres.append(item.translate({ord(i): None for i in '{",}'}))

    response.genres = split_genres

    return render_template('pages/show_artist.html', artist=response, past_shows=past_shows, upcomming_shows=upcomming_shows)

@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist_form():
    form = ArtistForm(request.form, meta={'csrf': False})
    if form.validate_on_submit():
        artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
                    genres=form.genres.data, phone=form.phone.data, image_link=form.image_link.data,
                    facebook_link=form.facebook_link.data, website=form.website.data)
   
        form.name.data = ''
        form.city.data = ''
        form.state.data = ''
        form.genres.data = ''
        form.phone.data = ''
        form.image_link.data = ''
        form.facebook_link.data = ''
        form.website.data = ''
        
        db.session.add(artist)
        db.session.commit()

        return redirect(url_for('artists'))
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/<int:artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
    artist = Artist.query.filter_by(id=artist_id).first()
    form = ArtistForm()
    return render_template('forms/delete_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/delete', methods=['POST'])
def delete_artist_submit(artist_id):
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
    return redirect(url_for('index'))

#  Update
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    data = Venue.query.filter_by(id=venue_id).first()
    form = VenueForm()
    return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submit(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    venue.name = form.name.data
    venue.phone = form.phone.data
    venue.facebook_link = form.facebook_link.data
    venue.image_link = form.image_link.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.genres = form.genres.data
    venue.website = form.website.data

    db.session.add(venue)
    db.session.commit()
    return redirect(url_for('show_venue', venue_id=venue_id))

@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(meta={'csrf': False})
    if form.validate_on_submit():
        artist.name = form.name.data
        artist.phone = form.phone.data
        artist.facebook_link = form.facebook_link.data
        artist.image_link = form.image_link.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.genres = form.genres.data
        artist.website = form.website.data

        db.session.add(artist)
        db.session.commit()
        return redirect(url_for('show_artist', artist_id=artist_id))

    form.name.data = artist.name
    form.phone.data = artist.phone
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.city.data = artist.city
    form.state.data = artist.state
    form.genres.data = artist.genres
    form.website.data = artist.website

    return render_template('forms/edit_artist.html', form=form)

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    return render_template('pages/shows.html', shows=Show.query.all())

@app.route('/shows/create', methods=['GET','POST'])
def create_show_submit():
    form = ShowForm(request.form, meta={'csrf': False})
    if form.validate_on_submit():
        show = Show(venue_id=form.venue_id.data,
                artist_id=form.artist_id.data, start_time=form.start_time.data)
   
        form.venue_id.data = ''
        form.artist_id.data = ''
        form.start_time.data = ''
        
        db.session.add(show)
        db.session.commit()

        return redirect(url_for('shows'))

    return render_template('forms/new_show.html', form=form)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)
