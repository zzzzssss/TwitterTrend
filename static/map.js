var keyword = null;
var lat = null;
var lng = null;
var heatmap = null;
var marker = null;
var infowindow = null;
var map = null;

var xmlhttp = new XMLHttpRequest();

/*
 * Listen to the http request 
 */
xmlhttp.onreadystatechange = function() {
  if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
    var text = JSON.parse(xmlhttp.responseText); 
    if (text['pattern'] == "global") {
      var locs = text['tweets'];
      var arr = heatmap.getData();
      for (var i = 0; i < locs.length; ++i) {
          var loc = new google.maps.LatLng(parseInt(locs[i][1]), parseInt(locs[i][0]));
        arr.push(loc);
      }
    } else {
      var tweets = text['tweets'];
      var content = "";
      for (var i = 0; i < tweets.length; ++i) {
        content += ("<p>" + tweets[i] + "</p>")
      }
      infowindow.setContent(content);
        infowindow.open(map, marker);
    }
  }
};



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



/* 
 * Change the keyword of dropdown
 */
$(".dropdown").on("click", "li a", function() {
  keyword = $(this).text();
  $(".dropdown-toggle").html(keyword + ' <span class="caret"></span>');
}); 


$(".dropdown2").on("click", "li a", function() {
  keyword = $(this).text();
  $(".dropdown-toggle").html(keyword + ' <span class="caret"></span>');
}); 


/* 
 * Initilize two datetimepickers
 */
$('#datetimepicker1').datetimepicker();
$('#datetimepicker2').datetimepicker();

/*
 * When clicking the sumbit button, send a POST request
 */
$("button").on("click", function() {
  sendHttp("global");
});

function sendHttp(pattern) {

  /*
   * Remind the user to pick a location and a keyword
   */
  if (keyword == null) {
    alert("Please pick a keyword");
    return;
  }

  /* 
   * Get the begin date and end date 
   */
  var beginDate = $("#datetimepicker1 input").val().split("/").join("-").split(" ").join("+");
  var endDate = $("#datetimepicker2 input").val().split("/").join("-").split(" ").join("+");
  if (beginDate == "" || endDate == "") {
    alert("Please pick the begin date and end date");
    return;
  }

  if (pattern == "global") {
    /*
     * Clear the previous data
     */
    var arr = heatmap.getData();
    while (arr.length > 0)
      arr.pop();

    /*
     * HTTP request sent
     */
    xmlhttp.open("POST", "/global?kw=" + keyword + "&start=" + beginDate + "&end=" + endDate, true);
    xmlhttp.send();

  } else {
    // xmlhttp.open("POST", "/local?kw=" + keyword + "&start=" + beginDate + "&end=" + endDate, true);
    xmlhttp.open("POST", "/local?kw=" + keyword + "&start=" + beginDate + "&end=" + endDate + "&lat=" + lng + "&lon=" + lat, true);
    xmlhttp.send();
  }
}