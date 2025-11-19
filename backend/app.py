from flask import Flask, jsonify
from flask_security import Security
from flask_restful import Api

from controllers.database import db
from controllers.config import Config
from controllers.user_datastore import user_datastore





def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    security = Security(app, user_datastore)

    api = Api(app, prefix="/api")

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name = 'admin', description = 'Administrator')
        user_role = user_datastore.find_or_create_role(name = 'user', description = 'Regular User')

        if not user_datastore.find_user(email = "admin@gmail.com"):
            user_datastore.create_user(
                email = "admin@gmail.com",
                username = "admin",
                password = "admin",
                roles = [admin_role]
            )

        db.session.commit()

    return app, api

app, api = create_app()



from controllers.authentication_apis import LoginAPI, LogoutAPI
api.add_resource(LoginAPI, "/login")
api.add_resource(LogoutAPI, "/logout")



if __name__ == "__main__":
    app.run(debug=True)


