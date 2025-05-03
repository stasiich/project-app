from flask import Flask, render_template, request, redirect, url_for, session, flash
from models.user import User
from models.course import Course
from models.skill_request import SkillRequest


app = Flask(__name__)
app.secret_key = 'secret-key'

users = []
courses_list = []
skill_requests = []


@app.route('/')
def home():
    return render_template('main.html')

@app.route('/courses')
def courses():
    user_email = session.get('user')
    if not user_email:
        flash('Please log in to access courses.', 'warning')
        return redirect(url_for('login'))

    return render_template('courses.html', courses=courses_list)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = next((user for user in users if user.authenticate(email, password)), None)

        if user:
            session['user'] = {'name': user.name, 'email': user.email}
            flash('Login successful!', 'success')
            return redirect(url_for('home'))

        flash('Invalid credentials.', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User.register(name, email, password, users)

        if new_user:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email already registered.', 'danger')
    return render_template('register.html')
@app.route('/create-course', methods=['GET', 'POST'])
def create_course():
    user_email = session.get('user')
    if not user_email:
        flash('Please log in to access courses.', 'warning')
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        creator_email = session['user']['email']
        new_course = Course(title, description, creator_email)

        courses_list.append(new_course)
        flash('Course created successfully!', 'success')
        return redirect(url_for('courses'))

    return render_template('create_course.html')

@app.route('/course/<int:course_id>', methods=['GET', 'POST'])
def course_detail(course_id):
    course = next((c for c in courses_list if c.id == course_id), None)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('courses'))

    user_email = session.get('user', {}).get('email')

    # Handle review form submission
    if request.method == 'POST' and 'rating' in request.form and user_email and user_email != course.creator_email:
        try:
            rating = int(request.form['rating'])
            comment = request.form['comment']
            course.add_review(rating, comment)
            flash('Review submitted successfully!', 'success')
            return redirect(url_for('course_detail', course_id=course.id))
        except (ValueError, KeyError):
            flash('Invalid form submission.', 'danger')

    # Handle hire skill request form submission
    if request.method == 'POST' and 'hire_message' in request.form and user_email and user_email != course.creator_email:
        hire_message = request.form['hire_message']
        new_request = SkillRequest(
            from_email=user_email,
            to_email=course.creator_email,
            course_title=course.title,
            message=hire_message
        )
        skill_requests.append(new_request)
        flash('Your request has been sent to the course creator!', 'success')
        return redirect(url_for('course_detail', course_id=course.id))

    return render_template('course_detail.html', course=course, user_email=user_email)




@app.route('/profile')
def profile():
    user = session.get('user')
    if not user:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('login'))

    # Get courses created by this user
    user_courses = [c for c in courses_list if c.creator_email == user['email']]

    # Get skill hire requests sent to this user
    user_requests = [r for r in skill_requests if r.to_email == user['email']]

    return render_template('profile.html', user=user, user_courses=user_courses, user_requests=user_requests)



@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
