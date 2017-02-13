
function getDirection(){

    var direction = d3.event.target.value;
    console.log("value" + direction)

    var url = "/star_data.json/" + direction;
    console.log(url)
    d3.json(url, printStarData)    
}

d3.select("#directionValues").on("change", getDirection);

function printStarData(starData) {
  // d3 code
  console.log(starData);

  if (d3.select('#d3north').empty()){
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
                        // .attr('r', function(d) {return 0.5})
                        .attr('r', function(d) {return 5-d.magnitude})
}


var svgBodySelection = d3.select("#d3north");

var svgContainer = svgBodySelection.append("svg")
                                   .attr("width", 800)
                                   .attr("height", 600)
                                   .style("fill", "white");


console.log('hiya!');

