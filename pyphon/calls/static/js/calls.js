function makeCall() {
    var phoneNumber = '+' + $('#numfield').val()
    console.log('calling' + phoneNumber)
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

$('#call_button').click(function() {
    console.log('outgoing call')
    makeCall();
    $('#incoming').slideDown();
    $(".incoming_call").fadeOut();
    $("#hangupbutton").fadeIn();
});

/* End a call */
$("#hangupbutton").click(function () {
    Twilio.Device.disconnectAll();
});
