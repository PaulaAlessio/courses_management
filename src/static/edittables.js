
"use strict";
const doc = document;

const form = doc.getElementById('new_column');

form.addEventListener('submit', async event => {
  event.preventDefault();
  const data = new FormData(form);
  console.log(JSON.stringify(Object.fromEntries(data)));
  try {
    const res = await fetch(
      '/courses/api/'+data.get("course_id"),
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: JSON.stringify(Object.fromEntries(data)),
      },
    );
    const resData = await res.json();
    window.location.reload();
    console.log(resData);
  } catch (err) {
    console.log(err.message);
  }
});

doc.addEventListener("DOMContentLoaded", function(event) {

    // Used for API Requests
    var xhr1 = new XMLHttpRequest();

    // Toasts
    const notyf = new Notyf({
         position: {
             x: 'right',
             y: 'top',
         },
         types: [
             {
                 type: 'info',
                 background: '#FA5252',
                 icon: {
                     className: 'fas fa-comment-dots',
                     tagName: 'span',
                     color: '#fff'
                 },
                 dismissible: false
             }
         ]
     });

    // Used by cell edit
    document.addEventListener('keydown', event => {
        // Catch 'ENTER' event
        if (event.key === 'Enter') {
            // If applies on a TD
            if (event.target.matches('td.single-line')) {
                console.log("this is a test b");
               // Drop the default event
               event.preventDefault();
               let td = event.target;
               let tr = event.target.closest('tr.single-line');
               let student_id = tr.id;
               let column_id = td.dataset.column_id;
               let event_id = td.dataset.event_id;
               let tab_id = td.dataset.tab_id;
               let course_id = td.dataset.course_id;
               let value = td.textContent;
               console.log(student_id, tab_id, course_id, column_id, value);
               xhr1.open("PUT", "/courses/api/update_event/" + event_id);
               xhr1.setRequestHeader("Content-Type", "application/json");
               // Check Status
               xhr1.onreadystatechange = function() {

                   if (this.status == 200 && this.readyState == 4) {

                       notyf.open({
                           type: 'success',
                           message: 'Information saved successfully'
                       });
                   }

                   // XMLHttpRequest returns 0 on success
                   if ( (this.status > 0) && (this.status != 200) ) {

                       notyf.open({
                           type: 'error',
                           message: 'Error!'
                       });
                    }

                };//end onreadystate

                xhr1.send(JSON.stringify( { student_id: student_id,
                                            column_id: column_id,
                                            event_id: event_id,
                                            tab_id: tab_id,
                                            course_id: course_id,
                                            value: value} ));
               console.log(JSON.stringify( { student_id: student_id,
                                            column_id: column_id,
                                            event_id: event_id,
                                            tab_id: tab_id,
                                            course_id: course_id,
                                            value: value}));
               // Disable 'EDITABLE' property
               //td.setAttribute("contenteditable", "false");

            } // END if (event.target.matches('td.editable')) {

        } // END if (event.key === 'Enter') {

    });
});
