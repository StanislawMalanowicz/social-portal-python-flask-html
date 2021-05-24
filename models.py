import json
from time import gmtime, strftime
import time
import datetime
from datetime import date

def open_file(file_name):
    my_file = open(file_name, 'r')
    data = my_file.read()
    data = json.loads(data)
    my_file.close()
    return data

def save_file(file_name, dict_to_save):
    my_file = open(file_name, 'w')
    data_to_json = json.dumps(dict_to_save)
    my_file.write(data_to_json)
    my_file.close()

def get_users_data(users, client_login):
	for user in users:
		# print("user login is: ", user['login'])
		if user['login'] == client_login:
			return user

def check_password(data, login, password):
	users = data.get('users')
	user_to_check = get_users_data(users, login)
	proper_pass = user_to_check.get('password')
	print("from site pass: ", password)
	print("propper pass: ", proper_pass)

	return password == proper_pass
		
def get_posts_dates(user):
	posts = user.get("posts")
	dates = []
	for post in posts:
		if post.get("date") not in dates:
			dates.append(post.get("date"))
	return dates

def filter_post(day, posts):
	filter_posts = []
	if day == "all":
		return posts
	for post in posts:
		if post.get('date') == day:
			filter_posts.append(post)
	return filter_posts

def is_passwords_equal(password, password_conf):
	if len(password) < 4:
		return "Haslo jest za krotkie"
	if password != password_conf:
		return "Hasla nie sa takie same"

def create_user(login, name, password):
	new_user = {
        "login": login,
        "name": name,
		"password": password,
        "posts": [],
    }
	return new_user

def add_new_user(new_user, data, file_name):
	users = data.get('users')
	users.append(new_user)
	update_posts_id(users)
	save_file(file_name, data)

def create_post(post):

	t = time.localtime()
	current_time = time.strftime("%H:%M:%S", t)

	today = date.today()

	day = today.strftime("%d.%m.%Y")
	

	post_content = {
        "post": post,
        "date": day,
        "post_time": current_time,
    }
	print("post content: ", post_content)
	return post_content

def update_posts_id(posts, id=0):
	for post in posts:
		post["id"] = id
		id += 1
	return

def is_user_in_data(login, data):
	users = data.get('users')
	for user in users:
		if user.get("login") == login:
			return "Jest juz taki użytkownik w bazie"
	if len(login) < 3:
		return "Login jest za krótki"


def update_data_by_post(data, login, post, file_name):
	users = data.get('users')
	user_to_update = get_users_data(users, login)
	user_posts = user_to_update.get('posts')
	new_post_content = create_post(post)
	user_posts.append(new_post_content)
	update_posts_id(user_posts)
	
	save_file(file_name, data)

def delete_post(data, login, id, file_name):
	users = data.get('users')
	user_to_update = get_users_data(users, login)
	user_posts = user_to_update.get('posts')
	# delete id from list
	for post_content in user_posts:
		print(id, " is equal to: ", post_content.get('id'), id == post_content.get('id'))
		print("*******************************************")

		if post_content.get('id') == int(id):
			print("znalazlem: ", post_content)
			user_posts.remove(post_content)
			pass
	update_posts_id(user_posts)

	save_file(file_name, data)


def check_login(client_login, user_logins, data, client_password):
			if client_login not in user_logins:
				return f"Nie ma takiego uzytkownika jak {client_login}"
				# check password
			password_valid = check_password(data, client_login, client_password)

			if not password_valid:
				return "Haslo niepoprawne" 

