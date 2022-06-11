
//     $(document).ready(function(){
//     $("#email").change(function () {
//       var email_validation = $(this).val();
//
//       $.ajax({
//         url: '/validate_email/',
//         data: {
//           'email': email_validation
//         },
//         dataType: 'json',
//         success: function (data) {
//           if (data.is_taken) {
//             // alert("A user with this username already exists.");
//             $('#email').val("");
//           }
//         }
//       });
//
//     });
// });

$(document).ready(function(){
    $("#next").click(function () {
      var username = $('#email').val();

      $.ajax({
        url: '/validate_email/',
        data: {
          'email': username
        },
        dataType: 'json',
        success: function (data) {
          if (data.is_taken) {
            alert("A user with this username already exists.");
          }
        }
      });

    });
});
