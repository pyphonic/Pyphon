prev = ''
queryTwilio = function(){
    //Call the Api to grab recent texts
    $.get('/api/texts/last/', function(data,msg,xhr){
        if data.time != prev:
            prev = data.time
            $('#text_alert').slideDown()
            setTimeout(function(){
                $('#text_alert').slideUp()
            }, 2000);
    });
};



setInterval(queryTwilio, 10000);