# -*- coding: utf-8 -*-
"""
    forms.py
    ~~~~~~~~
    Flask-WTForms
"""

from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, Email


pitchPlaceholder = (
    'You have 300 characters to sell your talk. This is known as the "elevator pitch". \
Make it exciting.')

talkFormats = [
    (0, "-- select --"),
    ("IN-DEPTH", "In-Depth Talk (~20-30 minutes, 5-10 minute Q&A)"),
    ("LIGHTNING", "Lightning Talk (~5-10 minutes, no Q&A)"),
    ("DEMO", "Short Demo (~15-20 minutes, &lt; 5 minute Q&A)"),
    ("BEGINNER", "Beginner Track (20 minutes, 5 minute Q&A)")
]

audienceLevels = [
    (0, "-- select --"),
    ("BEGINNER", "Beginner"),
    ("INTERMEDIATE", "Intermediate"),
    ("ADVANCED", "Advanced")
]

descPlaceholder = (
    'This field supports Markdown. The description will be seen by reviewers during \
the CFP process and may eventually be seen by the attendees of the event.')

notesPlaceholder = (
    'This field supports Markdown. Notes will only be seen by reviewers during the CFP \
process. This is where you should explain things such as technical requirements, \
why you\'re the best person to speak on this subject, etc...')


class SubmissionForm(FlaskForm):
    email = EmailField('Email',
        validators=[InputRequired("Please enter your email address."),
        Email("Please enter your email address.")],
        render_kw={'placeholder': 'Email'})
    title = TextField('Title',
        validators=[InputRequired("Your talk needs a name.")],
        render_kw={'placeholder': 'Talk Title'})
    pitch = TextAreaField('Pitch',
        validators=[InputRequired("Field is required.")],
        render_kw={'placeholder': pitchPlaceholder})
    format = SelectField('Talk Format', choices=talkFormats)
    audience = SelectField('Audience Level', choices=audienceLevels)
    description = TextAreaField('Description',
        validators=[InputRequired("Field is required.")],
        render_kw={'placeholder': descPlaceholder})
    notes = TextAreaField('Notes', render_kw={'placeholder': notesPlaceholder})
