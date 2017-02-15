function getDirection(){

    var direction = d3.event.target.value;
    var url = "/star_data.json/" + direction;
    d3.json(url, printStarData)    
}

d3.select("#directionValues").on("change", getDirection);

function printStarData(starData) {
  // d3 code

  if (d3.select('#d3north').empty()){
    console.log("empty");
  } else{
    d3.selectAll('circle').remove();
  }

    var stars = svgContainer.selectAll("circle")
                            .data(starData)
                            .enter()
                            .append('circle');
      console.log(stars);

    var starAttributes = stars
                        .attr('cx', function(d) {return d.x})
                        .attr('cy', function(d) {return d.y})
                        .attr('r', function(d) {return 5-d.magnitude})
                        .attr("fill", function(d) {return d.color})
                        .on('click', function() {console.log('yo');});

    $('circle').on('click', function() {console.log('yo')})

}


var svgBodySelection = d3.select("#d3north");

var svgContainer = svgBodySelection.append("svg")
                                   .attr("width", 800)
                                   .attr("height", 600)
                                   .style("fill", "white");


console.log('hiya!');

