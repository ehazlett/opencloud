function flash(text, status){
  var msg = $("<div class='alert'></div>");
  msg.addClass('alert-'+status);
  msg.append("<a class='close' href='#' data-dismiss='alert'>x</a>");
  msg.append('<p>'+text+'</p>');
  $("#messages").append(msg);
  $("#messages").removeClass('hide');
  $(".alert").alert();
  $(".alert").delay(5000).fadeOut();
}
