var categories = ['Annual Mean Temperature','Temperature Annual Range','Annual Precipitation']
    select1 = document.getElementById('select1')
      
    for(var idx = 0; idx < categories.length; ++idx) {
        var option = document.createElement('option')
        option.text = categories[idx]
        option.value = "" + idx;
        select1.add(option, 0);
    }
      myliste = []
      select2 = document.getElementById('select2')
      fname = document.getElementById('fname')
      huhu = document.getElementById('huhu')
			image1 = document.getElementById('image1')
      function addc() {
        myliste.push([select1.value, select2.value, myvalue.value])
        renderer()
      }
      function deletec(idx) {
	      myliste.splice(idx,1)
        renderer()
      }
      function renderer(){
        htmlcollector = ''
        for (var idx = 0; idx < myliste.length; ++idx){
        	htmlcollector += categories[myliste[idx][0]] + " " + select2.options[myliste[idx][1]].innerText + " " + myliste[idx][2] +  " <button type='button' onclick='deletec(" + idx + ")'>Delete</button><br /><br />"
        }
        huhu.innerHTML = htmlcollector
        document.getElementById('button2').disabled=myliste.length==0
      }
      function updatec() {
      	imagesrc = "query?"
        for (var idx = 0; idx<myliste.length; ++idx){
          imagesrc += myliste[idx][0]+"_"+myliste[idx][1]+"_"+myliste[idx][2]
        }
        image1.src=imagesrc
      }
