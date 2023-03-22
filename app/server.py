from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from worker import countWordsTask, celery_app
from celery.result import AsyncResult

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/tasks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Tasks(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)



@app.route("/count", methods=["POST"])
def count():
    text = request.get_json()['text']
    result = countWordsTask.delay(text)
    print(result)
    # res = AsyncResult(id, app=celery_app)
    # newEntry = Tasks(result.id, text, res)
    # db.session.add(newEntry)
    # db.session.commit()
    return str(result.id)

@app.route("/status/<id>", methods=["GET"])
def getStatus(id):
    res = AsyncResult(id, app=celery_app)
    if res.status == "SUCCESS":
        count = res.get()
        return str(count)
    return str(-1)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

