$(function() {
  // Reload page after alerting feedback was submitted
  function reload() {
    alert("Submitted Feedback")
    location.reload();
  }

  // When feedback form submitted, reload page and notify user
  $("#feedback_form").submit(function(event) {
    event.preventDefault();

    var url = $("#feedback_form").attr("action");
    var postData = $("#feedback_form").serialize();

    $.ajax({
      url: url,
      type: "POST",
      data: postData,
      success: reload()
    });
  });
});
