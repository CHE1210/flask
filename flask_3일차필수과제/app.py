from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api, Blueprint
from flask.views import MethodView
from marshmallow import Schema, fields

# 앱 및 DB 설정
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0000@localhost/oz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.1.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
db = SQLAlchemy(app)
api = Api(app)

# ----------------------- 모델 -----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text)

# ----------------------- 스키마 -----------------------
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Str(required=True)

class BoardSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str()

# ----------------------- 블루프린트 -----------------------
user_blp = Blueprint("users", "users", url_prefix="/users", description="User operations")
board_blp = Blueprint("boards", "boards", url_prefix="/boards", description="Board operations")

@user_blp.route("/")
class UserList(MethodView):
    @user_blp.response(200, UserSchema(many=True))
    def get(self):
        return User.query.all()

    @user_blp.arguments(UserSchema)
    @user_blp.response(201, UserSchema)
    def post(self, data):
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

@board_blp.route("/")
class BoardList(MethodView):
    @board_blp.response(200, BoardSchema(many=True))
    def get(self):
        return Board.query.all()

    @board_blp.arguments(BoardSchema)
    @board_blp.response(201, BoardSchema)
    def post(self, data):
        board = Board(**data)
        db.session.add(board)
        db.session.commit()
        return board

# ----------------------- API 등록 -----------------------
api.register_blueprint(user_blp)
api.register_blueprint(board_blp)

# ----------------------- HTML 라우트 -----------------------
@app.route("/manage-users")
def manage_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/manage-boards")
def manage_boards():
    boards = Board.query.all()
    return render_template("boards.html", boards=boards)

# ----------------------- 실행 -----------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)