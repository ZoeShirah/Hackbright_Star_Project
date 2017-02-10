d3.json('/star_data.json', printStarData);

function printStarData(starData) {
  // d3 code
  console.log(starData);

    var stars = svgContainer.selectAll("circle")
                            .data(starData)
                            .enter()
                            .append('circle');


    var starAttributes = stars
                        .attr('cx', function(d) {return d.x})
                        .attr('cy', function(d) {return d.y})
                        .attr('r', function(d) {return 0.5})
                        // .attr('r', function(d) {return 6-d.magnitude})
}


var svgBodySelection = d3.select("#d3north");

var svgContainer = svgBodySelection.append("svg")
                                   .attr("width", 1260)
                                   .attr("height", 630)
                                   .style("fill", "white");


// var circleSelection = svgSelection.append("circle")
//                                   .attr("cx", 25)
//                                   .attr("cy", 25)
//                                   .attr("r", 25)
//                                   .style("fill", "purple");

console.log('hiya!');

