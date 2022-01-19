function modal_valid(modal) {
  modal.find('.required').each(function() {
    debugger;
    this.valid();
  });
};


$(document).on('click', '#addEmploymentHistorySubmit', function (e) {

  var company = $("#addEmploymentHistoryModal #company").val()
  var position = $("#addEmploymentHistoryModal #position").val()
  var employment_type = $("#addEmploymentHistoryModal #employment_type").val()
  var start_month = $("#addEmploymentHistoryModal #start_month").val()
  var start_year = $("#addEmploymentHistoryModal #start_year").val()
  var start = ""
  if (start_month && start_year) {
    start = `${start_month} / ${start_year}`
  }
  var end_month = $("#addEmploymentHistoryModal #end_month").val()
  var end_year = $("#addEmploymentHistoryModal #end_year").val()
  var end = ""
  if (end_month && end_year) {
    start = `${end_month} / ${end_year}`
  }
  var current = $("#addEmploymentHistoryModal #current").val()
  var overview = $("#addEmploymentHistoryModal #overview").val()
  var reference_person = $("#addEmploymentHistoryModal #reference_person").val()
  var mobile_number = "+63" + $("#addEmploymentHistoryModal #mobile_number").val()

  var url = $("#addEmploymentHistoryModal").attr("data-ajax-url");

  $.ajax({
    url: url,
    data: {
      'company': company,
      'position': position,
      'employment_type': employment_type,
      'start_month': start_month,
      'start_year': start_year,
      'end_month': end_month,
      'end_year': end_year,
      'current': current,
      'overview': overview,
      'reference_person': reference_person,
      'mobile_number': mobile_number,
    },
    success: function (data) {
      var newTbody = ""
      data.items.forEach(function(row) {
        var start = ""
        var end = ""
        var mobile_number = ""
        var current = ""
        var employment_type = data.types[row.employment_type]
        var start_month = data.months[row.start_month]
        var end_month = data.months[row.end_month]

        if (start_month && row.start_year) {
          start = `${start_month} / ${row.start_year}`
        }
        if (end_month && row.end_year) {
          end = `${end_month} / ${row.end_year}`
        }
        if (row.mobile_number) {
          mobile_number = `(${row.mobile_number})`
        }

        if (row.current) {
          current = `<i class="far fa-check-circle"></i>`
        }

        newTbody += `
          <tr>
            <td>${row.company_name}</td>
            <td>${row.job_position}</td>
            <td>${employment_type}</td>
            <td>${start}</td>
            <td>${end}</td>
            <td>${current}</td>
            <td>${row.reference_person} ${mobile_number}</td>
            <td class="p-0">
              <span class="table-remove">
                <span class="remove-row" data-id="${row.id}">
                  <i class="fas fa-times-circle"></i>
                </span>
              </span>
            </td>
          </tr>
        `;
      });

      $("#EmploymentHistoryTable tbody").html(newTbody);

      var nodata = $("#EmploymentHistoryTable .nodata")
      if (nodata.length) {
        nodata.remove()
      }

      $("#addEmploymentHistoryModal #company").val("")
      $("#addEmploymentHistoryModal #position").val("")
      $("#addEmploymentHistoryModal #employment_type").val("")
      $("#addEmploymentHistoryModal #start_month").val("")
      $("#addEmploymentHistoryModal #start_year").val("")
      $("#addEmploymentHistoryModal #end_month").val("")
      $("#addEmploymentHistoryModal #end_year").val("")
      $("#addEmploymentHistoryModal #current").prop('checked', false);
      $("#addEmploymentHistoryModal #overview").val("")
      $("#addEmploymentHistoryModal #reference_person").val("")
      $("#addEmploymentHistoryModal #mobile_number").val("")
      $("#addEmploymentHistoryModal").modal('toggle');
    },
    error: function(xhr, textStatus, error){
        console.log(xhr.statusText);
        console.log(textStatus);
        console.log(error);
    }
  });

});  // addEmploymentHistorySubmit

