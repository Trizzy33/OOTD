from .settings import *
from .views.main_view import main
from .views.auth import auth

app.register_blueprint(main)
app.register_blueprint(auth)
