// Module for calling the Text api and printing out its results.


'use strict';


function textData(text){
    this.time = new Date(text.time);
    this.body = text.body;
    this.sender = text.sender;
 };

textData.allTexts = []

textData.callAPI = function(){
    //Call the Api to grab recent texts
    $.get('/api/texts', function(data,msg,xhr){
        textData.allTexts = data.map(function(data,idx,array){
          return new textData(data);
        });
        textData.renderData(textData.allTexts.slice(textData.allTexts.length-10));
    });
};

textData.renderData = function(textsArray){
    //Take all of the texts and render them to the page.
    // all_texts = textsArray.sort(function(a, b){
    //   return b.time - a.time;
    // });
    $('#past_texts .message').remove();
    // textsArray.map(function(data){
    //     $('#past_texts').append(textData.renderMessage(data));
    // });
    for (var i=0; i<textsArray.length; i++){
        var message = textsArray[i];
        var mes_in_temp = textData.renderMessage(message);
        var appendTo = $('#past_texts');
        appendTo.append(mes_in_temp);
    };
}

textData.renderMessage = function(data){
    var source = $('#text-template').html();
    var template = Handlebars.compile(source);
    return template(data);
};

setInterval(textData.callAPI, 5000);


//This is stolen from learning journal, rewrite to post text.
$(document).ready(function(){
    var form = $("form");
    form.submit(function(e){
        e.preventDefault();
        $.ajax({
            url: '/texts',
            type: "POST",
            data:{
                // "csrf_token": $(this).parent().find("input[name='csrf_token']")[0].value,
                "body": body
            },
            success: function(){
            //     var href = $('h2 a').attr('href').split('/').slice(1);
            //     var new_post_id = Number(href[1]) + 1;
            //     var new_post_href = href[0] + '/' + new_post_id.toString();
            //     post_template = '<h2><a href="' + new_post_href + '">' + title + '</a></h2>'+
            //         '<p class="lead">by <a href="/about_me">Julien Wilson</a></p>'+
            //         '<p><span class="glyphicon glyphicon-time"></span> Posted Just Now</p>'+
            //         '<br/>'
            //     $('#posts').prepend(post_template);
                $('form')[0].reset();
            },
            error: function(err){
                console.error(err);
                alert("This is a problem", err.message);
            }
        });       
    });
});
