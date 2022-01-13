$(document).on('click', '.jobPostingApply', function (e) {
  var _this = $(this)
  var _id = $(this).attr("data-id");
  var url = $(this).attr("data-ajax-url");
  var action = $(this).attr("data-action");

  if (confirm(`Are you sure you want to ${action}?`)) {
      $.ajax({
          url: url,
          data: {
            'id': _id,
            'action': action,
          },
          success: function (data) {
            if (action == "apply") {
                var btnStr = `<button id="jobPostingApply" data-id="${_id}" data-ajax-url="${url}" data-action="cancel">Cancel</button>`
            } else {
                var btnStr = `<button id="jobPostingApply" data-id="${_id}" data-ajax-url="${url}" data-action="apply">Apply</button>`
            }
            _this.replaceWith(btnStr)
          },
          error: function(xhr, textStatus, error){
              console.log(xhr.statusText);
              console.log(textStatus);
              console.log(error);
          }
        });
  }

});

$(document).on('click', '.scheduleInterviewSubmit', function (e) {
  var _this = $(this)
  var modal = $(this).closest('.modal')
  var user_id = modal.attr("data-user-id");
  var posting_id = modal.attr("data-posting-id");
  var date = modal.find('input').val();
  var url = modal.attr("data-ajax-url");

    $.ajax({
      url: url,
      data: {
        'user_id': user_id,
        'posting_id': posting_id,
        'date': date,
      },
      success: function (data) {
        modal.find('input').val("");
        modal.modal('toggle');
      },
      error: function(xhr, textStatus, error){
          console.log(xhr.statusText);
          console.log(textStatus);
          console.log(error);
      }
    });

});

$(document).on('click', '.declineApplicant', function (e) {
  var _this = $(this)
  var user_id = _this.attr("data-user-id");
  var posting_id = _this.attr("data-posting-id");
  var actions_div = _this.closest('.job_posting_actions');
  var url = _this.attr("data-ajax-url");

  if (confirm(`Are you sure you want to decline this application?`)) {
    $.ajax({
      url: url,
      data: {
        'user_id': user_id,
        'posting_id': posting_id,
      },
      success: function (data) {
        actions_div.remove();
      },
      error: function(xhr, textStatus, error){
          console.log(xhr.statusText);
          console.log(textStatus);
          console.log(error);
      }
    });
  }

});

$(document).on('click', '.hireApplicant', function (e) {
  var _this = $(this)
  var user_id = _this.attr("data-user-id");
  var posting_id = _this.attr("data-posting-id");
  var actions_div = _this.closest('.job_posting_actions');
  var url = _this.attr("data-ajax-url");

  if (confirm(`Are you sure you want to hire this applicant?`)) {
    $.ajax({
      url: url,
      data: {
        'user_id': user_id,
        'posting_id': posting_id,
      },
      success: function (data) {
        actions_div.remove();
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
