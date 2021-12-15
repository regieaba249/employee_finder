// Material Select Initialization
$(document).ready(function() {
    $('.gender-select').change(function(){
      $('.gender-input').val($('.gender-select').val())
    });
    $('.applicant-status-select').change(function(){
      $('.applicant-status-input').val($('.applicant-status-select').val())
    });

    const $tableID = $('#table'); const $BTN = $('#export-btn'); const $EXPORT = $('#export');
    const newTr = `
    <tr>
      <td class="p-0" contenteditable="true"></td>
      <td class="p-0" contenteditable="true"></td>
      <td class="p-0" contenteditable="true">
        <select class="gender-select mdb-select md-form form-control form-control-lg" required>
          <option value="0" disabled selected>Month</option>
          <option value="1">Jan</option>
          <option value="2">Feb</option>
          <option value="3">Mar</option>
          <option value="4">Apr</option>
          <option value="5">May</option>
          <option value="6">Jun</option>
          <option value="7">Jul</option>
          <option value="8">Aug</option>
          <option value="9">Sep</option>
          <option value="10">Oct</option>
          <option value="11">Nov</option>
          <option value="12">Dec</option>
        </select></td>
      <td class="p-0" contenteditable="true"></td>
      <td class="p-0" contenteditable="true">
        <select class="gender-select mdb-select md-form form-control form-control-lg" required>
          <option value="0" disabled selected>Month</option>
          <option value="1">Jan</option>
          <option value="2">Feb</option>
          <option value="3">Mar</option>
          <option value="4">Apr</option>
          <option value="5">May</option>
          <option value="6">Jun</option>
          <option value="7">Jul</option>
          <option value="8">Aug</option>
          <option value="9">Sep</option>
          <option value="10">Oct</option>
          <option value="11">Nov</option>
          <option value="12">Dec</option>
        </select></td>
      <td class="p-0" contenteditable="true"></td>
      <td class="p-0"><span class="table-remove"><button type="button" class="btn btn-danger btn-rounded btn-sm my-2 px-3"><i class="fas fa-times"></i></button></span></td>
    </tr>
    `;

    $('.table-add').on('click', 'i', () => {
        const $clone = $tableID
            .find('tbody tr')
            .last()
            .clone(true)
            .removeClass('hide table-line');

        if ($tableID.find('tbody tr').length=== 0) {
            $('tbody').append(newTr);
        }
        $tableID.find('table').append($clone);
    });

    $tableID.on('click', '.table-remove', function () {
        $(this).parents('tr').detach();
    });

    $tableID.on('click', '.table-up', function () {
        const $row = $(this).parents('tr');
        if ($row.index() === 0) {
            return;
        }
        $row.prev().before($row.get(0));
     });

     $tableID.on('click', '.table-down', function () {
        const $row = $(this).parents('tr');
        $row.next().after($row.get(0));
     });

     // A few jQuery helpers for exporting only jQuery.fn.pop= [].pop;

     jQuery.fn.shift = [].shift;

     $BTN.on('click', () => {
        const $rows = $tableID.find('tr:not(:hidden)');
        const headers = [];
        const data = [];

        // Get the headers (add special header logic here)
        $($rows.shift()).find('th:not(:empty)').each(function () {
            headers.push($(this).text().toLowerCase());
        });

        // Turn all existing rows into a loopable array
        $rows.each(function () {
            const $td = $(this).find('td');
            const h = {};
            // Use the headers from earlier to name our hash keys
            headers.forEach((header, i) => {
                h[header] = $td.eq(i).text();
            });
            data.push(h);
        });
        // Output the result
        $EXPORT.text(JSON.stringify(data));
     });
});
