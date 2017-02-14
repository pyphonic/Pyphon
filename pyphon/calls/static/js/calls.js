function addNumber(element){
    $('#numfield').val($('#numfield').val()+element.value);
    console.log($('#numfield').val().length)
}

function deleteNumber(element){
    $('#numfield').val($('#numfield').val().slice(0, -1));
}
