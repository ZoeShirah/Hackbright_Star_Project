//set up
var my_canvasN = document.getElementById("myCanvasN");
context = my_canvasN.getContext("2d");

//gradient square
 var gradient = context.createLinearGradient(0, 0, 0, 630);
   gradient.addColorStop(0, '#000080');
   gradient.addColorStop(0.5, '#0000A0');
   gradient.addColorStop(1, '#488AC7');
   
 context.fillStyle = gradient;
 context.fillRect(0, 0, 1260, 630);

// var my_canvasE = document.getElementById("myCanvasE");
// context = my_canvasE.getContext("2d");
   
//  context.fillStyle = gradient;
//  context.fillRect(0, 0, 1260, 630);

// var my_canvasS = document.getElementById("myCanvasS");
// context = my_canvasS.getContext("2d");
   
//  context.fillStyle = gradient;
//  context.fillRect(0, 0, 1260, 630);

// var my_canvasW = document.getElementById("myCanvasW");
// context = my_canvasW.getContext("2d");
   
//  context.fillStyle = gradient;
//  context.fillRect(0, 0, 1260, 630);