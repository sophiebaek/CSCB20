$(function() {

  // When login is submitted post request and send credentials
  // Display login failed if incorrect credentials
  $("#login_form").submit(function(event) {
    event.preventDefault();

    var url = $("#login_form").attr("action");
    var postData = $("#login_form").serialize();

    $.ajax({
      url: url,
      type: "POST",
      data: postData,
      dataType: "html",
      success: function(data){
        location.reload();
      },
      statusCode: {
        401: function(response) {
          error = JSON.parse(response.responseText);
          alert(error.message);
          $("#login-password").val("");
        }
      }
    });
  });

  // When create account is submitted post request with account details
  // Display failed to create if username or student num already exists
  $("#create_form").submit(function(event) {
    event.preventDefault();

    var url = $("#create_form").attr("action");
    var postData = $("#create_form").serialize();

    $.ajax({
      url: url,
      type: "POST",
      data: postData,
      dataType: "html",
      success: function(data){
        alert("Created account.");
        location.reload();
      },
      statusCode: {
        401: function(response) {
          error = JSON.parse(response.responseText);
          alert(error.message);
          if(error.type == "USERNAME") {
            console.log("geer")
            $("#create-username").val("");
            $("#create-password").val("");
          }
          else {
            $("#student-number-or-instructor-email").val("");
            $("#create-password").val("");
          }
        }
      }
    });
  });
});
