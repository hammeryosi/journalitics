function countBarChart(data, elementId) {
    var maxCount = data.count.reduce(function(a,b) {return Math.max(a,b);});
    var xScale = d3.scaleLinear()
        .domain([0, maxCount])
        .range([namePadding,
            chartWidth - countPadding - namePadding]);
    var barTr = d3.transition()
        .duration(200);
    var numTr = d3.transition()
        .duration(150)
        .delay(150);

    var chart = d3.select("#" + elementId)
        .attr("width", chartWidth)
        .attr("height", chartHeight);

    var barGroups = chart.selectAll("g")
        .data(data.count)
        .enter().append("g")
            .attr("transform", function(d, i) {
                return "translate(0,"  + chartHeight / tableSize * i + ")";
            });

    barGroups.append("rect")
        .attr("height", chartHeight / tableSize - barPadding)
        .attr("x", namePadding)
        .transition(barTr)
            .attr("width", xScale);

    barGroups.append("text")
        .text(function(d) {
            return d;
        })
        .attr("y", 13)
        .attr("x", function (d) {
            return xScale(d) + namePadding + 5
        })
        .style("opacity", 0.)
        .transition(numTr)
            .style("opacity", 1.);

    barGroups.append("text")
        .text(function (d, i) {
            return data.names[i];
        })
        .attr("class", "bar-name-label")
        .attr("y", 13);
}