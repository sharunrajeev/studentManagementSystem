$(document).ready(function()
    {
        $('#butn').click(() => {
            var name = $('#name').val()
            var age =  $('#age').val()
            var gender = $('input[name="Gender"]:checked').val()
            var address =  $('#address').val()
            var mob = $('#mob').val()
            var email =$('#email').val()
            var department = $('#dept').val()
            var university = $('#university').val()
            var dob = $('#dob').val()
            var phd_reg = $('#phd_reg').val()
            var phd_joining_date = $('#phd_joining_date').val()
            var research_topic = $('#research_topic').val()
            var research_guide = $('#research_guide').val()
            var guide_mail = $('#guide_mail').val()
            var guide_phone = $('guide_phone').val()


            var data ={
                'csrfmiddlewaretoken':'{{csrf_token}}',
                'Name':name,
                'Age':age,
                'Gender':gender,
                'Address':address,
                'Mob':mob,
                'Email':email,
                'Department':department,
                'University':university,
                'Dob':dob,
                'Phd_Reg':phd_reg,
                'Phd_Joining_Date':phd_joining_date,
                'Research_Topic':research_topic,
                'Research_Guide':research_guide,
                'Guide_Mail':guide_mail,
                'Guide_Phone': guide_phone
            }


            $.ajax({
                url:'register',
                type: 'POST',
                data:data,
                dataType: 'json',
                success:function(data){

                    if(data.success=="pass"){
                        console.log("success")
                        window.location.replace('regSuccess')
                    }else{
                        console.log("error")
                       $("#error").html("Email already exists!!");
                    }
                }
            })



})
})

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
