"use strict";

function getDirection(){

    var direction = d3.event.target.value;
    var url = "/star_data.json/" + direction;
    d3.json(url, printStarData)    
}

d3.select("#directionValues").on("change", getDirection);

function printStarData(starData) {
  // d3 code


  if (d3.select('#d3starfield').empty()){
    console.log("empty");
  } else{
    d3.selectAll('circle').remove();
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
                          return tooltip.style("visibility", "visible");
                          })
                        .on("mousemove", function(){
                          return tooltip.style("top", (d3.event.pageY-50)+"px")
                                        .style("left",(d3.event.pageX+25)+"px");
                          })
                        .on("mouseout", function(){
                          return tooltip.style("visibility", "hidden");
                          });
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

