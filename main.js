function loadJSON(filename, callback) {
    var xobj = new XMLHttpRequest();
    xobj.overrideMimeType("application/json");
    xobj.open('GET', filename, true);
    // Replace 'my_data' with the path to your file
    xobj.onreadystatechange = function() {
        if (xobj.readyState === 4) {// && xobj.status === "200") {
            // Required use of an anonymous callback 
            // as .open() will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
        }
    };
    xobj.send(null);
}
loadJSON("maps.json", function(response) {
    maps = JSON.parse(response);
    select1 = document.getElementById('select1')
    for(var idx = 0; idx < maps.length; ++idx) {
        var option = document.createElement('option')
        option.text = maps[idx][0]
        option.value = "" + idx;
        select1.add(option, 0);
    }
    myliste = []
    select2 = document.getElementById('select2')
    fname = document.getElementById('fname')
    huhu = document.getElementById('huhu')
    image1 = document.getElementById('image1')
})

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
