$(document).ready(function() {
    $.get("/calls/token", {forPage: window.location.pathname}, function(data) {
        // Set up the Twilio Client Device with the token
        Twilio.Device.setup(data.token);
    });
});

function makeCall() {
    var phoneNumber = '+' + $('#numfield').val()
    var params = {"phoneNumber": phoneNumber};
    Twilio.Device.connect(params);
}

function addNumber(element){
    $('#numfield').val($('#numfield').val()+element.value);
    console.log($('#numfield').val().length)
}

function deleteNumber(element){
    $('#numfield').val($('#numfield').val().slice(0, -1));
}


// Twilio.Device.incoming(function(connection) {
//     updateCallStatus("Incoming support call");

//     // Set a callback to be executed when the connection is accepted
//     connection.accept(function() {
//         updateCallStatus("In call with customer");
//     });

//     // Set a callback on the answer button and enable it
//     answerButton.click(function() {
//         connection.accept();
//     });
//     answerButton.prop("disabled", false);
// });