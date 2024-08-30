DROP TABLE IF EXISTS course;
CREATE TABLE course (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "created" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "name" TEXT UNIQUE NOT NULL,
  "year1" INTEGER NOT NULL,
  "year2" INTEGER NOT NULL
);

DROP TABLE IF EXISTS course_group;
CREATE TABLE course_group (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "course_id" INTEGER NOT NULL,
  "group_id" INTEGER NOT NULL
);


DROP TABLE IF EXISTS _group;
CREATE TABLE _group (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "created" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "_level" TEXT NOT NULL,
  "linea" TEXT NOT NULL,
  "name" TEXT UNIQUE NOT NULL,
  "year1" INTEGER NOT NULL,
  "year2" INTEGER NOT NULL,
  "is_gm" BIT NOT NULL
);


DROP TABLE IF EXISTS student;
CREATE TABLE student (
 "id" INTEGER PRIMARY KEY,
 "name" TEXT NOT NULL,
 "surname" TEXT NOT NULL,
 "NIA" TEXT UNIQUE,
 "email" TEXT,
 "tutor_email" TEXT,
 "telephone1" UNSIGNED BIG INT,
 "telephone2" UNSIGNED BIG INT
);


DROP TABLE IF EXISTS student_group;
CREATE TABLE student_group (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "student_id" UNSIGNED BIG INT NOT NULL,
  "group_id" INTEGER NOT NULL
);


DROP TABLE IF EXISTS tab;
CREATE TABLE tab (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "name" TEXT NOT NULL
);


DROP TABLE IF EXISTS tab_column;
CREATE TABLE tab_column (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "tab_id" INTEGER NOT NULL,
  "course_id" INTEGER NOT NULL,
  "type_id" INTEGER NOT NULL,
  "name" TEXT NOT NULL
);


DROP TABLE IF EXISTS event_type;
CREATE TABLE event_type (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "name" TEXT UNIQUE NOT NULL,
  "type" TEXT NOT NULL,
  "max_value" REAL,
  "min_value" REAL,
  "max_color" BLOB,
  "min_color" BLOB,
  "mean_color" BLOB
);

DROP TABLE IF EXISTS event;
CREATE TABLE event (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "datetime" TEXT NOT NULL,
  "tab_column_id" INTEGER NOT NULL,
  "student_id" INTEGER NOT NULL,
  "event_type_id" INTEGER NOT NULL,
  "value_real"    REAL,
  "value_int"    INTEGER,
  "value_text"    TEXT
);