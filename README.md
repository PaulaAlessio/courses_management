# WORK IN PROGESS PROJECT


## Temporary deployment
```
# Create a virtual environment (optional) 
[...]
# install the requirements
[...]
export PYTHONPATH=<PATH/TO/PROJECT/DIRECTORY>
# Maybe it is correctly exported 
export PYTHONHASHSEED=0
# Initialize database
python3 -m flask --app src/app.py init-db
# Launch application 
flask --app src/app.py  run
# Expected output
Current Environment: Development
Using Database: board.sqlite
Using PythonPath: None
 * Serving Flask app 'src/app.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
# Open the browser on the  URL above
 
```
**WARNING:** Currently, there is NO error handling. This means, if there's any 
error while filling out the forms, you will most probably end up with a 
database error making the page rendering impossible, ;-). 


**NOTE:** you can use pycharm to launch the application instead.

## How to create a dummy example

In folder `dummy_students_data` you can find data to play with. 

### Importar grupo
The first thing you have to do is to import student groups. The file formats at 
your disposal are: 

- moodle format
- raíces format

Choose one of them and fill in the _importar grupo_ form consequently. 

When you are done with it, you can go to the _Grupos_ tab and check that 
the groups you just imported are available. You can also click on the 
group names to see the list of students. 

### Crear curso 

Once your groups have been imported, you are ready to create a course 
with one or several groups. Go to hte tab: _Crear Curso_ and fill in 
the form. 

Once you are done with it, you can go to the _Cursos_ tab and see a list 
of the so far created courses. Click on an already existing course. 

[...]

 To be continued ....
