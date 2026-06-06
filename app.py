from flask import Flask
from flask_login import LoginManager

from os import getenv
from functools import partial

from extensions import db

app = Flask(__name__)

app.config['ENV'] = getenv('FLASK_ENV', 'development')  # پیش‌فرض: development
if app.config['ENV'] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

login = LoginManager()
login.login_view = "signin"
login.login_message_category = "danger"
login.init_app(app)

db.init_app(app)
from models import airplane, flight, ticket, user, seat

from controller import home, admin, auth, users, reservatrion
homeController = home.Home()
adminController = admin.Admin()
userController = users.Member()
authController = auth.Authentication()
reservationController = reservatrion.Reservation()

@login.user_loader
def userLoader(user_id):
    return user.Users.query.get(user_id)

# -----Routs-----
app.add_url_rule("/", "main", partial(homeController.main))
app.add_url_rule("/admin", "admin_home", partial(adminController.admin_home))

# Authentication
app.add_url_rule("/auth/register", "register", partial(authController.register), methods = ["get","post"])
app.add_url_rule("/auth/login", "signin", partial(authController.signin), methods = ["get","post"])
app.add_url_rule("/auth/signout", "signout", partial(authController.signout))

# Account Dashboard
app.add_url_rule("/account", "account", partial(userController.account))
app.add_url_rule("/account/profile", "account_info", partial(userController.account_info))
app.add_url_rule("/account/wallet", "wallet_increase", partial(userController.wallet_increase), methods = ["get","post"])
app.add_url_rule("/account/ticket/delete", "del_ticket", partial(userController.del_ticket), methods = ["get","post"])

# =====ADMIN PANNEL=====
#Airplanes Dashboard
app.add_url_rule("/admin/add-airplane", "add_airplane", partial(adminController.add_airplane), methods = ["get","post"])
app.add_url_rule("/admin/airplanes-list", "get_all_airplanes", partial(adminController.get_all_airplanes), methods = ["get","post"])
app.add_url_rule("/admin/edit-airplane", "edit_airplane", partial(adminController.edit_airplane), methods = ["get","post"])

#Flights Dashboard
app.add_url_rule("/admin/add-flight", "add_flight", partial(adminController.add_flight), methods = ["get","post"])
app.add_url_rule("/admin/flights-list", "get_all_flights", partial(adminController.get_all_flights), methods = ["get","post"])
app.add_url_rule("/admin/edit-flight", "edit_flight", partial(adminController.edit_flight), methods = ["get","post"])

# Users Dashboard
app.add_url_rule("/admin/users-list", "get_all_users", partial(adminController.get_all_users), methods = ["get","post"])
app.add_url_rule("/admin/edit-user", "edit_user", partial(adminController.edit_user), methods = ["get","post"])

# Sales Report and Seats Status
app.add_url_rule("/admin/sales-profit", "sales_profit", partial(adminController.sales_profit))
app.add_url_rule("/admin/seats-status", "reservation_list", partial(adminController.reservation_list), methods = ["get", "post"])

# =====END ADMIN PANNEL=====

# Reservation
app.add_url_rule("/reserve/flights/<string:seat_class>", "reserve_main", partial(reservationController.reserve_main), methods = ["get","post"])
app.add_url_rule("/reserve/<int:flight_id>/seats/<string:seat_class>", "choice_seat", partial(reservationController.choice_seat), methods = ["get","post"])
app.add_url_rule("/reserve/make", "make_reservation", partial(reservationController.make_reservation), methods = ["post"])
app.add_url_rule("/reserve/ticket/<int:flight_id>", "make_ticket", partial(reservationController.make_ticket), methods = ["post", "get"])



if __name__ == "__main__":
    app.run()