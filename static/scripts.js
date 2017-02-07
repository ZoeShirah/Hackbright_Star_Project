//set up
var my_canvas = document.getElementById("myCanvas");
context = my_canvas.getContext("2d");

//gradient square
 var gradient = context.createLinearGradient(0, 0, 0, 150);
   gradient.addColorStop(0, '#00ABEB');
   gradient.addColorStop(1, '#26C000');
   
 context.fillStyle = gradient;
 context.fillRect(250, 10, 130, 130);