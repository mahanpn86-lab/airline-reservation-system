from extensions import db
from models import airplane, flight, user, seat, ticket
from flask import render_template, redirect, url_for, request, flash, abort, current_app
from flask_login import current_user, login_required
from sqlalchemy import update
from validators.admin import AddAirplane, EditAirplane, AddFlight, EditFlight
from validators.auth import EditUser
from datetime import datetime, time, timedelta

class Admin:
    def __init__(self, *args, **kwargs):
        pass

    @login_required
    def admin_home(self):
        if not current_user.admin:
            return redirect(url_for("account"))
        return render_template("admin/index.html")

    def add_airplane(self):
        form = AddAirplane()
        if request.method == "POST":
            if form.validate_on_submit():
                name = request.form.get("name")
                capacity_economy = request.form.get("capacity_economy")
                capacity_business = request.form.get("capacity_business")
                capacity_vip = request.form.get("capacity_vip")
                Airplane = airplane.Airplanes.query.filter_by(name = name).first()
                if not Airplane:
                    newAirplane = airplane.Airplanes(name=name, capacity_economy=capacity_economy, capacity_business=capacity_business, capacity_vip=capacity_vip)
                    db.session.add(newAirplane)
                    result = db.session.commit()
                    if result != False:
                        flash("هواپیمای جدید با موفقیت ساخته شد", "success")
                        return redirect(url_for("add_airplane"))
                else:
                    flash("هواپیمایی با این مشخصات از قبل دارد لطفا هواپیمای جدیدی را اضافه کنید", "info")
                    return redirect(url_for("add_airplane"))
        return render_template ("admin/airplane/create.html", form = form)

    def get_all_airplanes(self):
        if request.method == "POST":
            db.session.query(airplane.Airplanes).filter_by(id = request.args.get("id")).delete()
            db.session.commit()
            return redirect(url_for("get_all_airplanes"))
        get_all_airplane = airplane.Airplanes.query.all()
        return render_template("/admin/airplane/list.html", airplanes = get_all_airplane)

    def edit_airplane(self):
        form = EditAirplane()
        Airplane = db.session.query(airplane.Airplanes).filter_by(id=request.args.get("id")).one()
        if request.method == "POST":
            name = request.form.get("name")
            capacity_economy = request.form.get("capacity_economy")
            capacity_business = request.form.get("capacity_business")
            capacity_vip = request.form.get("capacity_vip")
            Airplane.name = name
            Airplane.capacity_economy = capacity_economy
            Airplane.capacity_business = capacity_business
            Airplane.capacity_vip = capacity_vip
            db.session.add(Airplane)
            db.session.commit()
            return redirect(url_for("get_all_airplanes"))
        return render_template("/admin/airplane/edit.html", form=form, airplane=Airplane)

    def add_flight(self):
        form = AddFlight()
        all_airplanes = airplane.Airplanes.query.all()
        if request.method == "POST":
            if form.validate_on_submit():
                airplane_id = request.form.get("airplane_id")

                last_flight = flight.Flights.query.filter_by(airplane_id=airplane_id).order_by(flight.Flights.arrival_date.desc(), flight.Flights.arrival_time.desc()).first()
                if last_flight:
                    last_arrival = datetime.combine(last_flight.arrival_date,last_flight.arrival_time)
                    if datetime.now() < last_arrival + timedelta(hours=1):
                        flash("این هواپیما هنوز در بازه‌ی استراحت (کمتر از ۱ ساعت از آخرین پرواز) است", "danger")
                        return redirect(url_for("add_flight"))
                selected_airplane = airplane.Airplanes.query.filter_by(id=airplane_id).first()
                airplane_name = selected_airplane.name
                origin = request.form.get("origin")
                destination = request.form.get("destination")
                departure_time = request.form.get("departure_time")
                arrival_time = request.form.get("arrival_time")
                departure_time_obj = datetime.strptime(departure_time, '%H:%M').time()
                arrival_time_time_obj = datetime.strptime(arrival_time, '%H:%M').time()
                arrival_date = request.form.get("arrival_date")
                departure_date = request.form.get("departure_date")
                arrival_date_obj = datetime.strptime(arrival_date, "%Y-%m-%d").date()
                departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()
                economy_price = request.form.get("economy_price")
                business_price = request.form.get("business_price")
                vip_price = request.form.get("vip_price")
                newFlight = flight.Flights(airplane_id=airplane_id,airplane_name=airplane_name , origin=origin, destination=destination, departure_time=departure_time_obj, arrival_time=arrival_time_time_obj, departure_date=departure_date_obj, arrival_date=arrival_date_obj, economy_price=economy_price, business_price=business_price, vip_price=vip_price)
                db.session.add(newFlight)
                result = db.session.commit()
                if result != False:
                    flash("پزواز با موفقیت ایجاد شد", "success")
                    return redirect(url_for("add_flight"))
        return render_template ("admin/flight/create.html", form = form, airplanes = all_airplanes)

    def get_all_flights(self):
        if request.method == "POST":
            flight_id = request.args.get("id")
            theSeats = seat.Seats.query.filter_by(flight_id = flight_id).all()
            theFlight = flight.Flights.query.filter_by(id = flight_id).first()
            for theSeat in theSeats:
                theUser = user.Users.query.filter_by(id = theSeat.user_id).first()
                if theSeat.seat_class == "economy":
                    theUser.wallet += theFlight.economy_price
                if theSeat.seat_class == "business":
                    theUser.wallet += theFlight.business_price
                if theSeat.seat_class == "vip":
                    theUser.wallet += theFlight.vip_price
            db.session.query(flight.Flights).filter_by(id = flight_id).delete()
            db.session.query(seat.Seats).filter_by(flight_id = flight_id).delete()
            db.session.query(ticket.Tickets).filter_by(flight_id = flight_id).delete()
            db.session.commit()
            return redirect(url_for("get_all_flights"))
        get_all_flights = flight.Flights.query.all()
        return render_template("/admin/flight/list.html", flights = get_all_flights)

    def edit_flight(self):
        form = EditFlight()
        myFlight = db.session.query(flight.Flights).filter_by(id=request.args.get("id")).first()
        if request.method == "POST":
            flight_id = request.form.get("id")
            myFlight = db.session.get(flight.Flights, flight_id)
            airplane_id = request.form.get("airplane_id")
            selected_airplane = airplane.Airplanes.query.filter_by(id=airplane_id).first()
            airplane_name = selected_airplane.name
            origin = request.form.get("origin")
            destination = request.form.get("destination")
            departure_time = request.form.get("departure_time")
            arrival_time = request.form.get("arrival_time")
            # departure_time_obj = datetime.strptime(departure_time, '%H:%M').time()
            # arrival_time_obj = datetime.strptime(arrival_time, '%H:%M').time()
            departure_time_obj = time.fromisoformat(departure_time)
            arrival_time_obj = time.fromisoformat(arrival_time)
            arrival_date = request.form.get("arrival_date")
            departure_date = request.form.get("departure_date")
            arrival_date_obj = datetime.strptime(arrival_date, "%Y-%m-%d").date()
            departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()
            economy_price = request.form.get("economy_price")
            business_price = request.form.get("business_price")
            vip_price = request.form.get("vip_price")
            # Edit Flight
            myFlight.airplane_id = airplane_id
            myFlight.airplane_name= airplane_name
            myFlight.origin = origin
            myFlight.destination = destination
            myFlight.departure_time = departure_time_obj
            myFlight.departure_date = departure_date_obj
            myFlight.arrival_time = arrival_time_obj
            myFlight.arrival_date = arrival_date_obj
            myFlight.economy_price = economy_price
            myFlight.business_price = business_price
            myFlight.vip_price = vip_price
            db.session.add(myFlight)
            db.session.commit()
            return redirect(url_for("get_all_flights"))
        get_all_airplanes = airplane.Airplanes.query.all()
        return render_template("/admin/flight/edit.html", form=form, flight=myFlight, airplanes=get_all_airplanes)

    def get_all_users(self):
        if request.method == "POST":
            db.session.query(user.Users).filter_by(id = request.args.get("id")).delete()
            db.session.commit()
            return redirect(url_for("get_all_users"))
        get_all_users = user.Users.query.all()
        return render_template("/admin/user/list.html", users = get_all_users)

    def edit_user(self):
        form = EditUser()
        myUser = db.session.query(user.Users).filter_by(id=request.args.get("id")).first()
        if request.method == "POST":
            user_id = request.form.get("id")
            myUser = db.session.get(user.Users, user_id)
            full_name = request.form.get("full_name")
            national_code = request.form.get("national_code")
            phone = request.form.get("phone")
            wallet = request.form.get("wallet")
            admin = request.form.get("admin")
            # Edit Flight
            myUser.full_name = full_name
            myUser.national_code = national_code
            myUser.phone = phone
            myUser.wallet = wallet
            myUser.admin = bool(int(form.admin.data))
            db.session.add(myUser)
            db.session.commit()
            return redirect(url_for("get_all_users"))
        return render_template("/admin/user/edit.html", form=form, user=myUser)

    def sales_profit(self):
        all_flights = flight.Flights.query.all()
        economy_profits = []
        business_profits = []
        vip_profits = []
        economy_profit = 0
        business_profit = 0
        vip_profit = 0
        for theFlight  in all_flights:
            economy_profit = theFlight.economy_passengers * theFlight.economy_price
            business_profit = theFlight.business_passengers * theFlight.business_price
            vip_profit = theFlight.vip_passengers * theFlight.vip_price
            economy_profits.append(economy_profit)
            business_profits.append(business_profit)
            vip_profits.append(vip_profit)
        profits = {"economy_profits" : economy_profits, "business_profits" : business_profits, "vip_profits" : vip_profits}
        return render_template("admin/sales_report.html", flights=all_flights, profits=profits)

    def reservation_list(self):
        if request.method == "GET":
            return render_template("admin/reservation_list.html", flight=None, type=None, capacity=0)
        flight_id = request.form.get("flight_id")
        theFlight = flight.Flights.query.filter_by(id = flight_id).first()
        if theFlight is None:
            flash("هیچ پروازی با این شناسه یافت نشد", "danger")
            return redirect(url_for("reservation_list"))
        type = request.form.get("type")
        type = type.lower()
        if type not in ["economy","business","vip"]:
            flash("نوع سالن را به درستی وارد کنید (economy, business, vip)", "danger")
            return redirect(url_for("reservation_list"))
        seats = seat.Seats.query.filter_by(flight_id=flight_id).all()
        booked_seat_numbers = [s.seat_number for s in seats if s.is_booked]
        return render_template("admin/reservation_list.html", flight=theFlight, type=type, booked_seat_numbers=booked_seat_numbers)