// Module for calling the Text api and printing out its results.


'use strict';


textData = {}



textData.callAPI = function(){
    //Call the Api to grab recent texts
    $.get('/api/texts', function(data,msg,xhr){
      var lastMod = xhr.getResponseHeader('Last-Modified');
      localStorage.setItem('lastMod', lastMod);
      localStorage.setItem('allIncidents', JSON.stringify(data));
      var newdataarray = data.map(function(elem,idx,array){
        return new policeData(elem);
      });
      policeData.loadData(newdataarray);
      policeData.buildDatabase();
    });
    };
