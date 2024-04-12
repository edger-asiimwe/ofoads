import os 

from ofoads_app import init_app, db
from ofoads_app.models import User

app = init_app()

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get("PORT"))