$(function(){
  $('#data-information.btn.dropdown-button span').click(function(){
        $('#data-information ul#dropdown2').show(); 
    });
    $('#data-information ul#dropdown2 li a').click(function(e){
         $('#data-information span').text($(this).text());
         $('#data-information ul#dropdown2').hide();

         data = {data: $('#data-information span').text()};

         $.ajax({
            url: '/load_date_data',
            data: JSON.stringify(data),
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            success: function(response) {
                console.log(response);
                //  Render checkboxes...To select the paths to be drawn
            },
            error: function(error) {
                console.log(error);
            }
        });

        e.preventDefault();
    });
})