$(document).on('click', '#addEducationSubmit', function (e) {
  var school_name = $("#addEducationModal #school_name").val()
  var degree = $("#addEducationModal #degree").val()
  var start_month = $("#addEducationModal #start_month").val()
  var start_year = $("#addEducationModal #start_year").val()
  var start = ""
  if (start_month && start_year) {
    start = `${start_month} / ${start_year}`
  }
  var end_month = $("#addEducationModal #end_month").val()
  var end_year = $("#addEducationModal #end_year").val()
  var end = ""
  if (end_month && end_year) {
    start = `${end_month} / ${end_year}`
  }
  var reference_person = $("#addEducationModal #reference_person").val()
  var mobile_number = "+63" + $("#addEducationModal #mobile_number").val()

  var url = $("#addEducationModal").attr("data-ajax-url");

  $.ajax({
    url: url,
    data: {
      'school_name': school_name,
      'degree': degree,
      'start_month': start_month,
      'start_year': start_year,
      'end_month': end_month,
      'end_year': end_year,
      'reference_person': reference_person,
      'mobile_number': mobile_number,
    },
    success: function (data) {
      var newTbody = ""
      data.items.forEach(function(row) {
        var start = ""
        var end = ""
        var mobile_number = ""
        var start_month = data.months[row.start_month]
        var end_month = data.months[row.end_month]

        if (start_month && row.start_year) {
          start = `${start_month} / ${row.start_year}`
        }
        if (end_month && row.end_year) {
          end = `${end_month} / ${row.end_year}`
        }
        if (row.mobile_number) {
          mobile_number = `(${row.mobile_number})`
        }

        newTbody += `
          <tr>
            <td>${row.school_name}</td>
            <td>${row.degree}</td>
            <td>${start}</td>
            <td>${end}</td>
            <td>${row.reference_person} ${mobile_number}</td>
            <td class="p-0">
              <span class="table-remove">
                <span class="remove-row" data-id="${row.id}">
                  <i class="fas fa-times-circle"></i>
                </span>
              </span>
            </td>
          </tr>
        `;
      });

      $("#educationTable tbody").html(newTbody);

      var nodata = $("#educationTable .nodata")
      if (nodata.length) {
        nodata.remove()
      }

      $("#addEducationModal #school_name").val("")
      $("#addEducationModal #degree").val("")
      $("#addEducationModal #start_month").val("")
      $("#addEducationModal #start_year").val("")
      $("#addEducationModal #end_month").val("")
      $("#addEducationModal #end_year").val("")
      $("#addEducationModal #reference_person").val("")
      $("#addEducationModal #mobile_number").val("")
      $("#addEducationModal").modal('toggle');
    },
    error: function(xhr, textStatus, error){
        console.log(xhr.statusText);
        console.log(textStatus);
        console.log(error);
    }
  });

});  // addEducationSubmit

