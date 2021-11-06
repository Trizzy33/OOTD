from flask import Blueprint, redirect, request
from OOTD.settings import *

main = Blueprint('main', __name__)

@main.route('/')
def page():
    return "<h1>Hello World!</h1>"