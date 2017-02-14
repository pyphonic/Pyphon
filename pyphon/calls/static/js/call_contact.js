// Make outgoing calls from the contact detail page

//Grab the phone number and connect using it as a param.
function makeCall() {
    var phoneNumber = $('#callme').text()
    console.log('calling' + phoneNumber)
    var params = {"phoneNumber": phoneNumber};
    Twilio.Device.connect(params);

}

//Make an outgoing call
$('#call_button').click(function() {
    console.log('outgoing call')
    makeCall();
    var name = $('#name').text()
    var phone_number = $('#callme').text()
    $('#incoming').slideDown();
    if (name == "No Name"){
        $("#contact").text(phone_number);
    } else {
        $("#contact").text(name);
    }
    $("#hangupbutton").fadeIn();
});
