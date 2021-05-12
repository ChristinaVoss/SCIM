#form imports
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField, ValidationError, SelectMultipleField, SelectField, TextAreaField, widgets
from wtforms.validators import DataRequired, EqualTo, URL, Length, Regexp, Optional
from flask_wtf.file import FileField, FileAllowed

#school imports
###from flask_login import current_user
from schoolclubinfomanager.models import School

# checkbox or dropdown options in forms
YEAR_GROUPS = [('nu', 'Nursery'),
         ('re', 'Reception'),
         ('y1', 'Year group 1'),
         ('y2', 'Year group 2'),
         ('y3', 'Year group 3'),
         ('y4', 'Year group 4'),
         ('y5', 'Year group 5'),
         ('y6', 'Year group 6'),
         ('y7', 'Year group 7'),
         ('y8', 'Year group 8'),
         ('y9', 'Year group 9'),
         ('y10', 'Year group 10'),
         ('y11', 'Year group 11')]

FONTS = [('Arial', 'Arial'),
         ('Baskerville', 'Baskerville'),
         ('Bodoni', 'Bodoni'),
         ('Calibri', 'Calibri'),
         ('Calisto', 'Calisto')]

# helper class to create checkbox fields (https://gist.github.com/doobeh/4668212)
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# Flask forms (wtforms) allow you to easily create forms in format:
# variable_name = Field_type('Label that will show', validators=[V_func1(), V_func2(),...])
class SchoolSetupStep1(FlaskForm):
    name = StringField('Name of school*', validators=[DataRequired(), Length(min=2, max=64)])
    summary = TextAreaField('Summary of school offer', validators=[Length(max=1000)])
    logo = FileField('Upload logo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'svg']), Optional()])
    year_groups = MultiCheckboxField('Year groups you offer clubs to*', choices=YEAR_GROUPS, validators=[DataRequired()])
    school_website = StringField('School website*', validators=[URL()])
    submit = SubmitField('Next')

class SchoolSetupStep2(FlaskForm):
    # use HTML input color option instead
    font_colour = StringField('Choose colour for school name', validators=[Regexp('#[A-Fa-f0-9]{6}', message="Font colour must be valid hexadecimal number")], default='#57F7FA')
    banner_colour = StringField('Choose background colour for banner', validators=[Regexp('#[A-Fa-f0-9]{6}', message="Banner colour must be valid hexadecimal number")], default='#5F6EE6')
    font = SelectField('Choose font', choices=FONTS, default='Arial')
    submit = SubmitField('Save')

'''
Do this for incremental stage 2 when you deal with filters.
You need to figure out how to add category choices to checkbox dynamically,
but if you can't, try to just have a StringField and ask the user to add values
separated by a comma.
class SchoolSetupStep3(FlaskForm):
    categories = SelectMultipleField()

    submit = SubmitField('Next')'''
