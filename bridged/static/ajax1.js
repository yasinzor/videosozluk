console.log("here");

var scenes = []

$(document).ready( function() {

  $("#searchButton").click(function(event) {
      var term = $("#search").val()
      var response = null;
      console.log(term);

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
                    var row = "<tr>" + "<td>" + scene.path + "</td>" +
                                  "<td>" + scene.text + "</td>" +
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
              + ".mp4?start=" + scene.start + "&end=" + scene.end;
  var video = $("#video")
  video.attr("src", str);
  video.play();
  if (autoPlay && i != scenes.length - 1)
      setTimeout(function() {
        play(i+1)
      }, 8000)

  console.log(str);
}

function getSceneObj(sceneArr) {
  var scene = {}
  scene.text = sceneArr[0];
  scene.path = sceneArr[3];
  scene.start = secont(sceneArr[1]);
  scene.end = secont(sceneArr[2]);
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

function subtitle{
  getSceneObj
  var newTextTrack = video.addTextTrack("subtitles", "english", "en");
  newTextTrack.mode = "showing";
  for (var i = 0; i < subtitles.length; i++) {
    startTime = subtitles[i].start;
    endTime = subtitles[i].end;
    message = subtitles[i].text;
    newTextTrack.addCue(new VTTCue(startTime, endTime, message));
  }
}
var subtitles =
[{"start": 0.0, "end": 1.7920000000000016, "text": "<i>Agent Barton, report.</i>"}, {"start": 2.670000000000016, "end": 3.832000000000022, "text": "<i>I gave you this detail</i>"}, {"start": 3.9630000000000223, "end": 5.5400000000000205, "text": "<i>so you could keep\\na close eye on things.</i>"}, {"start": 5.756, "end": 7.132000000000005, "text": "Well, I see better from a distance."}, {"start": 7.341000000000008, "end": 9.298000000000002, "text": "Have you seen anything\\nthat might set this thing off?"}, {"start": 9.759000000000015, "end": 11.88300000000001, "text": "Doctor, it\'s spiking again."}];

   var video = document.getElementById("video1");
   var startTime, endTime, message;
   var newTextTrack = video.addTextTrack("subtitles", "english", "en");
   newTextTrack.mode = "showing"; // set track to display
   // create some cues and add them to the new track
   for (var i = 0; i < subtitles.length; i++) {
     startTime = subtitles[i].start;
     endTime = subtitles[i].end;
     message = subtitles[i].text;
     newTextTrack.addCue(new VTTCue(startTime, endTime, message));
   }
