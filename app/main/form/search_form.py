from wtforms.validators import InputRequired
from app.main.form import AttribSelectField
from flask_wtf import FlaskForm
from wtforms import BooleanField

class SearchPetForm(FlaskForm):
    group_input = AttribSelectField("By specie", coerce=str, choices=[])
    subgroup_input = AttribSelectField("By breed", coerce=str, choices=[])
    status_input = AttribSelectField("By status", coerce=int, choices=[(0, "Closed", {"param-str": "&status=0"}), (1, "Open for adoption", {"param-str": "&status=1"}), (2, "Deceased", {"param-str": "&status=2"})])

class SearchPeopleForm(FlaskForm):
    sameFollowedPets_input = BooleanField("")
    sameBreedPreferences_input = BooleanField("")