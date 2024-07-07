from app import create_app
from app.validusers import add_sample_users

if __name__ == '__main__':
    app = create_app()
    # with app.app_context():
    #     add_sample_users()
    app.run(debug=True)
