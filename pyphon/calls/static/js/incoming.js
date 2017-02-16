//Receive incoming calls on any page.

/* Get a Twilio Client token with an AJAX request */
$(document).ready(function() {
    $.get("/calls/token", {forPage: window.location.pathname}, function(data) {
        // Set up the Twilio Client Device with the token
        console.log("Got token");
        Twilio.Device.setup(data.token);
    });
});

Twilio.Device.ready(function(device){
    // Get device ready to receive incoming calls.
    console.log("Twilio.Device is now ready for connections");
});

Twilio.Device.incoming(function(connection) {
    // Receive incoming call, slide down call screen.
    console.log('incoming call');
    $(".incoming_call").show();

    var phone_number = connection.parameters.From.slice(1)
    $.get('/api/contacts/number/' + phone_number, function(thisContact) {
        if (thisContact.name) {
            $("#contact").text(thisContact.name);
        } else {
            $("#contact").text(phone_number);
        }
        $('#incoming').slideDown();
    });

    $("#answerbutton").click(function() {
        // Answer call
        connection.accept();
        $(".incoming_call").hide();
        $("#hangupbutton").fadeIn();
    });

    $("#rejectbutton").click(function() {
        // Reject call
        connection.reject();
        $('#incoming').slideUp();
        $(".incoming_call").hide();
    });

});

/* End a call */
$("#hangupbutton").click(function () {
    Twilio.Device.disconnectAll();
});

Twilio.Device.disconnect(function() {
    $('#incoming').slideUp();
    $("#hangupbutton").hide();
})
