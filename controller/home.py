from flask import Flask, render_template, redirect, url_for, request, flash, abort
from extensions import db

class Home:
    def __init__(self, *args, **kwargs):
        pass
    
    def main(self):
        return render_template("home.html")
    



