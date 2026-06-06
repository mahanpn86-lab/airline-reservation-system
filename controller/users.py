from extensions import db
from models import airplane, flight, user, ticket, seat
from flask import render_template, redirect, url_for, request, flash, abort, current_app
from flask_login import current_user, login_required
from validators.admin import AddAirplane, EditAirplane, AddFlight, EditFlight
from validators.auth import EditUser

class Member:
    def __init__(self, *args, **kwargs):
        pass

    @login_required
    def account(self):
        return render_template("account/index.html")
    
    def account_info(self):
        return render_template("account/info.html")

    @login_required
    def wallet_increase(self):
        if request.method == "POST":
            amount = request.form.get('amount', type=int)
            if amount is None or amount <= 0:
                flash("مبلغ نامعتبر است", "danger")
                return redirect(url_for("wallet_increase"))
            current_user.wallet += amount
            db.session.commit()
            flash("موجودی شما با موفقیت افزایش یافت", "success")
            return redirect(url_for("wallet_increase"))
        return render_template("account/wallet.html")
    
    def del_ticket(self):
        theSeat = seat.Seats.query.filter_by(user_id = current_user.id).first()
        if theSeat != None:
            theTicket = ticket.Tickets.query.filter_by(user_id = current_user.id).first()
            thePrice = theTicket.price
            current_user.wallet += (0.7 * thePrice)
            if theSeat.seat_class == "economy":
                theSeat.flight.economy_passengers -= 1
            elif theSeat.seat_class == "business":
                theSeat.flight.business_passengers -= 1
            elif theSeat.seat_class == "vip":
                theSeat.flight.vip_passengers -= 1
            db.session.query(ticket.Tickets).filter_by(user_id = current_user.id).delete()
            db.session.query(seat.Seats).filter_by(user_id = current_user.id).delete()
            db.session.commit()
            flash("بلیط شما حذف شد و 70% مبلغ بلیط به حساب شما برگشت", "info")
            return redirect(url_for("account"))
        else:
            flash("هیچ بلیطی به نام شما یافت نشد!", "warning")
            return redirect(url_for("account"))
        return render_template("account/index.html")