$(document).ready(function(){
  //- autocomplete
  function insertAutocomplete(array) {
    var ele_string = '';
    for (var i = 0; i < array.length; i++) {
      ele_string += '<li><span>' + array[i] + '</span></li>';
    }
    $("#autocomplete").html(ele_string);
  }

  $(document).on('keyup', '#search_text', function() {
    var query = $(this).val();
    var getting = $.get('/autocomplete', {
      query: query
    });

    getting.done(function(response) {
      console.log(response);
      if (response.length > 0) {
        insertAutocomplete(response);
      } else {
        $('#autocomplete').html("");
      }
    });
  });

  $(document).on('click', 'ul#autocomplete > li', function(event) {
    var text = $(this).children().text();
    $('#search_text').val(text);
    $('#autocomplete').html("");
    $('#search_text').focus();
  });

  // There is some problem here.
  // $(document).on('blur', '#search_text', function(event) {
  //   console.log(event);
  //   $('#autocomplete').html("");
  // });

});
