$(function() {

  // Display student only links/content
  function show_student_links() {
    $(".student_only").show()
  }

  // Display instructor only links/content
  function show_instructor_links() {
    $(".instructor_only").show()
  }

  // Get request for type of currently logged in user
  // Hide content based on response
  $.ajax({
    url:"/current_user",
    type: "GET",
    success: function(data) {
      if (data.user_type == "student") {
        show_student_links();
      }
      else{
        show_instructor_links();
      }
    }
  });
});
