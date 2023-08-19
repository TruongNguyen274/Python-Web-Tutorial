#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from wtforms import (StringField, SubmitField, DateField,
                     SelectField, SelectMultipleField)
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from datetime import datetime

state = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME')
]
genres = [
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other'),
]

#----------------------------------------------------------------------------#
# VenueForm.
#----------------------------------------------------------------------------#

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=genres
    )
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired()]
    )
    website = StringField(
        'website', validators=[DataRequired()]
    )
    submit = SubmitField("Submit")

#----------------------------------------------------------------------------#
# ArtistForm.
#----------------------------------------------------------------------------#

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=genres
    )
    facebook_link = StringField(
        'facebook_link', validators=[DataRequired()]
    )
    website = StringField(
        'website', validators=[DataRequired()]
    )
    submit = SubmitField("submit")

#----------------------------------------------------------------------------#
# ShowForm.
#----------------------------------------------------------------------------#

class ShowForm(FlaskForm):
    venue_id = StringField("navenue_id", validators=[DataRequired()])
    artist_id = StringField("artist_id", validators=[DataRequired()])
    start_time = DateField("start_time", validators=[
                           DataRequired()], default=datetime.today())
    submit = SubmitField("Submit")
