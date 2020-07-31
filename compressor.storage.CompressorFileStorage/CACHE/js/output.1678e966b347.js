
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

          // set settings for each group
          for (var i = 0; i < 8; i++) {
              // get group
              var group = chart.group(i);

              // set group labels settings
              group.labels()
                  .enabled(true)
                  .anchor('left-center')
                  .position('right-center')
                  .padding(0, -5)
                  .fontColor(anychart.palettes.defaultPalette[i]);

              // set group nodes stroke and fill
              group.stroke(anychart.palettes.defaultPalette[i]);
              group.fill(anychart.palettes.defaultPalette[i]);
          }

          // set container id for the chart
          chart.container('container');
          // initiate chart drawing
          chart.draw();
      });
});;