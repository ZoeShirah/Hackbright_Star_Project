"use strict";

document.getElementById("directionValues").selectedIndex = -1;


function getConstellations(){

  var direction = d3.select('#directionValues').node().value;
  var url = "/constellation_data.json/"+direction;
  d3.json(url, constellate);
}

d3.select("#constellations").on("click", getConstellations);

function getDirection(){

    var direction = d3.event.target.value;
    var url = "/star_data.json/" + direction;
    d3.json(url, printStarData);   
}

d3.select("#directionValues").on("change", getDirection);

function changeDirectionRight(){
    var direction = d3.select('#directionValues').node().value;
    if (direction === 'North'){
      direction = 'East';
    } else if (direction === 'East'){
      direction = 'South';
    } else if (direction === 'South'){
      direction = 'West';
    }  else if (direction === 'West'){
      direction = 'North';}

    d3.select('#directionValues').property('value', direction);
    var url = "/star_data.json/" + direction;
    d3.json(url, printStarData);
}

function changeDirectionLeft(){
    var direction = d3.select('#directionValues').node().value;
    if (direction === 'North'){
      direction = 'West';
    } else if (direction === 'West'){
      direction = 'South';
    } else if (direction === 'South'){
      direction = 'East';
    }  else if (direction === 'East'){
      direction = 'North';}

    d3.select('#directionValues').property('value', direction);
    var url = "/star_data.json/" + direction;
    d3.json(url, printStarData);
}

d3.select(".rarrow").on("click", changeDirectionRight);

d3.select(".larrow").on("click", changeDirectionLeft);

d3.select("#clear").on("click", function (){
  if (d3.select('#d3starfield').empty()){
    console.log("empty");
  } else{
    d3.selectAll('path').remove();
    d3.select('#v_const').selectAll('text').remove()
  }
});

function printStarData(starData) {
  // d3 code

  if (d3.select('#d3starfield').empty()){
    console.log("empty");
  } else{
    d3.selectAll('circle').remove();
    d3.selectAll('path').remove();
    d3.select('#v_const').selectAll('text').remove()

  }

    var stars = svgContainer.selectAll("circle")
                            .data(starData)
                            .enter()
                            .append('circle');

    var starAttributes = stars
                        .attr('cx', function(d) {return d.x})
                        .attr('cy', function(d) {return d.y})
                        .attr('r', function(d) {return 5-d.magnitude})
                        .attr("fill", function(d) {return d.color})
                        .on('click', function(d) {
                          console.log('id '+ d.id);})
                        .on('mouseover', function(d){
                          tooltip.text("starID: "+d.id);
                            if (d.hasOwnProperty("name")){
                              tooltip.text(d.name);};
                            if (d.hasOwnProperty("constellations")){
                                tooltip.append("html").html("<p>");
                                tooltip.append("text").text("Constellation: "+d.constellations);
                                tooltip.append("html").html("</p>");};
                          return tooltip.style("visibility", "visible");
                          })
                        .on("mousemove", function(){
                          return tooltip.style("top", (d3.event.pageY-200)+"px")
                                        .style("left",(d3.event.pageX-80)+"px");
                          })
                        .on("mouseout", function(){
                          return tooltip.style("visibility", "hidden");
                          });
}


function constellate(constellation_data){
  var visible = [];
  for (var x = 0;x < constellation_data.length; x++){
    var data = constellation_data[x];
    visible.push(data.name);
    var lineList = data.lines;
    for (var i=0; i<lineList.length; i++){
      var lineData = lineList[i];
      var lineFunction = d3.line()
                              .x(function(d) { return d.x; })
                              .y(function(d) { return d.y; });

      var lineGraph = svgContainer.append("path")
                              .attr("d", lineFunction(lineData))
                              .attr("stroke", "yellow")
                              .attr("stroke-width", 1)
                              .attr("fill", "none");
    }
  }

  d3.select('#v_const').append("text")
                       .text(visible.join(', '))
}

var svgBodySelection = d3.select("#d3starfield");

var svgContainer = svgBodySelection.append("svg")
                                   .attr("width", 800)
                                   .attr("height", 600)
                                   .style("fill", "white");

var tooltip = d3.select("#d3starfield")
    .append("div")
    .attr("class", "d3tooltip")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    .text("a simple tooltip");

console.log('hiya!');