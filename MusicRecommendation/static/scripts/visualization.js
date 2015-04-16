(function(){

  L.mapbox.accessToken = 'pk.eyJ1Ijoia2VuY2hhbiIsImEiOiJpVTRzNG1RIn0.QDivyrM040Y1olXFj8UskA';

  var mapboxTiles = L.tileLayer('https://{s}.tiles.mapbox.com/v4/kenchan.ll57j89l/{z}/{x}/{y}.png?access_token=' + L.mapbox.accessToken, {
    attribution: '<a href="http://www.mapbox.com/about/maps/" target="_blank">Terms &amp; Feedback</a>'
  });

  //  https://maps.googleapis.com/maps/api/directions/json?origin=40.76019252,-73.9912551&destination=40.74147286,-73.98320928

  var map = L.map('map')
             .addLayer(mapboxTiles)
             .setView([40.72332345541449, -73.99], 13);

  var svg = d3.select(map.getPanes().overlayPane).append("svg");

  var newRoute = function(i){
    var g = svg.append("g").attr("class", "leaflet-zoom-hide");

    d3.json("/api/sample/10-2014/" + i.toString(), function(collection) {
      tripdata = collection[0];
      collection = collection[0].geoData;
      console.log(tripdata);
      console.log(collection);
      var featuresdata = collection.features.filter(function(d) {
          return d.properties.id == "route"
      })

      var transform = d3.geo.transform({
          point: projectPoint
      });

      var d3path = d3.geo.path().projection(transform);

      var toLine = d3.svg.line()
                     .interpolate("linear")
                     .x(function(d) {
                        return applyLatLngToLayer(d).x
                     })
                     .y(function(d) {
                        return applyLatLngToLayer(d).y
                     });

      var ptFeatures = g.selectAll("circle")
                        .data(featuresdata)
                        .enter()
                        .append("circle")
                        .attr("r", 3)
                        .attr("class", "waypoints");

      var linePath = g.selectAll(".lineConnect")
                      .data([featuresdata])
                      .enter()
                      .append("path")
                      .attr("class", "lineConnect");

      var marker = g.append("circle")
                    .attr("r", 10)
                    .attr("id", "marker")
                    .attr("class", "travelMarker");

      var originANDdestination = [featuresdata[0], featuresdata[featuresdata.length - 1]]

      var begend = g.selectAll(".locations")
                    .data(originANDdestination)
                    .enter()
                    .append("circle", ".locations")
                    .attr("r", 5)
                    .style("fill", "#26A69A")
                    .style("opacity", "1");

      var text = g.selectAll("text")
                  .data(originANDdestination)
                  .enter()
                  .append("text")
                  .text(function(d) {
                      return d.properties.time
                  })
                  .attr("class", "locnames")
                  .attr("y", function(d) {
                      return -10
                  });

      map.on("viewreset", reset);
      reset();
      transition(tripdata);

      function reset() {
          var bounds = d3path.bounds(collection),
              topLeft = bounds[0],
              bottomRight = bounds[1];

          text.attr("transform",
              function(d) {
                  return "translate(" +
                      applyLatLngToLayer(d).x + "," +
                      applyLatLngToLayer(d).y + ")";
              });

          begend.attr("transform",
              function(d) {
                  return "translate(" +
                      applyLatLngToLayer(d).x + "," +
                      applyLatLngToLayer(d).y + ")";
              });

          ptFeatures.attr("transform",
              function(d) {
                  return "translate(" +
                      applyLatLngToLayer(d).x + "," +
                      applyLatLngToLayer(d).y + ")";
              });

          marker.attr("transform",
              function() {
                  var y = featuresdata[0].geometry.coordinates[1]
                  var x = featuresdata[0].geometry.coordinates[0]
                  return "translate(" +
                      map.latLngToLayerPoint(new L.LatLng(y, x)).x + "," +
                      map.latLngToLayerPoint(new L.LatLng(y, x)).y + ")";
              });


          svg.attr("width", bottomRight[0] - topLeft[0] + 120)
              .attr("height", bottomRight[1] - topLeft[1] + 120)
              .style("left", topLeft[0] - 50 + "px")
              .style("top", topLeft[1] - 50 + "px");

          linePath.attr("d", toLine)
          g.attr("transform", "translate(" + (-topLeft[0] + 50) + "," + (-topLeft[1] + 50) + ")");

      }

      function transition(d) {
        var calculateDuration = function(d){
          
          //  Must define a time factor... Can be modified on the frontend later
          var timeFactor = 5;

          var start = Date.parse(d.starttime),
            finish = Date.parse(d.stoptime),
            duration = finish - start;

            duration = duration/60000; //convert to minutes

            duration = duration * (1/timeFactor) * 1000;
            return duration;
        };
          
          timeLength = calculateDuration(d);

          linePath.transition()
              .duration(timeLength)
              .attrTween("stroke-dasharray", tweenDash);
              // .each("end", callBack(i));
              //  Uncomment this bottom portion for infinite looping.
              /*
              .each("end", function() {
                  d3.select(this).call(transition);
              });
              */
      }

      function tweenDash() {
          return function(t) {
              var l = linePath.node().getTotalLength(); 
        
              interpolate = d3.interpolateString("0," + l, l + "," + l);
              var marker = d3.select("#marker");
              var p = linePath.node().getPointAtLength(t * l);

              marker.attr("transform", "translate(" + p.x + "," + p.y + ")"); 
            
              return interpolate(t);
          }
      }

      function projectPoint(x, y) {
          var point = map.latLngToLayerPoint(new L.LatLng(y, x));
          this.stream.point(point.x, point.y);
      } 

    });

    function applyLatLngToLayer(d) {
        var y = d.geometry.coordinates[1]
        var x = d.geometry.coordinates[0]
        return map.latLngToLayerPoint(new L.LatLng(y, x))
    }
  };

  newRoute(23);
  newRoute(80);
})();
