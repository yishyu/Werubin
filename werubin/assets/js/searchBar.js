//from https://stackoverflow.com/questions/67353099/how-to-create-an-autocomplete-search-box-in-bootstrap

function mergeArrays({arrayTags, arrayUsers}) {
  var result = [],
      i, l = Math.min(arrayTags.length, arrayUsers.length);

  for (i = 0; i < l; i++) {
      result.push({elt: arrayTags[i].name, type: "tag"}, {elt: arrayUsers[i].username, type: "user"});
  }
  for (i = l; i < arrayTags.length; i++) {
    result.push({elt: arrayTags[i].name, type: "tag"})
  }
  for (i = l; i < arrayUsers.length; i++) {
    result.push({elt: arrayUsers[i].username, type: "user"})
  }
  return result
}

async function autocomplete(inp) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", async function(e) {
    var a, b, i, val = this.value;

    let arrRaw = await $.ajax({
      url: `/travels/api/search-autocomplete/?search=${val}`,
      headers: {
          'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
      }
    })

    console.log(arrRaw)

    let arr = mergeArrays({arrayTags: arrRaw.tags, arrayUsers: arrRaw.users})

    console.log(arr)

    /*close any already open lists of autocompleted values*/
    closeAllLists();
    if (!val) {
      return false;
    }
    currentFocus = -1;
    /*create a DIV element that will contain the items (values):*/
    a = document.createElement("DIV");
    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items");
    /*append the DIV element as a child of the autocomplete container:*/
    this.parentNode.appendChild(a);
    /*for each item in the array...*/
    for (i = 0; i < arr.length; i++) {
      /*create a DIV element for each matching element:*/
      b = document.createElement("DIV");
      /*make the matching letters bold:*/
      if (arr[i].type == "tag") {
        b.innerHTML = "<strong class='blue-text'>#" + arr[i].elt.substr(0, val.length) + "</strong>";
      } else {
        b.innerHTML = "<strong class='yellow-text'>" + arr[i].elt.substr(0, val.length) + "</strong>";
      }
      
      b.innerHTML += arr[i].elt.substr(val.length);
      /*insert a input field that will hold the current array item's value:*/
      b.innerHTML += "<input id='valueHidden' type='hidden' value='" + arr[i].elt + "'>";
      b.innerHTML += "<input id='typeHidden' type='hidden' value='" + arr[i].type + "'>";
      /*execute a function when someone clicks on the item value (DIV element):*/
      b.addEventListener("click", function(e) {
        /*insert the value for the autocomplete text field:*/
        console.log($(this).find("#valueHidden")[0].value)
        console.log(this.getElementsByTagName("input"))
        inp.value = $(this).find("#valueHidden")[0].value;
        
        $("#myInput").removeClass()
        if ($(this).find("#typeHidden")[0].value == "user") {
          $("#myInput").addClass("yellow-text")
        } else {
          $("#myInput").addClass("blue-text")
        }

        $("#searchHidden").val($(this).find("#typeHidden")[0].value)
        /*close the list of autocompleted values,
        (or any other open lists of autocompleted values:*/
        closeAllLists();
      });
      a.appendChild(b);
    }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
    $("#myInput").removeClass()
    $("#searchHidden").val("")

    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      /*If the arrow DOWN key is pressed,
      increase the currentFocus variable:*/
      currentFocus++;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 38) { //up
      /*If the arrow UP key is pressed,
      decrease the currentFocus variable:*/
      currentFocus--;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 13) {
      /*If the ENTER key is pressed, prevent the form from being submitted,*/
      e.preventDefault();
      if (currentFocus > -1) {
        /*and simulate a click on the "active" item:*/
        if (x) x[currentFocus].click();
      }
    }
  });

  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }

  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }

  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function(e) {
    closeAllLists(e.target);
  });
}

$("#searchBarButton").unbind().click(function (){
  if ($("#searchHidden").val() == "user") {
    window.location.href = `/users/profile/${$("#myInput").val()}`;
    return false;
  } else if ($("#searchHidden").val() == "tag") {
    window.location.href = `/feed/${$("#myInput").val()}`;
    return false;
  }
})

/*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
autocomplete(document.getElementById("myInput"));