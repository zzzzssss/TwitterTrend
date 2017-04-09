var keyword = null;
var lat = null;
var lng = null;
var heatmap = null;
var marker = null;
var infowindow = null;
var map = null;

var xmlhttp = new XMLHttpRequest();
var socket;
var interval;
var timeInterval = 5000;


function initMap(markers){

      var heatmapData = [
        new google.maps.LatLng(37.782, -122.447),
        new google.maps.LatLng(37.782, -122.445),
        new google.maps.LatLng(37.782, -122.443),
        new google.maps.LatLng(37.782, -122.441),
        new google.maps.LatLng(37.782, -122.439),
        new google.maps.LatLng(37.782, -122.437),
        new google.maps.LatLng(37.782, -122.435),
        new google.maps.LatLng(37.785, -122.447),
        new google.maps.LatLng(37.785, -122.445),
        new google.maps.LatLng(37.785, -122.443),
        new google.maps.LatLng(37.785, -122.441),
        new google.maps.LatLng(37.785, -122.439),
        new google.maps.LatLng(37.785, -122.437),
        new google.maps.LatLng(37.785, -122.435)
      ];

      var locations= markers
      var small_blue = 'https://storage.googleapis.com/support-kms-prod/SNP_2752125_en_v0'

      var UScenter = {lat: 40.461881, lng: -99.757229};

      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: UScenter,
        mapTypeId: google.maps.MapTypeId.ROADMAP
      });

  
      
     


      var marker, i;
      var infowindow = new google.maps.InfoWindow();


      var data=[];
      for (i = 0; i < locations.length; i++) { 

          var position = new google.maps.LatLng(locations[i][0][0], locations[i][0][1])

          data.push(position)

          marker = new google.maps.Marker({
          position: position,
          map: map,
          icon: small_blue
        });

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
          return function() {
            infowindow.setContent(locations[i][1]);
            infowindow.open(map, marker);
          }
        })(marker, i));

          
        }

     
   
      var heatmap = new google.maps.visualization.HeatmapLayer({
        data: data
      });
        
      heatmap.setOptions({radius: heatmap.get('100')});
      heatmap.setMap(map);


        return 1
    }