$(document).on('click', '#addJobPostingSubmit', function (e) {
  var url = $("#addJobPostingModal").attr("data-ajax-url");
  var csrf_token = $("#addJobPostingModal").attr("data-csrf-token");
  var job_title = $("#addJobPostingModal #job_title").val()
  var description = $("#addJobPostingModal #description").val()
  var vacancy = $("#addJobPostingModal #vacancy").val()
  var salary_range_end = $("#addJobPostingModal #salary_range_end").val()
  var salary_range_start = $("#addJobPostingModal #salary_range_start").val()
  var preferred_skills = $("#addJobPostingModal #preferred_skills").val()

  var formData = new FormData()
  formData.append('job_title', job_title)
  formData.append('description', description)
  formData.append('vacancy', vacancy)
  formData.append('salary_range_end', salary_range_end)
  formData.append('salary_range_start', salary_range_start)
  formData.append('preferred_skills', preferred_skills)
  formData.append('csrfmiddlewaretoken', csrf_token)
  $.each($("#addJobPostingModal #attachments")[0].files, function(i, file) {
    formData.append("files", file);
  });

  $.ajax({
    url: url,
    data: formData,
    method: 'post',
    processData: false,
    contentType: false,
    cache: false,
    enctype: 'multipart/form-data',
    success: function (data) {
      $("#JobPostingTable tbody").html(postingStr);

      var nodata = $("#JobPostingTable .nodata")
      if (nodata.length) {
        nodata.remove()
      }

      $("#addJobPostingModal #job_title").val("")
      $("#addJobPostingModal #description").html("")
      $("#addJobPostingModal #vacancy").val("")
      $("#addJobPostingModal #salary_range_end").val("")
      $("#addJobPostingModal #salary_range_start").val("")
      $("#addJobPostingModal").modal('toggle');
    },
    error: function(xhr, textStatus, error){
        console.log(xhr.statusText);
        console.log(textStatus);
        console.log(error);
    }
  });

});  // addJobPostingSubmit


$(document).on('click', 'table .remove-row', function() {
  var _this = $(this)
  var _id = _this.attr("data-id");
  var _table = _this.attr("data-table");
  var th_count = _this.closest("table").find("th").length
  var tbody = _this.closest("tbody")

  if (confirm('Are you sure you want to delete this?')) {
    $.ajax({
      url: '/users/ajax/delete-data/',
      data: {
        'id': _id,
        'table': _table
      },
      success: function (data) {
        _this.closest("tr").remove();
        if (_this.closest("tbody").find("tr").length == 0) {
          var newTr = `<tr class="nodata">
                          <td colspan="${th_count}">No Data</td>
                        </tr>`

          $(newTr).appendTo(tbody)
        }
      },
      error: function(xhr, textStatus, error){
          console.log(xhr.statusText);
          console.log(textStatus);
          console.log(error);
      }
    });
  }

}) ;

$(document).on('click', '.badge .delete-file', function() {
  var _id = $(this).attr("data-id");
  var _type = $(this).attr("data-type");
  var _this = $(this);

  if (confirm('Are you sure you want to delete this?')) {
    $.ajax({
      url: '/users/ajax/delete-attachment/',
      data: {
        'id': _id,
        'type': _type
      },
      success: function (data) {
        _this.parent().remove();
      },
      error: function(xhr, textStatus, error){
          console.log(xhr.statusText);
          console.log(textStatus);
          console.log(error);
      }
    });
  }

}) ;

$(document).on('click', '#addSkillSubmit', function (e) {
  var url = $("#addSkillModal").attr("data-ajax-url");
  var csrf_token = $("#addSkillModal").attr("data-csrf-token");
  var user_id = $("#addSkillModal").attr("data-user-id");
  var school_name = $("#addSkillModal #school_name").val()
  var efficiency = $("#addSkillModal #efficiency").val()
  var attachment = $("#addSkillModal #attachment")[0].files[0]

  var formData = new FormData()
  formData.append('csrfmiddlewaretoken', csrf_token)
  formData.append('_id', user_id)
  formData.append('school_name', school_name)
  formData.append('efficiency', efficiency)
  formData.append("file", attachment);

  $.ajax({
    url: url,
    data: formData,
    method: 'post',
    processData: false,
    contentType: false,
    cache: false,
    enctype: 'multipart/form-data',
    success: function (data) {
      var newTbody = ""

      data.items.forEach(function(row) {

        var attachment = ""
        if (row.attachment) {
          attachment += `<span class="badge rounded-pill bg-info">
                    <a href="${row.attachment.url}">${row.attachment}</a> |
                  </span>`
        }

        newTbody += `
          <tr>
            <td>${row.name}</td>
            <td>${row.efficiency}</td>
            <td>${attachment}</td>
            <td class="p-0">
              <span class="table-remove">
                <span class="remove-row" data-id="${row.id}" data-table="ApplicantSkill">
                  <i class="fas fa-times-circle"></i>
                </span>
              </span>
            </td>
          </tr>
        `;
      });

      $("#skillsTable tbody").html(newTbody);

      var nodata = $("#skillsTable .nodata")
      if (nodata.length) {
        nodata.remove()
      }

      $("#addSkillModal #school_name").val("")
      $("#addSkillModal #efficiency").val("")
      $("#addSkillModal #attachment").val("")
      $("#addSkillModal").modal('toggle');
    },
    error: function(xhr, textStatus, error){
        console.log(xhr.statusText);
        console.log(textStatus);
        console.log(error);
    }
  });

});  // addSkillSubmit

