/* Get a Twilio Client token with an AJAX request */
$(document).ready(function() {
    $.get("/calls/token", {forPage: window.location.pathname}, function(data) {
        // Set up the Twilio Client Device with the token
        console.log("Got token");
        Twilio.Device.setup(data.token);
    });
});

// /* Report any errors to the call status display */
// Twilio.Device.error(function (error) {
//     updateCallStatus("ERROR: " + error.message);
// });

Twilio.Device.ready(function(device){
    console.log("Twilio.Device is now ready for connections");
});

Twilio.Device.incoming(function(connection) {
    console.log('incoming call')
    $('#incoming').slideDown();

    $("#answerbutton").click(function() {
        connection.accept();
        // $("#hangupbutton").fadeIn();
        // $(".incoming_call").fadeOut();
    });

    $("#rejectbutton").click(function() {
        connection.reject();
        $('#incoming').slideUp();
    });
});
/* End a call */
$("#hangupbutton").click(function () {
    Twilio.Device.disconnectAll();
});
