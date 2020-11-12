

    $('#btnPlace').on('click', function(event) {
        event.preventDefault();
        //alert("ajax")
        place= $('#placename').val()
        alert(place)
        // $.ajax({
        //     data : {
        //         placename:place
        //        // placename : $('#placename').val()
               
        //     },
        //     type : 'POST',
        //     url : '/insertplace'
        // })
       
        // .done(function(data) {
        //     if (data.error) {
        //         $('#errorAlert').text(data.error).show();
        //         $('#successAlert').hide();
        //     }
        //     else {
        //         $('#successAlert').text(data.name).show();
        //         $('#errorAlert').hide();
        //     }
        // });
        $.ajax({
            url: "/insertplace",
              data: { 'placename':place
               // 
          },
          
          type: "POST",
          success: function(data) {
            console.log(data)
            
          },
    
          error: function(xhr) {
           
          }
      });
        
    });