$(document).on('click', 'tr.job_posting_table_item', function() {
  var _this = $(this)
  var _id = _this.attr("data-id");

  $.ajax({
    url: '/jobs/ajax/job-details/',
    data: {
      'id': _id,
    },
    success: function (data) {
      $("#emptyModal").modal('toggle');
      $("#emptyModal .modal-content").html(data.postingStr);
    },
    error: function(xhr, textStatus, error){
        console.log(xhr.statusText);
        console.log(textStatus);
        console.log(error);
    }
  });

}) ;

$(document).on('click', '#updateJobPostingSubmit', function (e) {
  e.preventDefault()

  var modal = $(this).closest(".modal")
  var url = $(this).attr("data-ajax-url");
  var csrf_token = $(this).attr("data-csrf-token");
  var _id = $(this).attr("data-id");
  var job_title = modal.find("#job_title").val()
  var description = modal.find("#description").val()
  var vacancy = modal.find("#vacancy").val()
  var salary_range_end = modal.find("#salary_range_end").val()
  var salary_range_start = modal.find("#salary_range_start").val()
  var preferred_skills = modal.find("#preferred_skills").val()

  var formData = new FormData()
  formData.append('job_title', job_title)
  formData.append('description', description)
  formData.append('vacancy', vacancy)
  formData.append('salary_range_end', salary_range_end)
  formData.append('salary_range_start', salary_range_start)
  formData.append('preferred_skills', preferred_skills)
  formData.append('csrfmiddlewaretoken', csrf_token)
  formData.append('id', _id)
  $.each(modal.find("#attachments")[0].files, function(i, file) {
    formData.append("files", file);
  });

  $.ajax({
    url: url,
    data: formData,
    method: 'post',
    processData: false,
    contentType: false,
    cache: false,
    enctype: 'multipart/form-data',
    success: function (data) {
      $("#emptyModal .modal-content").html(data.postingStr);
      modal.modal('toggle');
    },
    error: function(xhr, textStatus, error){
        console.log(xhr.statusText);
        console.log(textStatus);
        console.log(error);
    }
  });

});  // addJobPostingSubmit

$(document).on('click', '.postingCandidateApply', function (e) {
  var _this = $(this)
  var _id = $(this).attr("data-posting-id");
  var user_id = $(this).attr("data-user-id");
  var url = $(this).attr("data-ajax-url");
  var action = "apply"

  _this.attr('disabled','disabled');

  $.ajax({
      url: url,
      data: {
        'id': _id,
        'user_id': user_id,
        'action': action,
      },
      success: function (data) {
        reload_candidates(_id);
      },
      error: function(xhr, textStatus, error){
          console.log(xhr.statusText);
          console.log(textStatus);
          console.log(error);
      }
    });

});

function reload_candidates(_id) {
  $.ajax({
    url: '/jobs/ajax/get-candidates/',
    data: {
      '_id':_id
    },
    success: function (data) {
      $('.candidates_container').html(data.postingStr);
    },
    error: function(xhr, textStatus, error){
        console.log(xhr.statusText);
        console.log(textStatus);
        console.log(error);
    }
  });
}