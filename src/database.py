import sqlite3
import click
from flask import current_app, g


def init_app(app):
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)


@click.command("init-db")
def init_db_command():
  print("Initializing database ...")
  db = get_db()
  with current_app.open_resource("schema.sql") as f:
    db.executescript(f.read().decode("utf-8"))
  create_event_type_table(db)
  create_tab_table(db)
  click.echo("You successfully initialized the database!")


def create_event_type_table(_db):
  _db.execute("INSERT INTO event_type (name, type, max_value, min_value, max_color, min_color, mean_color) VALUES ("
              "'asistencia', 'integer', 2, 0, 2,1,0)")
  _db.execute("INSERT INTO event_type (name, type, max_value, min_value, max_color, min_color, mean_color) VALUES ("
              "'prueba_escrita', 'real', 10, 0, 5, 4, 'yellow')")
  _db.execute("INSERT INTO event_type (name, type, max_value, min_value, max_color, min_color, mean_color) VALUES ("
              "'trabajo_casa', 'integer', 2, 0, 5, 4, 'yellow')")
  _db.execute("INSERT INTO event_type (name, type, max_value, min_value, max_color, min_color, mean_color) VALUES ("
              "'trabajo_clase', 'integer', 2, 0, 5, 4, 'yellow')")
  _db.execute("INSERT INTO event_type (name, type, max_value, min_value, max_color, min_color, mean_color) VALUES ("
              "'entrega_ejercicios', 'real', 10, 0, 5, 4, 'yellow')")
  _db.execute("INSERT INTO event_type (name, type, max_value, min_value, max_color, min_color, mean_color) VALUES ("
              "'boletín', 'integer', 10, 0, 5, 4, 'yellow')")
  _db.commit()


def create_tab_table(_db):
  _db.execute("INSERT INTO TAB (name) VALUES ('Primer Trimestre')")
  _db.execute("INSERT INTO TAB (name) VALUES ('Segundo Trimestre')")
  _db.execute("INSERT INTO TAB (name) VALUES ('Tercer Trimestre')")
  _db.execute("INSERT INTO TAB (name) VALUES ('Asistencia')")
  _db.execute("INSERT INTO TAB (name) VALUES ('Amonestaciones')")
  _db.commit()


def get_db():
  if "db" not in g:
    g.db = sqlite3.connect(
      current_app.config["DATABASE"],
      detect_types=sqlite3.PARSE_DECLTYPES,
    )
    g.db.row_factory = sqlite3.Row
  return g.db


def close_db(e=None):
  db = g.pop("db", None)

  if db is not None:
    db.close()
