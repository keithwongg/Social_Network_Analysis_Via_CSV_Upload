$('#inputGroupFile01').on('change',function(){
    //get the file name
    var fileName = $(this).val();
    fileName = fileName.slice(12, fileName.length);
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
});

// set listeners to centrality buttons
centralityDict = {
    "degCentrality": "Degree of Centrality",
    "eigenvectorCentrality": "Eigenvector Centrality",
    "betweennessCentrality": "Betweenness Centrality",
};
// tbodyDict = {
//   "degCentrality": "#degCentralityTableData",
//   "eigenvectorCentrality": "#eigenCentralityTableData",
//   "betweennessCentrality": "#betweennessCentralityTableData",
// };
[...$('.btn.centrality')].forEach((btn) => {
    // console.log(btn.id);
    $(`#${btn.id}`).on('click', function(){
        
        // Only add button pressed styling to current button that is pressed and remove pressed button styling for other buttons
        $("#centralityButtons * > button").removeClass('buttonPressed');
        $(this).addClass('buttonPressed');

        // Empty table data
        $('#centralityTableData').empty();

        var data = JSON.parse($(`#${btn.id}P`).text());

        // console.log(btn.id);
        render_text = centralityDict[btn.id];
        $('#analyticsTitle').text(render_text);
        $('#centralityTableHeader').text(render_text);
        let topN = $('#topNValue').text();
        console.log(topN);
        $('#topNTitle').text(topN);
        // console.log(data);

        // Get Number of rows from range input
        let numRows = Number($('#topNValue').text());
        let iterCount = 0;

        // get full data from para
        // alter the data in the para
        // parse it back as txt
        let graphDataToSet = JSON.parse($(graphData).text());
        styleList = ['normal', 'height', 'fill'];

        // remove previous styling
        Object.keys(graphDataToSet['nodes']).forEach((key) => {
            if('normal' in graphDataToSet['nodes'][key]){
            delete graphDataToSet['nodes'][key]['normal'];
            } else if('hovered' in graphDataToSet['nodes'][key]){
            delete graphDataToSet['nodes'][key]['hovered'];
            } else if('selected' in graphDataToSet['nodes'][key]){
            delete graphDataToSet['nodes'][key]['selected'];
            };
        });

        Object.keys(data).forEach((key) => {
            var randomColor = "#000000".replace(/0/g,function(){return (~~(Math.random()*16)).toString(16);});

            if(iterCount < numRows){
                // Alter graph data nodes accordingly
                graphDataToSet['nodes'].forEach((node) => {
                    if(node.id === key){
                        node["normal"] = {
                            "height": Number(data[key]*150),
                            "fill": randomColor,
                        };
                        node["hovered"] = {
                            "height": Number(data[key]*150),
                            "fill": "#ffffff",
                        };
                        node["selected"] = {
                            "height": Number(data[key]*150),
                            "fill": "#ffffff",
                        };
                    }
                });
                // get consolidated data from rendered graph
                
                let basketRefer = 0; // Basket data for referring other people
                let basketReceive = 0; // Basket data for using other ppl referrals
                graphDataToSet['edges'].forEach((edge) => {
                    if(key === edge['from']){
                        basketRefer += Number(edge['basket']);
                    };
                });
                graphDataToSet['edges'].forEach((edge) => {
                    if(key === edge['to']){
                        basketReceive += Number(edge['basket']);
                    };
                });
                // append all into the table
                toAppend = `<tr><td>${iterCount+1}</td><td>${key}</td><td>${data[key]}</td><td>${basketRefer}</td><td>${basketReceive}</td></tr>`;
                $('#centralityTableData').append(toAppend);
                iterCount += 1;
            } else {
            console.log('iteration exceeded');
            };
        });
        iterCount = 0;
        graphDataToSet = JSON.stringify(graphDataToSet);
        $(graphData).text(graphDataToSet);
        renderGraph();
    });
});

// Start Button
let start = false;
$('#start').on('click', function(){
    console.log('start', start);
    if(!start){
        start = true;
        $('#start').removeClass('btn-success').text('Stop').addClass('btn-danger');
        $('#startStopText').text('Recording Filtered Data Rendered In The Table Below. Press Again to STOP.');
        return start = true;
    }else {
        $('#dataExportBody').empty();
        $('#start').removeClass('btn-danger').text('Start').addClass('btn-success');
        $('#startStopText').text('Press To Start Recording Filtered Data.');
        $.ajax({
            url: "resetCSV/",
            method: 'POST', // or another (GET), whatever you need
            data: {
                clearCSV: true,
            },
            success: function (data) {
                // success callback
                // you can process data returned by function from views.py
                console.log('ajax csv reset is working', data);
            },
            error: function (data) {        
                // success callback
                // you can process data returned by function from views.py
                console.log('ajax failed but csv reset cleared', data);
            },
          });
        return start = false;
    };
});

//slider on change
function updateRangeInput(val){
    $('#topNValue').text(val);

    console.log(val);
}


// Date Range Picker

$(function() {

    var start = moment().subtract(29, 'days');
    var end = moment();
    // var start = $('#startDate').text()
    // var end = $('#endDate').text()

    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        let startPost = start.format('YYYY-MM-DD');
        let endPost = end.format('YYYY-MM-DD');
        console.log(startPost, endPost);
        $('#reportrange input').remove();
        $('#reportrange span').after(`<input class="hideContent" name = "dateInput" value="${startPost},${endPost}">`);
        // $('#dateForm').submit();
    }

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        }
    }, cb);

    cb(start, end);

});

$("#dateSubmit").on('click', function(){
    $('#dateForm').submit();
})

function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;

    // CSV file
    csvFile = new Blob([csv], {type: "text/csv"});

    // Download link
    downloadLink = document.createElement("a");

    // File name
    downloadLink.download = filename;

    // Create a link to the file
    downloadLink.href = window.URL.createObjectURL(csvFile);

    // Hide download link
    downloadLink.style.display = "none";

    // Add the link to DOM
    document.body.appendChild(downloadLink);

    // Click download link
    downloadLink.click();
};

function exportTableToCSV(filename) {
    var csv = [];
    var rows = document.getElementById('centralityTable').querySelectorAll("table tr");
    console.log(rows);
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");
        
        for (var j = 0; j < cols.length; j++) 
            row.push(cols[j].innerText);
        
        csv.push(row.join(","));        
    }

    // Download CSV file
    downloadCSV(csv.join("\n"), filename);
};

