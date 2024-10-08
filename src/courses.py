import pandas
import pandas as pd
from flask import (
  Blueprint,
  redirect,
  render_template,
  request,
  url_for,
  jsonify
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
    """SELECT course.id, course.created, course.name, course.year1, course.year2, 
       group_concat(_group.name) AS groups 
       FROM course
       JOIN course_group ON course.id = course_group.course_id
       JOIN _group ON _group.id = course_group.group_id
       GROUP BY course.id, course.created, course.name, course.year1, course.year2
       HAVING COUNT(*) > 0;
    """).fetchall()
  return render_template("courses/courses.html", courses=my_courses)


@bp.route("/courses/<c_id>")
def course_page(c_id):
  db = get_db()
  my_course = db.execute(
    "SELECT * FROM course WHERE id=?", (c_id,)
  ).fetchone()
  tabs = db.execute("SELECT * from tab;").fetchall()
  event_dict = {}
  for tab in [row['id'] for row in tabs]:
    event_dict[tab] = get_events(c_id, tab)
  columns = db.execute("SELECT * from tab_column WHERE course_id=?", (c_id,)).fetchall()
  events_type = db.execute("SELECT * from event_type")
  return render_template("courses/course_template.html", course=my_course,
                         tabs=list(tabs), events_type=events_type, events=event_dict,
                         columns=columns)


@bp.route("/courses/api/<c_id>", methods=["POST"])
def add_event_column(c_id):
  json_data = request.get_json()
  db = get_db()
  tab_id = json_data['tab_id']
  name = json_data['name']
  event_type = json_data['event_type']
  my_type = db.execute("SELECT * FROM event_type WHERE name=?", (event_type,)).fetchone()
  db.execute("""INSERT INTO tab_column (tab_id, course_id, type_id, name)
    VALUES (?, ?, ?, ?)""", (tab_id, c_id, my_type['id'], name))
  db.commit()
  tab_column_id = db.execute("""SELECT * FROM tab_column WHERE tab_id=? and course_id=? and type_id=? 
                and name=?""", (tab_id, c_id, my_type['id'], name)).fetchone()['id']
  students = _get_student_list_to_pandas(db, c_id)['st_id'].to_list()
  for st in students:
    db.execute("""INSERT INTO event (student_id, tab_column_id, event_type_id, value_int)
               VALUES (?, ?, ?, ?)""", (st, tab_column_id, 2, 4))
    db.commit()
  return jsonify(json_data), 201


def get_events(c_id, t_id) -> pd.DataFrame:
  db = get_db()
  students = _get_student_list_to_pandas(db, c_id)
  exercises_list = _get_tasks_list_to_pandas(db, c_id, t_id)
  student_ids = students['st_id'].to_list()
  column_ids = exercises_list['id'].to_list()
  events = _get_events_list_to_pandas(db, student_ids, column_ids)
  students.index = students['st_id']
  return pd.concat([students, events], axis=1)


@bp.route('/courses/api/<c_id>/<t_id>')
def get_table(c_id, t_id):
  result = get_events(c_id, t_id)
  return jsonify(result.to_dict('index'))


@bp.route('/courses/api/update_event/<ev_id>', methods=['PUT'])
def update(ev_id):
  db = get_db()
  json_data = request.get_json()
  dict_data = dict(json_data)
  print(dict_data)
  query = """UPDATE event SET value_int = ?  WHERE id=?"""
  print(query)
  print(dict_data['value'], dict_data['event_id'])
  db.execute(query, (dict_data['value'], dict_data['event_id']))
  db.commit()
  return jsonify("true")


def _get_student_list(_db, _c_id):
  return _db.execute(
    "SELECT "
    "course.id, course.name as c_name, course.year1, course.year2, _group.name as g_name, _group.is_gm, "
    "student.id as st_id, student.name as st_name, student.surname "
    "FROM(course, course_group, _group, student_group, student) "
    "WHERE course.id = ? and "
    "course.id = course_group.course_id and _group.id = course_group.group_id and "
    "_group.id = student_group.group_id and student_group.student_id = student.id", (_c_id,)
  ).fetchall()


def _get_student_list_to_pandas(_db, _c_id):
  sql_query = """SELECT
                 course.id, course.name as c_name, course.year1, course.year2, 
                 _group.name as g_name, _group.is_gm, 
                 student.id as st_id, student.name as st_name, student.surname 
                 FROM(course, course_group, _group, student_group, student) 
                 WHERE course.id = ? and 
                 course.id = course_group.course_id and _group.id = course_group.group_id and 
                _group.id = student_group.group_id and student_group.student_id = student.id
              """
  params = [_c_id]
  return pd.read_sql_query(sql_query, _db, params=params)


def _get_tasks_list(_db, _c_id, _t_id):
  return _db.execute("""SELECT * from tab_column WHERE 
                        tab_id=? AND course_id=?""", (_t_id, _c_id)).fetchall()


def _get_tasks_list_to_pandas(_db, _c_id, _t_id):
  sql_query = """SELECT * from tab_column WHERE 
                        tab_id=? AND course_id=?"""
  params = [_c_id, _t_id]
  return pd.read_sql_query(sql_query, _db, params=params)


def _get_events_list_to_pandas(_db, _student_ids, _column_ids):
  query = """SELECT event.id as event_id, event.tab_column_id, event.student_id,  
             event.value_int, tab_column.name FROM 
             event, tab_column WHERE event.tab_column_id=tab_column.id AND 
             student_id IN ({seq_st}) 
             AND tab_column_id IN ({seq_col})""".format(
    seq_st=','.join(['?'] * len(_student_ids)),
    seq_col=','.join(['?'] * len(_column_ids)))

  df = pd.read_sql_query(query, _db, params=_student_ids + _column_ids)
  df = pandas.pivot(df, index="student_id", columns="name",
                    values=["value_int", "event_id"])
  df = df.rename_axis()
  return df


def _get_events_list(_db, _student_ids, _column_ids):
  query = """SELECT event.id, 
             event.tab_column_id, event.student_id, event.value_real, 
             event.value_int, event.value_text, tab_column.name FROM 
             event, tab_column WHERE event.tab_column_id=tab_column.id AND 
             student_id IN ({seq_st}) 
             AND tab_column_id IN ({seq_col})""".format(
    seq_st=','.join(['?'] * len(_student_ids)),
    seq_col=','.join(['?'] * len(_column_ids)))
  return _db.execute(query, _student_ids + _column_ids).fetchall()
