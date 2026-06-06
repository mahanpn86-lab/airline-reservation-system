from flask import Flask, render_template, redirect, url_for, request, flash, abort
from validators.auth import Register, Login
from extensions import db
from flask_login import login_user, logout_user, login_required
from models import user


class Authentication:
    def __init__(self, *args, **kwargs):
        pass

    def register(self):
        form = Register()
        if request.method == "POST":
            if form.validate_on_submit():
                full_name = request.form.get("full_name")
                national_code = request.form.get("national_code")
                phone = request.form.get("phone")
                User = user.Users.query.filter_by(national_code = national_code).first()
                if not User:
                    newUser = user.Users( full_name=full_name, national_code=national_code, phone=phone)
                    db.session.add(newUser)
                    result = db.session.commit()
                    if result != False:
                        flash("ثبت نام با موفقیت انجام شد", "success")
                        return redirect(url_for("register"))
                else:
                    flash("کاربر با این مشخصات وجود دارد", "info")
                    return redirect(url_for("register"))
        return render_template("auth/register.html", form = form)
    
    def signin(self):
        form = Login()
        if request.method == "POST":
            if form.validate_on_submit():
                national_code = request.form.get("national_code")
                phone = request.form.get("phone")
                phone = int (phone)
                national_code = int (national_code)
                User = user.Users.query.filter_by(national_code = national_code).first()
                if not User:
                    flash("کاربری با این مشخصات یافت نشد", "warning")
                    return redirect(url_for("signin"))
                if User and User.phone == phone :
                    login_user(User, remember=False)  # برا این از UserMixin به ارث برده شد
                    next_page = request.args.get("next")
                    return redirect(next_page) if next_page else redirect(url_for("main"))
        return render_template ("auth/signin.html", form = form)

    def signout(self):
        logout_user()
        return redirect(url_for("main"))


