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
    var current = $("#addEmploymentHistoryModal #current").is(':checked')
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

        if (current == 'true') {
          current = `<i class="far fa-check-circle"></i>`
        } else {
          current = ""
        }
        const newTr = `
          <tr>
            <td>${company}</td>
            <td>${position}</td>
            <td>${employment_type}</td>
            <td>${start}</td>
            <td>${end}</td>
            <td>${current}</td>
            <td>${reference_person} (${mobile_number})</td>
            <td>
              <span class="table-remove">
                <button type="button" class="remove-row btn btn-danger btn-rounded btn-sm my-0">
                  <i class="fas fa-times"></i>
                </button>
              </span>
            </td>
          </tr>
        `;

        $(newTr).appendTo($("#addEmploymentHistoryTable tbody"))

        var nodata = $("#addEmploymentHistoryTable .nodata")
        if (nodata.length) {
          nodata.remove()
        }

        $("#addEmploymentHistoryModal #company").val("")
        $("#addEmploymentHistoryModal #position").val("")
        $("#addEmploymentHistoryModal #employment_type").val("")
        $("#addEmploymentHistoryModal #start_month").val("january")
        $("#addEmploymentHistoryModal #start_year").val("2022")
        $("#addEmploymentHistoryModal #end_month").val("")
        $("#addEmploymentHistoryModal #end_year").val("")
        $("#addEmploymentHistoryModal #current").val("")
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

});  // Document ready

$(document).on('click', 'table .remove-row', function() {
  var _id = $(this).attr("data-id");
  var _this = $(this)

  debugger;
  if (confirm('Are you sure you want to delete this?')) {
    $.ajax({
      url: '/users/ajax/delete-data/',
      data: {
        'id': _id,
        'table': "ApplicantExperience"
      },
      success: function (data) {
        _this.closest("tr").remove();

        if ($("#addEmploymentHistoryTable tbody tr").length == 0) {
          var newTr = `<tr class="nodata">
                          <td colspan="100%">No Data</td>
                        </tr>`
          $(newTr).appendTo($("#addEmploymentHistoryTable tbody"))
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
