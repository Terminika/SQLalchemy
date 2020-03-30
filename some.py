@app.route('/')
def index():
    db_session.global_init("db/mars_explorer.sqlite")
    session = db_session.create_session()
    leaders = []
    for i in session.query(Jobs).all():
        leaders.append(session.query(User).filter(User.id == i.team_leader).first())
    jobs = session.query(Jobs).all()
    session.commit()
    return render_template('index.html', jobs=jobs, leaders=leaders)


if __name__ == '__main__':
    app.debug = True
    app.run(port=5000, host='127.0.0.1')