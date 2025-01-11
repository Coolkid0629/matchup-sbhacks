from flask import Flask
from models import create_tables
from routes import register_routes

app = Flask(__name__)

# Create database tables
create_tables()

# Register routes
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
