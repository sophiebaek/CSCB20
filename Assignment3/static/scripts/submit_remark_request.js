$(function() {
  // Reload page after alerting remark request was submitted
  function reload() {
    alert("Submitted Remark Request")
    location.reload();
  }

  // When remark request form submitted, reload page and notify user
  $("#remark_request_form").submit(function(event) {
    event.preventDefault();

    var url = $("#remark_request_form").attr("action");
    var postData = $("#remark_request_form").serialize();

    $.ajax({
      url: url,
      type: "POST",
      data: postData,
      success: reload()
    });
  });
});
