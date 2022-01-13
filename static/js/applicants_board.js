$(document).on('click', '.addToPostingSubmit', function (e) {
  var _this = $(this)
  var url = $(this).closest('.modal').attr("data-ajax-url");
  var applicant_id = $(this).closest('.modal').attr("data-applicant-id");
  var posting_id = $('.job_posting_select').val();

  if (confirm(`Are you sure you want to add this applicant to your job posting?`)) {
      $.ajax({
          url: url,
          data: {
            'applicant_id': applicant_id,
            'posting_id': posting_id,
          },
          success: function (data) {
            $("#addToPostingModal").modal('toggle');
          },
          error: function(xhr, textStatus, error){
              console.log(xhr.statusText);
              console.log(textStatus);
              console.log(error);
          }
        });
  }

});