from extensions import db
from models import airplane, flight, user, seat, ticket
from flask import render_template, redirect, url_for, request, flash, abort, current_app
from flask_login import current_user, login_required
from validators.admin import AddAirplane, EditAirplane, AddFlight, EditFlight
from validators.auth import EditUser
from datetime import datetime, time, timedelta
import os
from random import randint

class Reservation:
    def __init__(self, *args, **kwargs):
        pass

    @login_required
    def reserve_main(self, seat_class):
        origin = request.form.get("origin")
        destination = request.form.get("destination")
        flights = flight.Flights.query.filter_by(origin=origin, destination=destination).all()
        return render_template(f"reserve/{seat_class}_index.html", flights=flights, origin=origin, destination=destination, seat_class=seat_class)

    def choice_seat(self, flight_id, seat_class):
        selected_flight = flight.Flights.query.get(flight_id)
        seats = seat.Seats.query.filter_by(flight_id=flight_id).all()
        booked_seat_numbers = [s.seat_number for s in seats if s.is_booked and s.seat_class == seat_class]
        return render_template ("reserve/seat_map.html", flight=selected_flight, seats=seats, seat_class=seat_class, booked_seat_numbers=booked_seat_numbers)

    def make_reservation(self):
        flight_id = request.form.get("flight_id")
        seat_class = request.form.get("seat_class")
        is_booked = True
        seat_number = request.form.get('seat_id')
        user_id = current_user.id
        theSeat = seat.Seats.query.filter_by(seat_number = seat_number, flight_id = flight_id).first()
        theFlight = flight.Flights.query.filter_by(id = flight_id).first()
        user_reserved_seat = seat.Seats.query.filter_by(flight_id=flight_id, user_id=user_id, is_booked=True).first()
        if user_reserved_seat:
            flash("شما قبلاً برای این پرواز صندلی رزرو کرده‌اید.", "warning")
            return redirect(url_for("choice_seat",flight_id=flight_id,seat_class=seat_class))
        if current_user.wallet < theFlight.economy_price:
            flash("موجودی حساب شما کافی نیست! لطفا از پنل کاربری موجودی خود را شارژ کنید", "danger")
            return redirect(url_for("choice_seat", flight_id=flight_id, seat_class=seat_class))
        if not theSeat:
            newSeat = seat.Seats(flight_id=flight_id, seat_class=seat_class, is_booked=is_booked, user_id=user_id, seat_number = seat_number)
            current_user.wallet -= theFlight.economy_price
            theFlight.economy_passengers += 1
            db.session.add(newSeat)
            result = db.session.commit()
            if result != False:
                flash("صندلی شما با موفقیت رزرو شد", "success")
                return redirect(url_for("choice_seat", flight_id=flight_id, seat_class=seat_class))
        else:
            flash("این صندلی رزرو شده است، لطفا صندلی های دیگر را امتحان کنید", "info")
            return redirect(url_for("choice_seat", flight_id=flight_id, seat_class=seat_class))
        return render_template ("reserve/ticket.html", seat_id=seat_number, seat_class=seat_class, flight_id=flight_id)

    def make_ticket(self, flight_id):
        flight_id=flight_id
        theSeat = seat.Seats.query.filter_by(user_id=current_user.id, flight_id=flight_id).first()
        flight_id = theSeat.flight_id
        airplane_name = theSeat.flight.airplane_name
        seat_id = theSeat.seat_number
        seat_type = theSeat.seat_class
        user_id = current_user.id
        full_name = current_user.full_name
        national_code = current_user.national_code
        phone = current_user.phone
        price = theSeat.flight.economy_price
        newTicket = ticket.Tickets(flight_id=flight_id, airplane_name=airplane_name, seat_id=seat_id, seat_type=seat_type, user_id=user_id, full_name=full_name, national_code=national_code, phone=phone, price=price) 
        db.session.add(newTicket)
        result = db.session.commit()
        theTicket = ticket.Tickets.query.filter_by(national_code=current_user.national_code, flight_id=flight_id).first()
        if result != False:
            flash("بلیط شما با موفقیت صادر شد", "success")
            return render_template ("reserve/make_ticket.html", ticket=theTicket)
        return render_template ("reserve/make_ticket.html", ticket = theTicket)