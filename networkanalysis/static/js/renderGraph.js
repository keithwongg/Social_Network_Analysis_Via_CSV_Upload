function renderGraph(){
    // load data
    // console.log(data);
    $('#container').empty();
    var data = JSON.parse($('#graphData').text());

    // create graph chart
    var chart = anychart.graph(data);

    // Node Styling
    chart.nodes().labels().enabled(true);
    chart.nodes().labels().fontSize(12);
    chart.nodes().labels().fontWeight(900);
    chart.nodes().normal().fill("#3D5A98");
    chart.nodes().hovered().fill("white");
    chart.nodes().selected().fill("#3D5A98");
    chart.nodes().normal().stroke(null);
    chart.nodes().hovered().stroke("#3D5A98", 3);
    chart.nodes().selected().stroke("#333333", 3);

    // configure the visual settings of edges
    chart.edges().normal().stroke("#A3D2FA", 1, "round");
    chart.edges().hovered().stroke("black", 4, "round");
    chart.edges().selected().stroke("black", 4);

    // Add zoom control panel
    var zoomController = anychart.ui.zoom();
    zoomController.target(chart);
    zoomController.render();

    // set container id for the chart
    chart.container('container');
    // initiate chart drawing
    chart.draw();

    //Event Listeners 
    chart.listen("click", function(e){
      // console.log(e);
      // console.log('e', e.domTarget.tag);
      
      let start = $('#start').text();
      let start_csv_record = false;
      // if the button shows 'start' means that the recording has not started. 
      if(start === "Start"){
        // Empty data as long as macro is not started
        $('#dataExportBody').empty();
        start_csv_record = false;
      } else {
        start_csv_record = true;
      }

      let selected_data = e.domTarget.tag;
      // console.log('type', e.domTarget.tag.type);
      // console.log('id', e.domTarget.tag.id);
      // console.log(selected_data === undefined);
      if(selected_data !== undefined){
        if (selected_data.type === "node"){
          let selected_node = selected_data.id;
          console.log('node selected is', selected_node);
          // pass this data back out - all data with regards to the node selected. (From & To)
          
          $.ajax({
              url: "clickDataQuery/",
              method: 'POST', // or another (GET), whatever you need
              data: {
                  name: JSON.stringify(selected_node), // data you need to pass to your function
                  click: true,
                  start: start_csv_record,
                  node: true,
              },
              success: function (data) {
                  // success callback
                  // you can process data returned by function from views.py
                  console.log('ajax is working', data);
                  
                  let table_rows = '';
                  let fieldsToInclude = [
                    "Advocate_Name",
                    "Advocate_Email", 
                    "Friend_Name",
                    "Friend_Email", 
                    "Order_Number",
                    "Completed_At", 
                    "State", 
                    "Total_Amount_Spent"];
                  data.forEach((line)=> {
                    // add body data 
                    // table_rows += '<tr>'
                    fieldsToInclude.forEach((col)=>{
                      let value = line['fields'][col];
                      table_rows += `<td>${value}</td>`;
                    })
                    $('#dataExportBody').append(`<tr>${table_rows}</tr>`);
                    table_rows = '';
                  });
                  
              },
              error: function (data) {        
                  // success callback
                  // you can process data returned by function from views.py
                  console.log('ajax failed', data);
              },
          });

        } else if(selected_data.type === "edge"){
          let selected_edge_full = selected_data.id;
          console.log('edge selected is', selected_edge_full);
          let selected_edge_index = selected_edge_full.split('_')[1];
          // pass data back out - only those edges that are selected 
          let edge_data = data["edges"][selected_edge_index];
          $.ajax({
              url: "clickDataQuery/",
              method: 'POST', // or another (GET), whatever you need
              data: {
                  name: JSON.stringify(edge_data), // data you need to pass to your function
                  click: true,
                  start: start_csv_record,
                  node: false,
              },
              success: function (data) {
                  // success callback
                  // you can process data returned by function from views.py
                  console.log('ajax is working', data);
                  
                  let table_rows = '';
                  let fieldsToInclude = [
                    "Advocate_Name",
                    "Advocate_Email", 
                    "Friend_Name",
                    "Friend_Email", 
                    "Order_Number",
                    "Completed_At", 
                    "State", 
                    "Total_Amount_Spent"];
                  data.forEach((line)=> {
                    // add body data 
                    // table_rows += '<tr>'
                    fieldsToInclude.forEach((col)=>{
                      let value = line['fields'][col];
                      table_rows += `<td>${value}</td>`;
                    })
                    $('#dataExportBody').append(`<tr>${table_rows}</tr>`);
                    table_rows = '';
                  });
                  
              },
              error: function (data) {        
                  // success callback
                  // you can process data returned by function from views.py
                  console.log('ajax failed', data);
              },
          });

        };
      } else {
        console.log('user selected blank space');
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
      }
    });
  };
  renderGraph();