from flask import Blueprint, redirect, request
from OOTD.settings import *

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/')
def page():
    return "<h1>Authentication</h1>"