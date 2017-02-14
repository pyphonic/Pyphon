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
    console.log('incoming call')
    $('#incoming').slideDown();

    $("#answerbutton").click(function() {
        // Answer call
        connection.accept();
        $(".incoming_call").fadeOut();
        $("#hangupbutton").fadeIn();
    });

    $("#rejectbutton").click(function() {
        // Reject call
        connection.reject();
        $('#incoming').slideUp();
    });
});

/* End a call */
$("#hangupbutton").click(function () {
    Twilio.Device.disconnectAll();
    $('#incoming').slideUp();
    $("#hangupbutton").fadeOut();
    $(".incoming_call").fadeIn();
});
