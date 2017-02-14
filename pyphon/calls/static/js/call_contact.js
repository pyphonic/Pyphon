// Make outgoing calls from the contact detail page

//Grab the phone number and connect using it as a param.
function makeCall() {
    var phoneNumber = $('#callme').val()
    console.log('calling' + phoneNumber)
    var params = {"phoneNumber": phoneNumber};
    Twilio.Device.connect(params);

}

//Make an outgoing call
$('#call_button').click(function() {
    console.log('outgoing call')
    makeCall();
    var name = $('#name').val()
    var phone_number = $('#callme').val()
    $('#incoming').slideDown();
    if (thisContact.name) {
        $("#contact").text(thisContact[0].name);
    } else {
        $("#contact").text(phone_number);
    }
    });
    $("#hangupbutton").fadeIn();
});
