from schema import factory, User
from flask import Flask, request, render_template, redirect


app = Flask(__name__)


@app.route('/')
@app.route('/index')
def show_all_users():
    result = session.query(User)
    return render_template('all users.html', users=result)


@app.route('/add-user')
def add_new_user():
    return render_template('registration.html')


@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = session.query(User).get(user_id)
    if request.method == 'GET':
        return render_template('edit_user.html', user=user)
    elif request.method == 'POST':
        user.first_name = request.form.get('name')
        user.last_name = request.form.get('surname')
        user.email = request.form.get('email')
        user.username = request.form.get('username')
        user.password = request.form.get('pwd')
        try:
            session.commit()
            return redirect("/index")
        except Exception as e:
            session.rollback()
            return f"Failed to update user: {e}"


@app.route('/user-reg', methods=['POST'])
def user_form():
    u = User()
    u.first_name = request.form["name"]
    u.last_name = request.form["surname"]
    u.email = request.form["email"]
    u.username = request.form["username"]
    u.password = request.form["pwd"]
    confirm_pwd = request.form["confirm_pwd"]

    if u.password != confirm_pwd:
        return "Подтверждение пароля не совпадает"

    try:
        session.add(u)
        session.commit()
        return redirect("/index")
    except Exception as e:
        session.rollback()
        return f"Failed: {e}"


@app.route('/user-log', methods=['GET', 'POST'])
def user_log_in():
    if request.method == "GET":
        return render_template('log_in.html')
    else:
        user_username = session.query(User).filter(User.username == request.form["username"]).first()
        if user_username is None:
            return "Username is not found"
        elif request.form["pwd"] == user_username.password:
            return "Success"
        else:
            return "Wrong password"


if __name__ == "__main__":
    session = factory()
    app.run(host="127.0.0.1", port=4322)

