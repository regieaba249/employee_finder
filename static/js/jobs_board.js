$(document).on('click', '.jobPostingApply', function (e) {
  var _this = $(this)
  var _id = $(this).attr("data-posting-id");
  var user_id = $(this).attr("data-user-id");
  var url = $(this).attr("data-ajax-url");
  var action = $(this).attr("data-action");

  _this.attr('disabled','disabled');

  if (confirm(`Are you sure you want to ${action}?`)) {
      $.ajax({
          url: url,
          data: {
            'id': _id,
            'user_id': user_id,
            'action': action,
          },
          success: function (data) {
            if (action == "apply") {
                var btnStr = `<button id="jobPostingApply" data-id="${_id}" data-ajax-url="${url}" data-action="cancel">Cancel</button>`
            } else {
                var btnStr = `<button id="jobPostingApply" data-id="${_id}" data-ajax-url="${url}" data-action="apply">Apply</button>`
            }
            _this.replaceWith(btnStr)
            $('.job_posting_applicants').replaceWith(data.applicantsStr)
          },
          error: function(xhr, textStatus, error){
              console.log(xhr.statusText);
              console.log(textStatus);
              console.log(error);
          }
        });
  }

});

$(document).on('click', '#filterPostings', function (e) {
  var _this = $(this)
  var _input = $("#searchInput");
  var url = _input.attr("data-ajax-url");

  $.ajax({
    url: url,
    data: {
      '_input': _input.val(),
    },
    success: function (data) {
      $('#postingsContainer').html(data.htmlStr)
    },
    error: function(xhr, textStatus, error){
        console.log(xhr.statusText);
        console.log(textStatus);
        console.log(error);
    }
  });

});

$(document).on('click', '.jobPostingArchive', function (e) {
  var _this = $(this)
  var _parent = $(this).closest('.bg-white.border.mt-2')
  var _id = _this.attr("data-id");
  var url = _this.attr("data-ajax-url");

  if (confirm(`Are you sure you want to archive this job posting?`)) {
    $.ajax({
      url: url,
      data: {
        '_id': _id,
      },
      success: function (data) {
        _parent.remove()
      },
      error: function(xhr, textStatus, error){
          console.log(xhr.statusText);
          console.log(textStatus);
          console.log(error);
      }
    });
  }

});
