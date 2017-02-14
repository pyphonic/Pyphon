function makeCall() {
    var phoneNumber = '+' + $('#phone_number').text()
    console.log('calling' + phoneNumber)
    var params = {"phoneNumber": phoneNumber};
    Twilio.Device.connect(params);
}

/* End a call */
function hangUp() {
    Twilio.Device.disconnectAll();
}

Twilio.Device.ready(function(device) {
    makeCall();
});