from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def get_homepage():
	""" Get the homepage """
	projects = hackbright.get_all_projects()
	students = hackbright.get_all_students()
	return render_template("index.html", projects=projects, students=students)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github','jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    projects = hackbright.get_student_projects(github)
    html = render_template("student_info.html",
    						first=first,
    						last=last,
    						github=github,
    						projects=projects)
    return html


@app.route("/student-search")
def get_student_form():
	""" Show form for searching students. """

	return render_template("student_search.html")

@app.route("/add-a-student")
def get_add_form():
	""" Show form for searching students. """

	return render_template("student_add.html")

@app.route("/student-add", methods=['POST'])
def student_add():
	""" Add student from the form. """

	first = request.form.get('fname')
	last = request.form.get('lname')
	github = request.form.get('github')

	hackbright.make_new_student(first, last, github)
    
	return render_template("student_added.html",
    						first=first,
    						last=last,
    						github=github)

@app.route("/project")
def get_project():
	""" Display project info """
	title = request.args.get('title')
	project = hackbright.get_project_by_title(title)
	students = hackbright.get_student_completed_project(title)

	return render_template("project_page.html",
							project=project,
							students=students)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
