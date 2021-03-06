"use strict";

var NorthInfo = null;
var SouthInfo = null;
var EastInfo = null;
var WestInfo = null;
var NorthConsts = null;
var SouthConsts = null;
var EastConsts = null;
var WestConsts = null;

setInfo();
var myVar;

// tests if there are circles in the DOM 4 times per second
var testAppearTmr = setInterval(function() {
    if ($('circle').length) {
        clearInterval(testAppearTmr);
        console.log("here I am!")
        activateMenu();
        myFunction();
    }
}, 250);

function myFunction() {
    myVar = setTimeout(showPage, 3000);
}

function showPage() {
  document.getElementById("loader").style.display = "none";
  document.getElementById("d3starfield").style.visibility = "visible";
}

$(document).ready(function() {
  console.log("ready");
  getDirection();
  getPlanets();
});

function getConstellations(){

  var direction = d3.select('#directionValues').node().value;
  if (direction === 'North'){
    constellate(NorthConsts);
  } else if (direction === 'East'){
    constellate(EastConsts);
  } else if (direction === 'South'){
    constellate(SouthConsts);
  }else if (direction === 'West'){
    constellate(WestConsts);
  }
}

d3.select("#constellations").on("click", getConstellations);

function getDirection(){

    var direction = d3.select('#directionValues').node().value;
    var url = "/star_data.json/" + direction;
    d3.json(url, printStarData);   
}

function getPlanets(){

    var direction = d3.select('#directionValues').node().value;
    console.log(direction)
    var url = "/planet_data.json/" + direction;
    d3.json(url, printPlanetData);   
}

function deactivateMenu(){
  $('#directionValues').attr('disabled', true);
  $('.arrow').addClass('click');
  $('.twoforms').addClass('hidden');
 
  console.log("wait");
}


// activates direction changing after all directions have loaded
function activateMenu(){
  $('#directionValues').removeAttr('disabled');
  $('.arrow').removeClass('click');
  $('.twoforms').removeClass('hidden');
  
  console.log("go");
}


// activates constellation button after constellations have loaded
function activateButton(){
  $('.const').removeAttr('disabled').removeClass('hidden');
  console.log("constellations activated");
}

// preload all the directional and constellation data, set it to variables
function setInfo(){
  deactivateMenu();
  d3.json("/star_data.json/North", function(data){NorthInfo=data;});
  d3.json("/star_data.json/East", function(data){EastInfo=data;});
  d3.json("/star_data.json/South", function(data){SouthInfo=data;});
  d3.json("/star_data.json/West", function(data){WestInfo=data;});
  d3.json("/constellation_data.json/North", function(data){NorthConsts=data;});
  d3.json("/constellation_data.json/East", function(data){EastConsts=data;});
  d3.json("/constellation_data.json/South", function(data){SouthConsts=data;});
  d3.json("/constellation_data.json/West", function(data){WestConsts=data; setTimeout(activateButton, 2000);});
  console.log("set");
}

// get direction from the menu and display those stars
function getInfo(){
  var direction = d3.select('#directionValues').node().value;
  if (direction === 'North'){
    printStarData(NorthInfo);
    getPlanets();
  } else if (direction === 'East'){
    printStarData(EastInfo);
      getPlanets();
  } else if (direction === 'South'){
    printStarData(SouthInfo);
      getPlanets();
  }else if (direction === 'West'){
    printStarData(WestInfo);
      getPlanets();
  }
}


d3.select("#directionValues").on("change", getInfo);

// get direction value from menu and reset menu and stars to the next direction to the right
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
    getInfo();
}

// get direction value from menu and reset menu and stars to the next direction to the left
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
    getInfo(direction);
}

d3.select(".rarrow").on("click", changeDirectionRight);

d3.select(".larrow").on("click", changeDirectionLeft);

// if the clear button is clicked clear all constellation data
d3.select("#clear").on("click", function (){
  if (d3.select('#d3starfield').empty()){
    console.log("empty");
  } else{
    d3.selectAll('path').remove();
    d3.select('#v_const').selectAll('text').remove()
  }
});

// print out stars to the screen
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
                        .attr('cx', function(d) {return d.x;})
                        .attr('cy', function(d) {return d.y;})
                        .attr('r', function(d) {return 5-d.magnitude;})
                        .attr("fill", function(d) {return d.color;})
                        .on('click', function(d) {
                          console.log('id '+ d.id);})
                        .on('mouseover', function(d){
                          tooltip.text("starID: "+d.id);
                            if (d.hasOwnProperty("name")){
                              tooltip.text(d.name);};
                            if (d.hasOwnProperty("constellations")){
                                tooltip.append("html").html("<p>");
                                tooltip.append("text").text(d.constellations.join(", "));
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


function printPlanetData(planetData) {

    console.log(planetData);

    var planets = svgContainer.selectAll("circle.planet")
                            .data(planetData, function(d){ return d;})
                            .enter()
                            .append("circle")
                            .attr("class", "planet");

    var planetAttributes = planets
                        .attr('cx', function(d) {return d.x;})
                        .attr('cy', function(d) {return d.y;})
                        .attr('r', function(d) {return 5-d.magnitude;})
                        .attr("fill", function(d){return d.color;})
                        .on('mouseover', function(d){
                              tooltip.text(d.name);
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
  var visible = []
  for (var i=0; i<constellation_data["constellations"].length; i++){
    visible.push(constellation_data["constellations"][i].name);}
  var lineList = constellation_data["lines"];
  for (var i=0; i<lineList.length; i++){
    var lineData = lineList[i];
    var lineFunction = d3.line()
                         .x(function(d) { return d.x; })
                         .y(function(d) { return d.y; });

    var lineGraph = svgContainer.append("path")
                              .attr("d", lineFunction(lineData))
                              .attr("stroke", "#fff1b7")
                              .attr("stroke-width", 1)
                              .attr("fill", "none");
  }

  d3.select('#v_const').append("text").text("Constellations").style("font-family","'Tangerine', 'cursive'").style('font-size', '40px')
                       .append('ul').style("font-family","sans-serif").style('font-size', '18px').selectAll('li')
                       .data(visible)
                       .enter().append('li').append('a')
                       .html(function(d){return d;})
                       .on("mouseover", function(d){
                            d3.select('#v_const').append("div").append("img")
                                        .attr("src", "/static/images/"+d+".jpg")
                                        .attr("width", "200px")
                                        .attr("x", -8)
                                        .attr("y", 200);})
                       .on("mouseout", function() {
                            d3.select('#v_const').selectAll("div").remove();
                       });
}

var svgBodySelection = d3.select("#d3starfield");

var svgContainer = svgBodySelection.append("svg")
                                   .attr("width", 800)
                                   .attr("height", 600)
                                   .style("fill", "white");

var tooltip = d3.select(".box")
    .append("div")
    .attr("class", "d3tooltip")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden");

console.log('hiya!');
