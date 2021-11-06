from .settings import *
from .views.main_view import main

app.register_blueprint(main)