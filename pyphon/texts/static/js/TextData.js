// Module for calling the Text api and printing out its results.


'use strict';


function textData(text){
    this.body = text.body;
    this.sender = text.sender;
    this.contact = text.contact;
    var time = new Date(text.time);
    var today = new Date();
    if (time.getDate() === today.getDate()) {
        this.time = time.toLocaleTimeString('en-US');
    } else {
        this.time = time.toLocaleDateString('en-US');
    }
 };

textData.allTexts = []

textData.callAPI = function(callback){
    //Call the Api to grab recent texts
    var scroll = false;
    $.get('/api/texts', function(data,msg,xhr){
        textData.allTexts = data.map(function(data,idx,array){
            return new textData(data);
        });

        var Contacts_texts_only = textData.allTexts.filter(function(value){
            return value.contact == window.location.href.split('/')[5]
        })
        if ($('.message').length === 0) {
            scroll = true;
        }
        textData.renderData(Contacts_texts_only);//.slice(textData.allTexts.length-20));
        if (scroll) {
            var message_container = $('#past_texts');
            message_container.scrollTop(message_container.prop("scrollHeight"));
        }
        if (callback) callback();
    })
};

textData.renderData = function(textsArray){
    //Take all of the texts and render them to the page.

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
    // var message_container = $('#past_texts');
    // message_container.scrollTop(message_container.prop("scrollHeight"));
    textData.callAPI()
    var form = $("form");

    // form.on('submit', function(e){
    //     e.preventDefault();

    //     $.ajax({
    //         url: window.location.href,
    //         type: "POST",
    //         data: form.serialize(),

    //         success: function(){
    //             console.log('The text was sent!')
    //             form[0].reset();
    //         },
    //         error: function(err){
    //             console.log(err.responseText)
    //             console.error(err);
    //             alert("This is a problem", err.responseText);
    //         }
    //     });
    // });
});