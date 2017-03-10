/**
 * Created by yosi on 3/9/2017.
 */
function simpleCountBarPlot(parentElementId, data, orient) {
    var chart = d3.select("#" + parentElementId)
        .append("svg");

    var chartWidth = $("#" + parentElementId).width(),
        tableSize = data.length,
        barPadding = 7,
        namePadding, countPadding, chartHeight,
        leftPadding, barLengthAttr, barWidthAttr,
        countAxis, nameAxisLength, barGTransform;

    var maxCount = 0;
    for (var i in data) {
        if (data[i].count > maxCount) {
            maxCount = data[i].count;
        }
    }

    var barLengthScale = d3.scaleLinear()
        .domain([0, maxCount]);

    if (orient == "vertical") {
        namePadding = 145;
        countPadding = 60;
        chartHeight = tableSize * 25;
        leftPadding = 0;
        barLengthAttr = "width";
        barWidthAttr = "height";
        countAxis = "x";
        barLengthScale
            .range([0, chartWidth - countPadding - namePadding]);
        nameAxisLength = chartHeight;
        barGTransform = function(d,i) {
            return "translate(0," +
                (chartHeight / tableSize * i) + ")";
        };
    }
    else {
        namePadding = 140;
        countPadding = 60;
        chartHeight = 370;
        leftPadding = 30;
        barLengthAttr = "height";
        barWidthAttr = "width";
        countAxis = "y";
        barLengthScale
            .range([0, chartHeight - countPadding - namePadding]);
        nameAxisLength = chartWidth;
        barGTransform = function(d, i) {
            return "translate("  + (leftPadding +
                    (chartWidth - leftPadding) / tableSize * i) + ","  +
                    (chartHeight - namePadding - barLengthScale(d.count)) + ")";
        };
    }


    chart.attr("class", "chart")
        .attr("width", chartWidth)
        .attr("height", chartHeight);

    var barGroups = chart.selectAll("g")
        .data(data)
        .enter().append("g")
            .attr("transform", barGTransform);

    var rects = barGroups.append("rect")
        .attr(barLengthAttr, function(d) {
            return barLengthScale(d.count);
        })
        .attr(barWidthAttr, nameAxisLength / tableSize - barPadding)
        .style("fill", "red");

    var countText = barGroups.append("text")
        .text(function(d) {
            return d.count;
        });

    var nameText = barGroups.append("text")
        .text(function (d, i) {
            return d.name;
        })
        .style("font-weight", "bold");

    if (orient == "vertical") {
        nameText.attr("y", (chartHeight / tableSize) / 2);
        rects.attr(countAxis, namePadding);
        countText
            .attr("x", function (d) {
            return namePadding + barLengthScale(d.count) + 5;
        })
        .attr("y", (chartHeight / tableSize) / 2);
    }
    else {
        countText.attr("transform", "translate(5,-3) rotate(-45)");
        nameText.attr("transform", function(d) {
                return "translate(12," + (barLengthScale(d.count) + 5) + ") " + "rotate(-70)";
            })
            .style("text-anchor", "end");
    }
}

function comparePlot(data, parentElementId) {
   var tableLength = data.length,
       chartWidth = $("#" + parentElementId).width(),
       chartHeight = 350,
       namePadding = 140;

   var x0 = d3.scaleBand()
       .range([0, chartWidth - 40])
       .paddingInner(0.1);
   var uniqueNames = Array.from(new Set(data.map(function(x) {return x.name;})));
   x0.domain(uniqueNames);

   var x1 = d3.scaleBand()
       .padding(0.05)
       .paddingInner(0.05);
   var journals = Array.from(new Set(data.map(function(x) {return x.journal;})));
   x1.domain(journals)
       .range([0, x0.bandwidth()]);

   var y = d3.scaleLinear()
    .range([0, chartHeight - namePadding])
    .domain([0,1]);

   var z = d3.scaleOrdinal()
       .range(["#98abc5", "#8a89a6", "#7b6888", "#6b486b",
       "#a05d56", "#d0743c", "#ff8c00"].reverse())
       .domain(journals);

   var chart = d3.select("#" + parentElementId).append("svg")
       .attr("width", chartWidth)
       .attr("height", chartHeight)
       .style("padding-left", "30px");

   var barGroups = chart.selectAll("g")
       .data(data)
       .enter()
       .append("g")
            .attr("transform", function(d) {
                return "translate(" + x0(d.name) + ",0)";
            });

   barGroups.append("rect")
       .attr("x", function(d) {
           return x1(d.journal);
       })
       .attr("width", x1.bandwidth())
       .attr("height", function(d) {
           return y(d.rel);
       })
       .attr("y", function(d) {
           return chartHeight - namePadding - y(d.rel);
       })
       .attr("fill", function(d) {
           return z(d.journal);
       });

   barGroups.append("text")
       .text(function (d) {
           return d.name;
       })
       .attr("transform", function(d) {
                return "translate(" +
                    (x0.bandwidth()/2 + 4) + "," +
                    (chartHeight - namePadding + 10) +
                    ") " + "rotate(-70)";
            })
       .style("text-anchor", "end")
       .style("font", "14px sans-serif")
       .style("font-weight", "bold");

   var legend = chart.append("g")
       .attr("transform", "translate(" + (chartWidth-120) +",0)");

   var legendEnts = legend.selectAll("g")
       .data(journals)
       .enter()
       .append("g")
            .attr("transform", function(d,i) {
                return "translate(0," + (10 + 20*i) +")";
            });

   legendEnts.append("rect")
       .attr("width", 16)
       .attr("height", 16)
       .attr("fill", function(d) {
           return z(d);
       });

    legendEnts.append("text")
        .attr("x", 22)
        .attr("y", 13)
        .text(function(d) {return d;})
        .style("font", "14px sans-serif");
}
