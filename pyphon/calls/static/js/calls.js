// Make outgoing calls from the dial_screen.html page

//Grab the phone number and connect using it as a param.
function makeCall() {
    var phoneNumber = '+' + $('#numfield').val()
    console.log('calling' + phoneNumber)
    var params = {"phoneNumber": phoneNumber};
    Twilio.Device.connect(params);

}

//Grab the number from the number field
function addNumber(element){
    $('#numfield').val($('#numfield').val()+element.value);
    console.log($('#numfield').val().length)
}

//Delete a number from the number field
function deleteNumber(element){
    $('#numfield').val($('#numfield').val().slice(0, -1));
}

//Make an outgoing call
$('#call_button').click(function() {
    console.log('outgoing call')
    makeCall();
    $('#incoming').slideDown();
    $(".incoming_call").fadeOut();
    $("#hangupbutton").fadeIn();
});

//End a call
$("#hangupbutton").click(function () {
    Twilio.Device.disconnectAll();
});
