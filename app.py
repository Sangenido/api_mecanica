from flask import Flask
from flasgger import Swagger
from controllers.agendamento_controller import agendamentos_bp

app = Flask(__name__)
app.json.ensure_ascii = False
Swagger(app)
app.register_blueprint(agendamentos_bp)

if __name__ == "__main__":
    app.run(debug=True)