import logging
from flask import render_template
from sqlalchemy.orm import contains_eager
from app import app, db
from models import Subject, SubjectTree, Work, Artist

log = logging.getLogger(__name__)

@app.route('/truculent/<word>')
def slowmatch(word):
    pat = "%{}%".format(word)

    artists_sq = Artist.query.join(Artist.works).join(Work.subjects).join(SubjectTree.subject)
    artists_sq = artists_sq.options(contains_eager(Artist.works).contains_eager(Work.subjects).contains_eager(SubjectTree.subject))
    artists_sq = artists_sq.filter(Subject.name.like(pat))

    artists_q = Artist.query.join(Artist.works).join(Work.subjects).join(SubjectTree.subject).join(Artist.movements)
    artists_q = artists_q.options(
        contains_eager(Artist.works).
        contains_eager(Work.subjects).
        contains_eager(SubjectTree.subject).
        contains_eager(Artist.movements)
    )
    #artists = artists_q.all()
    log.warn("Artists retrieved: %d", len(artists))
    return render_template('truculent.html', artists=artists)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
