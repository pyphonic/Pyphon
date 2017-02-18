// Make outgoing calls from the dial_screen.html page

//Grab the phone number and connect using it as a param.
function makeCall() {
    var phoneNumber = $('#numfield').val()
    console.log('calling ' + phoneNumber)
    var params = {"phoneNumber": phoneNumber};
    Twilio.Device.connect(params);

}

//Grab the number from the number field
function addNumber(element){
    $('#numfield').val($('#numfield').val()+element.value);
}

//Delete a number from the number field
function deleteNumber(element){
    $('#numfield').val($('#numfield').val().slice(0, -1));
}

//Make an outgoing call
$('#dial_button').click(function() {
    console.log('outgoing call')
    makeCall();
    var phone_number = $('#numfield').val();
    $("#hangupbutton").show();
    $('#incoming').slideDown();
    $('#numfield').val('')
    $.get('/api/contacts/list/', function(data) {
        var thisContact = data.filter(function(contact) {
            return contact.number === '+' + phone_number;
        });
        if (thisContact.name) {
            $("#contact").text(thisContact[0].name);
        } else {
            $("#contact").text(phone_number);
        }
    });
});
