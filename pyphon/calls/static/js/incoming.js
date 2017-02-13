$(document).ready(function() {
    $.get("/calls/token", {forPage: window.location.pathname}, function(data) {
        // Set up the Twilio Client Device with the token
        console.log("Got token");
        Twilio.Device.setup(data.token);
    });
});

// Twilio.Device.ready(function(device){
//     console.log("Twilio.Device is now ready for connections");
// });
// Twilio.Device.incoming(function(connection) {
//     console.log('incoming call')
//     $('#incoming').slideDown();

//     // Set a callback on the answer button and enable it
//     $("#answerbutton").click(function() {
//         connection.accept();
//     });
// });