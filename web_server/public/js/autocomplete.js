$(document).ready(function(){

  // insert html elements under search bar
  function insertAutocomplete(array) {
    var ele_string = '';
    for (var i = 0; i < array.length; i++) {
      ele_string += '<li><span>' + array[i] + '</span></li>';
    }
    $("#autocomplete").html(ele_string);
  }

  $("#search_text").keyup(function(event) {
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

  $("ul#autocomplete").on('click', 'li', function(event) {
    var text = $(this).children().text();
    $('#search_text').val(text);
    $('#autocomplete').html("");
    $('#search_text').focus();
  });

});
