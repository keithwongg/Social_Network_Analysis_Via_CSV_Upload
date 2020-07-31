
// alert('/static/');

let jsonFile = '/static/' + 'js/testdata.json';
console.log(jsonFile);
anychart.onDocumentReady(function () {
  anychart.data.loadJsonFile(
      // The data used in this sample can be obtained from the CDN
      jsonFile,
      function (data) {
          // create graph chart
          var chart = anychart.graph(data);

          // Node Styling
        //   chart.nodes().labels().enabled(true);
        //   chart.nodes().normal().fill("#3D5A98");
        //   chart.nodes().hovered().fill("white");
        //   chart.nodes().selected().fill("#3D5A98");
        //   chart.nodes().normal().stroke(null);
        //   chart.nodes().hovered().stroke("#3D5A98", 3);
        //   chart.nodes().selected().stroke("#333333", 3);

        //   // set settings for each group
        //   for (var i = 0; i < 8; i++) {
        //       // get group
        //       var group = chart.group(i);

        //       // set group labels settings
        //       group.labels()
        //           .enabled(true)
        //           .anchor('left-center')
        //           .position('right-center')
        //           .padding(0, -5)
        //           .fontColor(anychart.palettes.defaultPalette[i]);

        //       // set group nodes stroke and fill
        //       group.stroke(anychart.palettes.defaultPalette[i]);
        //       group.fill(anychart.palettes.defaultPalette[i]);
        //   }

          // Add zoom control panel
          var zoomController = anychart.ui.zoom();
          zoomController.target(chart);
          zoomController.render();

          // set container id for the chart
          chart.container('container');
          // initiate chart drawing
          chart.draw();
      });
});;