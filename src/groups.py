import re
import os
import sys
from flask import (
  Blueprint,
  redirect,
  render_template,
  request,
  url_for,
  jsonify
)
import pandas as pd
from src.database import get_db

bp = Blueprint("groups", __name__)
os.system('export PYTHONHASHSEED=0')


@bp.route("/create_group", methods=("GET", "POST"))
def create_group():
  if request.method == "POST":

    level = request.form["level"]
    linea = request.form["linea"]
    is_gm = (request.form["is_gm"] == "1")
    year1 = request.form['year1']
    year2 = request.form['year2']
    name = level + linea + '_' + year1[2:] + year2[2:]
    filetype = request.form['filetype']
    file = request.files['file']
    if name and file and _allowed_file(file.filename):
      db = get_db()
      db.execute("""INSERT INTO _group 
                 (_level, linea, name, year1, year2, is_gm) VALUES (?, ?, ?, ?, ?, ?)""",
                 (level, linea, name, year1, year2, is_gm)
                 )
      db.commit()
      df = pd.DataFrame()

      student_ids = []
      if filetype == 'r':
        df = pd.read_csv(file.stream, encoding='ISO-8859-1')
        student_ids = insert_student_list_raices(df, db)
      elif filetype == 'm':
        df = pd.read_csv(file.stream, encoding='utf-8')
        student_ids = insert_student_list_moodle(df, db)
      elif filetype == "f":
        insert_student_list_jefatura(df, db)
      else:
        pass
      my_group = db.execute("SELECT * FROM _group WHERE name=?", (name,)).fetchone()
      for _id in student_ids:
        db.execute(
          "INSERT INTO student_group (student_id, group_id) VALUES (?, ?)",
          (_id, my_group['id']))
        db.commit()
      return redirect(url_for("groups.groups"))
  return render_template("groups/create_group.html")


@bp.route("/groups")
def groups():
  db = get_db()
  my_groups = db.execute(
    "SELECT * FROM _group ORDER BY created DESC"
  ).fetchall()
  return render_template("groups/groups.html", groups=my_groups)


@bp.route("/groups/api/delete/<group_id>", methods=["POST"])
def delete_group(group_id):
  db = get_db()

  query_lst = [
    """DELETE FROM student WHERE id IN 
        (SELECT student_id FROM student_group WHERE group_id=?)""",
    """DELETE FROM student_group WHERE group_id=?""",
    """DELETE FROM _group WHERE id=?""",
    """DELETE FROM event WHERE student_id IN 
         (SELECT student_id FROM student_group WHERE group_id=?)"""
  ]
  for query in query_lst:
    db.execute(query, group_id)
  print(query_lst)
  db.commit()

  return jsonify("true")


@bp.route("/groups/<iden>")
def group_page(iden):
  db = get_db()
  my_group = db.execute(
    "SELECT * FROM _group WHERE id=?", iden
  ).fetchone()
  print(my_group['name'])
  _ids = db.execute(
    "SELECT student_id FROM student_group WHERE group_id=?", iden
  ).fetchall()
  my_ids = []
  for _id in _ids:
    my_ids.append(_id[0])
  print(_ids)
  sql = "SELECT * FROM student WHERE id in ({seq})".format(
    seq=','.join(['?'] * len(my_ids)))
  my_students = db.execute(sql, my_ids).fetchall()
  return render_template("groups/groups_template.html", name=my_group['name'],
                         students=my_students)


def insert_student_list_raices(_df, _db):
  dfout = _process_student_list_raices(_df)
  ids = dfout['id'].tolist()
  double_entry = _sanity_check(dfout, _db)
  dfout = _drop_entries(double_entry, dfout)
  dfout.to_sql('student', _db, if_exists='append', index=False)
  return ids


def insert_student_list_moodle(_df, _db):
  dfout = _process_student_list_moodle(_df)
  ids = dfout['id'].tolist()
  double_entry = _sanity_check(dfout, _db)
  dfout = _drop_entries(double_entry, dfout)
  dfout.to_sql('student', _db, if_exists='append', index=False)
  return ids


def insert_student_list_jefatura(_df, _db):
  pass


def _drop_entries(double_entry, dfout):
  if len(double_entry):
    print("No se pudieron procesar los datos de los alumnos con los siguientes id's")
    print(double_entry)
    for de in double_entry:
      dfout.drop(dfout[dfout.id == de].index, inplace=True)
  return dfout


def _process_student_list_raices(_df):
  column_names = ["tutor_email", "telephone1", "telephone2"]
  print(_df.columns)
  _df.columns = _df.columns[:2].tolist() + column_names
  _df['name'] = _df['Alumno'].apply(_get_name)
  _df['surname'] = _df['Alumno'].apply(_get_surname)
  _df['id'] = _df.apply(_get_hash, axis=1)
  del _df['Alumno']
  return _df


def _process_student_list_moodle(df):
  del df['Grupos']
  column_names = ["name", "surname", "email"]
  df.columns = column_names
  df['id'] = df.apply(_get_hash, axis=1)
  return df


def _sanity_check(df, c):
  existing_students = []
  for _id in df['id']:
    output = c.execute("SELECT * FROM student WHERE id=?", (_id,)).fetchone()
    if output:
      existing_students.append(_id)
  return existing_students


def _allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in {"csv"}


def _get_name(my_str):
  return re.split(', ', my_str)[1]


def _get_surname(my_str):
  return re.split(', ', my_str)[0]


class _Person:
  def __init__(self, name, surname):
    self.name = name
    self.surname = surname

  def __hash__(self):
    return hash((self.name, self.surname)) % 2 ** sys.hash_info.width


def _get_hash(x):
  name = x['name']
  surname = x['surname']
  return hash(_Person(name, surname))
