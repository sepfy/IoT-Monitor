function LineChart(id) {
  this.width = 400;
  this.height = 200;
  this.id = id;
}

LineChart.prototype.init = function() {
  this.dataset = [];
  this.margin = 50;
  console.log(this.id);
  this.svg = d3.select(this.id)
    .append('svg')
    .attr('width', this.width + 2*this.margin )
    .attr('height', this.height + 2*this.margin)

//    this.svg.append('text').attr('x', 10).attr('y', this.margin/2).style('fill', 'steelblue').style('font-size', '24px').style('font-weight', 'bold').text("溫度");

  this.svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(" + this.margin + "," + (this.margin+this.height) + ")")
    this.svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(" + this.margin + ", "+this.margin+")")

    this.svg.append('g')
    .append('path')
    .attr('class', 'line')
    .attr("transform", "translate(" + this.margin + ", "+this.margin+")")
    .attr('fill', 'none')
    .attr('stroke-width', 3)
    .attr('stroke', '#CD5C5C');

  this.svg.append("g")
    .attr("class", "dot");
}

LineChart.prototype.update = function(new_data) {
  this.dataset = this.dataset.concat([[Date.parse(new_data[0]), new_data[1]]]);
  //console.log(this.dataset);
  this.draw();
}

LineChart.prototype.draw = function() {

  if(this.dataset.length > 20)
    this.dataset.shift();

  var min = d3.min(this.dataset, function(d) { return d[1];})
    var max = d3.max(this.dataset, function(d) { return d[1];})
    var xScale = d3.scaleTime()
    .domain([this.dataset[0][0], this.dataset[this.dataset.length-1][0]])
    .range([0, this.width]);
  var yScale = d3.scaleLinear().domain([min, max]).range([this.height, 0]);
  var xAxis = d3.axisBottom();
  var yAxis = d3.axisLeft();
  var linePath = d3.line()
    .x(function(d){ return xScale(d[0]) })
    .y(function(d){ return yScale(d[1]) })
    .curve(d3.curveMonotoneX);
  this.svg.select(".x.axis")
    .call(d3.axisBottom(xScale)); 
  this.svg.select(".y.axis")
    .call(d3.axisLeft(yScale)); 
  this.svg.select(".line")
    .transition()
    .duration(800)
    .attr("d", linePath(this.dataset))
    //.attr("d", linePath(this.dataset.slice(-2, -1)))
    //console.log(this.dataset.slice(-2, -1));

    var m = this.margin;
  d3.selectAll(".circle").remove();
  var dot = this.svg.selectAll(".dot");
  dot.data(this.dataset)
    .enter()
    .append("circle") // Uses the enter().append() method
    .attr("class", "circle")
    .attr("cx", function(d) { return xScale(d[0])+m })
    .attr("cy", function(d) { return yScale(d[1])+m })
    .transition()
    .delay(500)
    .attr("r", 5)
    .attr("fill", "#DC143C")


}


