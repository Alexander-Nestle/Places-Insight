var pac_input = document.getElementById('searchTextField');
var create = document.getElementById('Create');
var createFailed = document.getElementById('CreateFailed');
var pageJson;
var reviewResults = [];
var failedPlaces = [];
var textFile;
var currentPlace;

(function pacSelectFirst(input) {
    // store the original event binding function
    var _addEventListener = (input.addEventListener) ? input.addEventListener : input.attachEvent;
    
   createFailed.addEventListener('click', function () {
    var link = document.getElementById('downloadlink');
    link.href = makeTextFile(JSON.stringify(failedPlaces));
    link.style.display = 'block';
  }, false)
    
  create.addEventListener('click', function () {
    var link = document.getElementById('downloadlink');
    link.href = makeTextFile(JSON.stringify(reviewResults));
    link.style.display = 'block';
  }, false)

    function addEventListenerWrapper(type, listener) {
        // Simulate a 'down arrow' keypress on hitting 'return' when no pac suggestion is selected,
        // and then trigger the original listener.
        if (type == "keydown") {
            var orig_listener = listener;
            listener = function (event) {
                var suggestion_selected = $(".pac-item-selected").length > 0;
                if (event.which == 13 && !suggestion_selected) {
                    var simulated_downarrow = $.Event("keydown", { keyCode: 40, which: 40 })
                    orig_listener.apply(input, [simulated_downarrow]);
                }

                orig_listener.apply(input, [event]);
            };
        }

        // add the modified listener
        _addEventListener.apply(input, [type, listener]);
    }

    if (input.addEventListener)
        input.addEventListener = addEventListenerWrapper;
    else if (input.attachEvent)
        input.attachEvent = addEventListenerWrapper;

})(pac_input);


$(function () {
    var autocomplete = new google.maps.places.Autocomplete(pac_input);

    pac_input.click();
    autocomplete.setFields(['place_id', 'geometry', 'name', 'reviews', 'formatted_address', 'formatted_phone_number', 'url', 'types']);
    autocomplete.addListener('place_changed', function () {
        var place = autocomplete.getPlace();
        // obj = JSON.parse(place);
        
        if(place.hasOwnProperty('reviews')){
					if (reviewResults.filter(e => e.place_id == place.place_id).length == 0) {
  						reviewResults.push(place);
					} 
				}else if(!place.hasOwnProperty('formatted_address')) {
          	failedPlaces.push(currentPlace);
            console.log(place)
          } else {
          	console.log(place)
          }
    });

    /*  let element = document.getElementById(id); */

});


  function makeTextFile(text) {
    var data = new Blob([text], {type: 'text/plain'});

    // If we are replacing a previously generated file we need to
    // manually revoke the object URL to avoid memory leaks.
    if (textFile !== null) {
      window.URL.revokeObjectURL(textFile);
    }

    textFile = window.URL.createObjectURL(data);

    return textFile;
  }

function readSingleFile(e) {
    var file = e.target.files[0];
    if (!file) {
      return;
    }
    var reader = new FileReader();
    reader.onload = function(e) {
      var contents = e.target.result;
      pageJson = JSON.parse(contents);
      getReviews(pageJson)
      
    };
    reader.readAsText(file);
  }
  
function displayContents(contents) {
  var element = document.getElementById('file-content');
  element.textContent = contents;
}
  
document.getElementById('file-input')
  .addEventListener('change', readSingleFile, false);
  
function getReviews(pageJson) {
var i = 1;
	pageJson.forEach((page) => {
  	
  	    setTimeout(function () {
        console.log(page.name)
        currentPlace = page
        pac_input.value = page.name + ' ' + page.address;
        pac_input.dispatchEvent(new Event("focus"));
    }, (1000 * i))

     setTimeout(function () {
        pac_input.dispatchEvent(new KeyboardEvent('keydown', { 'keyCode': 13, 'which': 13 }));
    }, (1000 * i) + 1000);
    i += 3;
  })
}

