/* Change Student Number to Email Address if the user is Instructor */
function changeTextForInstructor() {
    document.getElementById('student-number-or-instructor-email').placeholder = "Email Address";
    document.getElementById('student-number-or-instructor-email').pattern = "[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$";
    document.getElementById('student-number-or-instructor-email').title = "Invalid Email";
    document.getElementById('student-number-or-instructor-email').value = "";
}

/* Change Email Address to Student Number if the user is Student */
function changeTextForStudent() {
    document.getElementById('student-number-or-instructor-email').placeholder = "Student Number";
    document.getElementById('student-number-or-instructor-email').pattern = "[0-9]{10}";
    document.getElementById('student-number-or-instructor-email').title = "Invalid Student Number";
    document.getElementById('student-number-or-instructor-email').value = "";
}
