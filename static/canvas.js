//set up
var my_canvas = document.getElementById("myCanvas");
context = my_canvas.getContext("2d");

//gradient square
 var gradient = context.createLinearGradient(0, 0, 0, 600);
   gradient.addColorStop(0, '#000080');
   gradient.addColorStop(0.5, '#0000A0');
   gradient.addColorStop(1, '#488AC7');
   
 context.fillStyle = gradient;
 context.fillRect(0, 0, 400, 600);

