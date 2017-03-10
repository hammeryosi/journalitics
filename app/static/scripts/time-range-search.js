var data = null, gotData = false;
var journalAbbr = {"NYT": "New York Times",
    "WSJ": "Wall Street Journal",
    "NYDN": "New York Daily News",
    "NYP": "New York Post"};

$(document).ready(function () {
    $("#loading-anim").hide();
});

function makePlotPanels(n) {
    var plotsInRow = 2,c= 0,
        rows = Math.ceil(n / plotsInRow), currentRow,
        plotBlock = $("#plot-block");
    plotBlock.append("<div class='panel panel-default' id='compare-plot-panel'></div>");
    for (var r = 0; r < rows; r++) {
        currentRow = plotBlock.append("<div class='row' id='plot-row-" + (r+1) + "'></div>")
        for (var p = 0; p < plotsInRow; p++) {
            if (c < n) {
                currentRow.append(
                    "<div class='col-sm-" + Math.round(12 / plotsInRow)+ "'>" +
                        "<div class='panel panel-default' id='bar-plot-panel-" + (c + 1) +
                    "'></div></div>"
                );
            }
            c++;
        }
    }
}

function makeBarPlots() {
    $("#plot-block").empty();
    var startDate = $("#start-date-input").val(),
        endDate = $("#end-date-input").val(),
        url = $SCRIPT_ROOT + "/people-for-time-range_" +
            startDate + "_" + endDate;
    if (startDate != "" && endDate != "" && endDate >= startDate) {
        $("#loading-anim").show();
        $.getJSON(url, function(res) {
            $("#loading-anim").hide();
            data = res.result;
            gotData = true;
            var l = data.journals.length;
            makePlotPanels(l);
            $("#compare-plot-panel").append(
                "<div class='panel-heading'>Number of mentions relative to max</div>" +
                "<div class='panel-body' id='compare-chart'></div>"
            );
            comparePlot(data.compare, "compare-chart");
            for (var i=0; i< l; i++) {
                var j = data.journals[i];
                $("#bar-plot-panel-" + (i + 1)).append(
                    "<div class='panel-heading'>" + journalAbbr[j] + "</div>" +
                    "<div class='panel-body' id='bar-plot-chart-" + j + "'></div>"
                );
                simpleCountBarPlot("bar-plot-chart-" + j ,
                    data.journalCounts[i], "horizontal");
            };
            $(window).resize(redrawPlots);
        });
    }
}

function redrawPlots() {
    $("[id*=chart]").empty();
    comparePlot(data.compare, "compare-chart");
    for (var i=0;i<data.journals.length;i++) {
        j = data.journals[i];
        simpleCountBarPlot("bar-plot-chart-" + j ,
                    data.journalCounts[i], "horizontal");
    }
}

