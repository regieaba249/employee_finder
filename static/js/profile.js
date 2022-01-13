function modal_valid(modal) {
  modal.find('.required').each(function() {
    debugger;
    this.valid();
  });
};

$(document).ready(function() {

  $('#addEmploymentHistorySubmit').click(function (e) {

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

  });

  $('#addEducationSubmit').click(function (e) {
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

  $('#addJobPostingSubmit').click(function (e) {
    var url = $("#addJobPostingModal").attr("data-ajax-url");
    var csrf_token = $("#addJobPostingModal").attr("data-csrf-token");
    var job_title = $("#addJobPostingModal #job_title").val()
    var description = $("#addJobPostingModal #description").val()
    var vacancy = $("#addJobPostingModal #vacancy").val()
    var salary_range_end = $("#addJobPostingModal #salary_range_end").val()
    var salary_range_start = $("#addJobPostingModal #salary_range_start").val()

    var formData = new FormData()
    formData.append('job_title', job_title)
    formData.append('description', description)
    formData.append('vacancy', vacancy)
    formData.append('salary_range_end', salary_range_end)
    formData.append('salary_range_start', salary_range_start)
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
        var newTbody = ""
        var attachmets = ""
        data.items.forEach(function(row) {
          // row.job_posting_attachments.forEach(function(file) {
          //   attachmets += `
          //     ${file}
          //   `
          // });

          newTbody += `
            <tr>
              <td>${row.job_title}</td>
              <td class="text-truncate">${row.description}</td>
              <td>${row.vacancy}</td>
              <td>${row.salary_range_end} - ${salary_range_start}</td>
              <td>${attachmets}</td>
              <td class="p-0">
                <span class="table-remove">
                  <span class="remove-row" data-id="${row.id}" data-table="CompanyJobPosting">
                    <i class="fas fa-times-circle"></i>
                  </span>
                </span>
              </td>
            </tr>
          `;
        });

        $("#JobPostingTable tbody").html(newTbody);

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
  });  // addEducationSubmit

});  // Document ready

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
