from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, IntegerField, TimeField, SelectField, DateField
from wtforms.validators import DataRequired


class AddAirplane(FlaskForm):
    name = StringField("name", validators=[DataRequired("فیلد نام اجباری است")])
    capacity_economy = IntegerField("capacity_economy", validators=[DataRequired("فیلد های مربوط به اطلاعات ظرفیت صندلی اجباری است")])
    capacity_business = IntegerField("capacity_business", validators=[DataRequired("فیلد های مربوط به اطلاعات ظرفیت صندلی اجباری است")])
    capacity_vip = IntegerField("capacity_vip", validators=[DataRequired("فیلد های مربوط به اطلاعات ظرفیت صندلی اجباری است")])
    submit = SubmitField("افزودن هواپیما")

class EditAirplane(FlaskForm):
    name = StringField("name", validators=[DataRequired("فیلد نام اجباری است")])
    capacity_economy = IntegerField("capacity_economy", validators=[DataRequired("فیلد های مربوط به اطلاعات ظرفیت صندلی اجباری است")])
    capacity_business = IntegerField("capacity_business", validators=[DataRequired("فیلد های مربوط به اطلاعات ظرفیت صندلی اجباری است")])
    capacity_vip = IntegerField("capacity_vip", validators=[DataRequired("فیلد های مربوط به اطلاعات ظرفیت صندلی اجباری است")])
    submit = SubmitField("ویرایش اطلاعات هواپیما")

class AddFlight(FlaskForm):
    airplane_id = StringField("airplane_id", validators=[DataRequired("فیلد نام هواپیما اجباری است")])
    origin = StringField("origin", validators=[DataRequired("فیلد مبدا اجباری است")])
    destination = StringField("destination", validators=[DataRequired("فیلد مقصد اجباری است")])
    departure_time = TimeField("departure_time", format="%H:%M", validators=[DataRequired("فیلد مربوط به ساعت رفت اجباری است")])
    arrival_time = TimeField("arrival_time", format="%H:%M", validators=[DataRequired("فیلد مربوط به ساعت رسیدن اجباری است")])
    departure_date = DateField("departure_date", format="%Y-%m-%d" , validators=[DataRequired("فیلد مربوط به تاریخ رفت اجباری است")])
    arrival_date = DateField("arrival_date", format="%Y-%m-%d", validators=[DataRequired("فیلد مربوط به تاریخ رسیدن اجباری است")])
    economy_price = IntegerField("economy_price", validators=[DataRequired("بخش های مربوط به قیمت بلیط هارا درست وارد کنید")])
    business_price = IntegerField("business_price", validators=[DataRequired("بخش های مربوط به قیمت بلیط هارا درست وارد کنید")])
    vip_price = IntegerField("vip_price", validators=[DataRequired("بخش های مربوط به قیمت بلیط هارا درست وارد کنید")])
    submit = SubmitField("افزودن پرواز")

class EditFlight(FlaskForm):
    airplane_id = StringField("airplane_id", validators=[DataRequired("فیلد نام هواپیما اجباری است")])
    origin = StringField("origin", validators=[DataRequired("فیلد مبدا اجباری است")])
    destination = StringField("destination", validators=[DataRequired("فیلد مقصد اجباری است")])
    departure_time = TimeField("departure_time", format="%H:%M", validators=[DataRequired("فیلد مربوط به ساعت رفت اجباری است")])
    arrival_time = TimeField("arrival_time", format="%H:%M", validators=[DataRequired("فیلد مربوط به ساعت رسیدن اجباری است")])
    departure_date = DateField("departure_date", format="%Y-%m-%d" , validators=[DataRequired("فیلد مربوط به تاریخ رفت اجباری است")])
    arrival_date = DateField("arrival_date", format="%Y-%m-%d", validators=[DataRequired("فیلد مربوط به تاریخ رسیدن اجباری است")])
    economy_price = IntegerField("economy_price", validators=[DataRequired("بخش های مربوط به قیمت بلیط هارا درست وارد کنید")])
    business_price = IntegerField("business_price", validators=[DataRequired("بخش های مربوط به قیمت بلیط هارا درست وارد کنید")])
    vip_price = IntegerField("vip_price", validators=[DataRequired("بخش های مربوط به قیمت بلیط هارا درست وارد کنید")])
    submit = SubmitField("ویرایش پرواز")