$.get("/calls/token", {forPage: window.location.pathname}, function(data) {
    // Set up the Twilio Client Device with the token
    Twilio.Device.setup(data.token);
});

Twilio.Device.incoming(function(connection) {
    updateCallStatus("Incoming call");
    $('#incoming').slideDown();

    // Set a callback to be executed when the connection is accepted
    connection.accept(function() {
        updateCallStatus("Call accepted.");

    });

    // Set a callback on the answer button and enable it
    answerButton.click(function() {
        connection.accept();
    });
    answerButton.prop("disabled", false);
});