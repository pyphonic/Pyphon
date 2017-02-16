var prev = "";

$(document).ready(function() {
    $.get("/api/texts/last/", function(text) {
        prev = text.time;
    });
});

function queryTwilio() {
    $.get("/api/texts/last/", function(text) {
        if (text.time !== prev && text.sender === 'them') {
            prev = text.time;
            $.get('/api/contacts/get/' + text.contact, function(contact) {
                $text_alert = $('#text_alert');
                if (contact.name) {
                    $text_alert.find("#text_contact").text(contact.name);
                } else {
                    $text_alert.find("#text_contact").text(contact.number);
                }
                $text_alert.find("#text_content").text(text.body);
                $text_alert.find("#alert_link").attr('href', '/texts/contact/' + text.contact)
                $text_alert.slideDown();
                setTimeout(function(){
                    $text_alert.slideUp();
                }, 4000);
            });
        }
    });
};



setInterval(queryTwilio, 10000);