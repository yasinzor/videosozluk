console.log("here");

var scenes = [],
    videoS = null,
    newTextTrack = null;
var loop=0;

$(document).ready( function() {

  videoS = document.getElementById("video");
  newTextTrack = videoS.addTextTrack("subtitles","english","en");
  newTextTrack.mode ="showing";
  
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
                var translate = $('#translate');
                tbody.empty();
                var i;
                var out ="";
                var start,stop,length;
                var all = response["scenes1"].concat(response["scenes2"]);
                console.log(all);

                //var trans= "<h2>"+response["transword"]+"</h2>"
                //translate.append(trans);
                for(i=0;i<all.length;i++){
                    var scene = getSceneObj(all[i])
                    scenes.push(scene);
              
                     var newword= "<em>"+term+"</em>"
                     var str = scene.text;                  
                     var res = str.replace(term ,newword );
                     var translate = scene.translate;
     
                    
                    var row = "<tr>" + "<td>" + scene.title + "</td>" +
                                  "<td>" + res + "</td>" +
                                  "<td>" + translate + "</td>" +
                                  "<td><button class='play' >play</button></td>" +
                               "</tr>";   
                    tbody.append(row);
                }
                 
                
                $("#result").on("click", ".play", function() {
                  var i = $(this).parent().parent().index();
                  // console.log(i);
                  loop=0;
                  play(i);
                  $("html, body").animate({ scrollTop: 100 }, 700);
                })
                console.log(response);
                console.log(status);
                
                }
          })   
      }
      else {alert("Boş bırakılmaz.")}
  })     
}) // document.ready

var lastCue = null;


function play(i) {
  $("#result tr.vidic-selected").removeClass("vidic-selected");
  $("#result tr").eq(i).addClass("vidic-selected");
  
  var scene = scenes[i];
  var str = "http://127.0.0.1:1234/" + scene.path + "/"  + scene.path 
              + ".mp4?start=" + scene.start + "&"+"end=" + scene.end;
  var video = $("#video")   
  video.attr("src", str);
  var startTime, endTime, message;
 console.log(scene)
     startTime = scene.start-scene.start;
     endTime = scene.end- scene.start;
     message = scene.text;
     if (lastCue) {
       newTextTrack.removeCue(lastCue);
     }
     lastCue = new VTTCue(startTime, endTime, message)
     newTextTrack.addCue(lastCue);
  
  console.log("1.- "+loop);
  if (loop<=1 && i != scenes.length - 1)
      setTimeout(function() {
        play(i);
        loop++;
        console.log(loop);
      },6000)
  
  
  
  //video.play();
  var autoPlay = false;
  if (autoPlay && i != scenes.length - 1)
      setTimeout(function() {
        play(i+1)
      }, 8000)
               
  console.log(str);            
}

function getSceneObj(sceneArr) {
  var scene = {}
  scene.text = sceneArr[0];
  scene.path = sceneArr[4];
  scene.title = sceneArr[3];
  scene.start = secont(sceneArr[1]);
  scene.end = secont(sceneArr[2]);
  scene.translate = sceneArr[5];
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





