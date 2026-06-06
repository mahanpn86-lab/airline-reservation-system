from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Regexp


class Register(FlaskForm):
    full_name = StringField("name", validators=[DataRequired("فیلد نام و نام خانوادگی را درست وارد کنید")])
    national_code = StringField("cnational_codes", validators=[DataRequired("فیلد کد ملی را درست وارد کنید")])
    phone = StringField("phone", validators=[DataRequired("شماره تلفن را به درستی وارد کنید"), Regexp(r"^\+?[0-9\s\-]{10,20}$", message="شماره تلفن معتبر نیست")])
    submit = SubmitField("ثبت نام")

class Login(FlaskForm):
    national_code = StringField("cnational_codes", validators=[DataRequired("فیلد کد ملی را درست وارد کنید")])
    phone = StringField("phone", validators=[DataRequired("شماره تلفن را به درستی وارد کنید"), Regexp(r"^\+?[0-9\s\-]{10,20}$", message="شماره تلفن معتبر نیست")])
    submit = SubmitField("ورود")

class EditUser(FlaskForm):
    full_name = StringField("name", validators=[DataRequired("فیلد نام و نام خانوادگی را درست وارد کنید")])
    national_code = StringField("cnational_codes", validators=[DataRequired("فیلد کد ملی را درست وارد کنید")])
    phone = StringField("phone", validators=[DataRequired("شماره تلفن را به درستی وارد کنید"), Regexp(r"^\+?[0-9\s\-]{10,20}$", message="شماره تلفن معتبر نیست")])
    wallet = StringField("wallet", validators=[DataRequired("مقدار موجودی کاربر را به درستی وارد کنید")])
    admin = SelectField("admin",choices=[("1", "بله"), ("0", "خیر")], default=0)
    submit = SubmitField("ویرایش مشخصات کاربر")