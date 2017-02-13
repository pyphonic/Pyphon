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


/* End a call */
function hangUp() {
    Twilio.Device.disconnectAll();
}