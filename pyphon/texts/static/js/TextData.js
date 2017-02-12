// Module for calling the Text api and printing out its results.


'use strict';


var textData = {}

textData.allTexts = []

textData.callAPI = function(){
    //Call the Api to grab recent texts
    $.get('/api/texts', function(data,msg,xhr){
      localStorage.setItem('allTexts', JSON.stringify(data));
      console.log(data);
      return data;
      });
    };
    
textData.renderData