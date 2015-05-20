console.log("here");

var scenes = []


  

$(document).ready( function() {
 
  $("#searchButton").click(function(event) {
      var term = $("#search").val()
      var response = null;
      var dil = $('.btn-select').text();
      console.log(dil);
      
      //alert($('.btn-select').text()+", "+$('.btn-select2').text());
      
      if(term != "") {
          $.ajax({
            url: "query",
            data: { word: term },
            dataType: "json",
            success: function(response, status){
                scenes = []
                var tbody = $("#result");
                tbody.empty();
                var i;
                var out ="";
                var start,stop,length;
                var all = response["scenes1"].concat(response["scenes2"]);
                console.log(all);
                for(i=0;i<all.length;i++){
                    var scene = getSceneObj(all[i])
                    scenes.push(scene);
                     var newword= "<em>"+term+"</em>"
                     var str = scene.text;                  
                     var res = str.replace(term ,newword );
                     var translate = scene.translate;
                     var row = "<tr>" + "<td>" + scene.path + "</td>" +
                                  "<td>" + res + "</td>" +
                                  "<td>" + translate + "</td>" +
                                  "<td><button class='play'>play</button></td>" +
                               "</tr>";   
                    tbody.append(row);
                }
                $("#result").on("click", ".play", function() {
                  var i = $(this).parent().parent().index();
                  
                  // console.log(i);
                  
                  play(i);
                })
                console.log(response);
                console.log(status);
                }
          })   
      }
      else {alert("Boş bırakılmaz.")}
  })     
}) // document.ready

function play(i) {
  var scene = scenes[i];
  var str = "http://127.0.0.1:1234/" + scene.path + "/"  + scene.path 
              + ".mp4?start=" + scene.start + "&"+"end=" + scene.end;
  var video = $("#video")   
  video.attr("src", str);
  video.play();
  video.play();
  subtitle(i);
  /*if (autoPlay && i != scenes.length - 1)
      setTimeout(function() {
        play(i+1)
      }, 8000)
               
  console.log(str);*/            
}

function getSceneObj(sceneArr) {
  var scene = {}
  scene.text = sceneArr[0];
  scene.path = sceneArr[3];
  scene.start = secont(sceneArr[1]);
  scene.end = secont(sceneArr[2]);
  scene.translate = sceneArr[4];
  return scene;
}

function secont(time)
{
        a = time.split(":");
        var hour=a[0];
        var minute=a[1];
        var second=a[2].replace(",",".");
        time = parseFloat(hour)*3600+parseFloat(minute)*60+parseFloat(second)   
        return time
}

function subtitle(i) {
   var scene = scenes[i];
   var video = $("video");
   var startTime, endTime, message;
   var track = video.addTextTrack("subtitles", "english", "en");
   track.mode = "showing"; // set track to display
   // create some cues and add them to the new track 
   track.addCue(new VTTCue(scene.start, scene.end, scene.text));
   $(track).on('cuechange', function () {
        if (window.console) {
            var activeCues = $.prop(this, 'activeCues');
            console.log(activeCues && activeCues[0] || 'exit');
        }
    });
}




