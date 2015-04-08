(function(){
  L.mapbox.accessToken = 'pk.eyJ1Ijoia2VuY2hhbiIsImEiOiJpVTRzNG1RIn0.QDivyrM040Y1olXFj8UskA';
// Replace 'examples.map-i87786ca' with your map id.
var mapboxTiles = L.tileLayer('https://{s}.tiles.mapbox.com/v4/kenchan.ll57j89l/{z}/{x}/{y}.png?access_token=' + L.mapbox.accessToken, {
    attribution: '<a href="http://www.mapbox.com/about/maps/" target="_blank">Terms &amp; Feedback</a>'
});

//  https://maps.googleapis.com/maps/api/directions/json?origin=40.76019252,-73.9912551&destination=40.74147286,-73.98320928

var map = L.map('map')
    .addLayer(mapboxTiles)
    .setView([40.6323, -73.9970], 13);
})();
