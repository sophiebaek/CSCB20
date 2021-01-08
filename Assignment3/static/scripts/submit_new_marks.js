$(function() {
  var alerted = false;

  // When user clicks on mark to edit alert that user needs to press submit marks
  // button to submit new Marks
  // Only alert the first time
  $(".mark input").on("click", function() {
    $("#submit_marks_btn").prop("disabled", false);

    if(alerted == false) {
      alert("Press \"Submit Mark\" button to submit new marks.");
      alerted = true;
    }
  });


  // Return a json format of student Marks
  // Formatted in the following way
  // {
  //   student_0: {fname: "", lname: "", ...}
  //   student_1: ...
  // }
  function get_student_marks() {
    var result_json = {};

    // Get num of students from html form
    var num_students = ($("#submit_marks_form input[type=text]").size()/9);
    // Get the list of names, student nums, etc
    var student_fnames = $("#submit_marks_form input[name=fname]");
    var student_lnames = $("#submit_marks_form input[name=lname]");
    var student_nums = $("#submit_marks_form input[name=student_no]");
    var student_a1s = $("#submit_marks_form input[name=A1]");
    var student_a2s = $("#submit_marks_form input[name=A2]");
    var student_a3s = $("#submit_marks_form input[name=A3]");
    var student_labs = $("#submit_marks_form input[name=lab]");
    var student_midterms = $("#submit_marks_form input[name=midterm]");
    var student_finals = $("#submit_marks_form input[name=final]");

    // For each student, create an inner json that hold student info and mark info
    // Set this inner json to be the value of the current student key in outer
    // json
    for (i = 0; i < num_students; i++) {
      curr_student_json = {};
      curr_student_json["fname"] = student_fnames[i].value;
      curr_student_json["lname"] = student_lnames[i].value;
      curr_student_json["student_no"] = student_nums[i].value;
      curr_student_json["a1"] = student_a1s[i].value;
      curr_student_json["a2"] = student_a2s[i].value;
      curr_student_json["a3"] = student_a3s[i].value;
      curr_student_json["lab"] = student_labs[i].value;
      curr_student_json["midterm"] = student_midterms[i].value;
      curr_student_json["final"] = student_finals[i].value;

      result_json["student_" + i] = curr_student_json;
    }

    return result_json;
  }

  // Notify user that marks were submitted
  function notify() {
    alert("Submitted Marks");
    $("#submit_marks_btn").prop("disabled", true);
    // location.reload();
  }

  // Send post request when form submitted with formatted data
  $("#submit_marks_form").submit(function(event) {
    event.preventDefault();

    var url = $("#submit_marks_form").attr("action");
    var postData = get_student_marks();

    $.ajax({
      url: url,
      type: "POST",
      dataType: "json",
      contentType: 'application/json',
      data: JSON.stringify(postData),
      async: false,
      success: notify()
    });
  });
});
