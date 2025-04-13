

document.addEventListener("DOMContentLoaded", function () {

    $("form.create_reservation_form").on('submit', createReservationFormProcessing);

});


function createReservationFormProcessing(event) {
    event.preventDefault();

    let data = {
        'customer_name': $(this).find('input[id="customerNameInput"]').val(),
        'table_id': parseInt($(this).find('select[id="tablesInputGroupSelect"]').val()),
        'reservation_time': moment(new Date($(this).find('input[id="datetimeInput"]').val())).format('YYYY-MM-DDThh:mm:ss'),
        'duration_minutes': parseInt($(this).find('input[id="durationInput"]').val()),
    };

    $.ajax({
        async: false,
        type: 'POST',
        url: `/api/v1/reservations/`,
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
            alert('Успешно создано');
        },
        error: function (jqXHR, exception) {
            alert(jqXHR.responseText);
        },
    });
}
