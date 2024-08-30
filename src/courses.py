from flask import (
  Blueprint,
  redirect,
  render_template,
  request,
  url_for,
)
from src.database import get_db

bp = Blueprint("courses", __name__)


@bp.route("/create_course", methods=("GET", "POST"))
def create_course():
  db = get_db()
  group_list = db.execute("SELECT * FROM _group order by created")
  if request.method == "POST":
    name = request.form["name"]
    group_ids = request.form.getlist("group_ids")
    print("this is the group")
    print(group_ids)
    print(request.form.getlist('groups'))
    year1 = request.form["year1"]
    year2 = request.form["year2"]
    if name and group_ids:
      db.execute(
        "INSERT INTO course (name, year1, year2) VALUES (?, ?, ?)",
        (name, year1, year2),
      )
      db.commit()
      course_id = db.execute("SELECT id FROM course WHERE name=? ", (name,)).fetchone()
      for g in group_ids:
        db.execute(
          "INSERT INTO course_group (course_id, group_id) VALUES (?, ?)", (course_id[0], g)
        )
        db.commit()

      return redirect(url_for("courses.courses"))
  return render_template("courses/create_course.html", groupList=group_list)


@bp.route("/courses")
def courses():
  db = get_db()
  my_courses = db.execute(
    "SELECT course.id, course.created, course.name, course.year1, course.year2, "
    "group_concat(_group.name) as groups "
    "FROM(course, course_group, _group) WHERE "
    "course.id = course_group.course_id and _group.id = course_group.group_id "
  ).fetchall()
  return render_template("courses/courses.html", courses=my_courses)


@bp.route("/courses/<c_id>",  methods=("GET", "POST"))
def course_page(c_id):
  db = get_db()
  my_course = db.execute(
    "SELECT * FROM course WHERE id=?", c_id
  ).fetchone()
  students = db.execute(
    "SELECT "
    "course.id, course.name as c_name, course.year1, course.year2, _group.name as g_name, _group.is_gm, "
    "student.id as st_id, student.name as st_name, student.surname "
    "FROM(course, course_group, _group, student_group, student) "
    "WHERE "
    "course.id = course_group.course_id and _group.id = course_group.group_id and "
    "_group.id = student_group.group_id and student_group.student_id = student.id"
  ).fetchall()
  tabs = db.execute("SELECT * from tab;").fetchall()
  columns = db.execute("SELECT * from tab_column").fetchall()
  events = db.execute("SELECT * from event")
  events_type = db.execute("SELECT * from event_type")
  if request.method == "POST":
    if request.form['submit_button'] == 'add_column':
      _add_event(request.form, db)
    elif request.form['submit_button'] == 'something_else':
      pass  # do something else
    else:
      pass  # unknown
  return render_template("courses/course_template.html",
                         course=my_course, students=students,
                         tabs=list(tabs), events_type=events_type,
                         columns=columns)


def _add_event(_form, _db):
  tab_id = _form['tab_id']
  course_id = _form['course_id']
  name = _form['name']
  event_type = _form['event_type']
  my_type = _db.execute("SELECT * FROM event_type WHERE name=?", (event_type,)).fetchone()
  _db.execute("""INSERT INTO tab_column (tab_id, course_id, type_id, name)
  VALUES (?, ?, ?, ?)""", (tab_id, course_id, my_type['id'], name))
  _db.commit()
