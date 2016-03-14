console.log("here");
$(document).ready( function() {
 
  $("#searchButton").click(function(event) {
      var term = $("#search").val()
      var response = null;
      console.log(term);
      
      if(term != "") {
          $.ajax({
            url: "query_word.py/query",
            data: { word: term },
            dataType: "json",
            success: function(response, status){
                var i;
                var out ="";
                var start,stop,length;
                for(i=0;i<response["scenes1"].length;i++){
                    out +=response["scenes1"][i];
                    sentence=response["scenes1"][i][0];
                    start=response["scenes1"][i][1];
                    stop=response["scenes1"][i][2];
                    movie=response["scenes1"][i][3];
                    
                    milstart = secont(start);
                    milstop = secont(stop);
                    
                    $("#result").append(milstart +"<br>");
                    $("#result").append(milstop +"<br>");
                    $("#result").append(sentence+"<b>"+start+"</b>"+stop+movie+"<br>");
                }
                for(i=0;i<response["scenes2"].length;i++){
                    out +=response["scenes2"][i];
                    sentence=response["scenes2"][i][0];
                    start=response["scenes2"][i][1];
                    stop=response["scenes2"][i][2];
                    movie=response["scenes2"][i][3];
                                  
                    milstart = secont(start);
                    milstop = secont(stop);

                    $("#result").append(milstart +"<br>");
                    $("#result").append(milstop +"<br>");                    
                    $("#result").append(sentence+"<b>"+start+"</b>"+stop+movie+"<br>");
                }
                console.log(response);
                console.log(status);
                }
          })   
      }
      else {alert("Boş bırakılmaz.")}
  })     
}) // document.ready


function secont(time)
{
        a = time.split(":");
        var hour=a[0];
        var minute=a[1];
        var second=a[2].replace(",",".");
        time = parseFloat(hour)*3600+parseFloat(minute)*60+parseFloat(second)   
        return time
}






