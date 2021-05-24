import json
from flask import Flask, render_template, request, redirect, url_for, session
# from models import get_users_data, save_file, open_file, update_data_by_post, delete_post, check_password, check_login
from models import filter_post, get_posts_dates, add_new_user, create_user, is_passwords_equal, is_user_in_data, get_users_data, save_file, open_file, update_data_by_post, delete_post, check_password, check_login, create_post
from models import update_posts_id as update_users_id
app = Flask(__name__)

db_name = "database"

app.secret_key = 'super secret key'



@app.route("/", methods=['get', 'post'])
def index():
	# Stwórz stronę 
	if request.method == "GET":
		# print("get")
		pass
	elif request.method == "POST":
		
		# client_login=request.form.get("login")
		# client_password = request.form.get("password")
		
		print("post from index")

	return render_template('index.html')

@app.route("/user_page", methods=['get', 'post'])
def user_page():
	# Stwórz stronę 
	error = None
	valid_password = False
	posts = None
	if request.method == "GET":
		pass
	elif request.method == "POST":

		# get data from the form

		client_login = request.form.get("login")
		client_password = request.form.get("password")
		# get data from the database
		data = open_file(db_name)
		users = data.get('users')
		# check if login in database
		
		user_logins = [d['login'] for d in users]
		
		error = check_login(client_login, user_logins, data, client_password)
		print("error is: ", error)
		if error == None:
			# print("client login from cos tam is: ", client_login)
			current_user = get_users_data(users, client_login)
			# print('user name is: ', current_user.get('name'))
			# print('user posts: ', current_user.get('posts'))
			posts = current_user.get('posts')
			dates = get_posts_dates(current_user)
			print("dates: ", dates)

			session['user_session_login'] = current_user.get('login')
		
			# print(f'user:  posts are: ',_user_login, user_posts)
	if error:
		return render_template('index.html', error=error)
	return render_template('user_page.html', posts=posts, dates=dates)




@app.route("/register", methods=['get', 'post'])
def register():
	data = open_file(db_name)
	users = data.get('users')
	info = None
	success = None
	if request.method == "GET":
		pass
	elif request.method == "POST":
		new_login = request.form.get("login")
		password = request.form.get("password")
		name = request.form.get("name")
		password_conf = request.form.get("password_conf")
		info = is_user_in_data(new_login, data)
		if info == None:
			info = is_passwords_equal(password, password_conf)
		if info == None:
			new_user = create_user(new_login, name, password)
			add_new_user(new_user, data, db_name)
			info = "Brawo, zostales u nas zarejestrowany"
			# update_users_id(users)
			
		# return "posted"
	return render_template("register_page.html", info = info)









@app.route("/logout", methods=['get', 'post'])
def logout():
	return render_template('index.html')

# add new post
@app.route("/user_page/add_post", methods=['get', 'post'])
def add_post():

	if request.method == "GET":
		pass
	elif request.method == "POST":
		new_post = request.form.get('post')

		user_login_from_session = session['user_session_login']
		data_base = open_file(db_name)
		users = data_base.get('users')
		current_users = get_users_data(users, user_login_from_session)

		# post_container = create_post(new_post)
		post_container = "lalala"
		# create_post(new_post)

		# print('user from session: ', user_login_from_session)
		update_data_by_post(data_base, user_login_from_session, new_post, db_name)
		current_user = get_users_data(users, user_login_from_session)
		posts = current_user.get('posts')
		dates = get_posts_dates(current_user)
		# session.clear()
		# print("post to update: ", new_post)
		# update data by new post
		
	return render_template('user_page.html', posts=posts, dates=dates)


@app.route("/user_page/date/<string:day>/")
def show_post_by_date(day):
	print("day: ", day)
	data_base = open_file(db_name)
	users = data_base.get('users')
	user_login_from_session = session['user_session_login']
	current_user = get_users_data(users, user_login_from_session)
	posts = current_user.get('posts')
	dates = get_posts_dates(current_user)
	posts = filter_post(day, posts)
	print("posts: ", posts)
	return render_template("user_page.html", posts=posts, dates=dates)

@app.route("/test/<string:test>/")
def test(test):
	return test


@app.route("/delete/<string:post>/")
def delete(post):
	data_base = open_file(db_name)
	users = data_base.get('users')
	user_login_from_session = session['user_session_login']
	delete_post(data_base, user_login_from_session, post, db_name)
	current_user = get_users_data(users, user_login_from_session)
	posts = current_user.get('posts')
	dates = get_posts_dates(current_user)
	# print("posts: ", posts)
	return render_template('user_page.html', posts = posts, dates=dates)
	# posts = current_user.get('posts').get('post')
	# return render_template('user_page.html', posts=posts)

if __name__ == "__main__":
	app.run()
