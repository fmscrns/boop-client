var currentDate = new Date();
const LOCAL_DOMAINS = ["localhost", "127.0.0.1"];

document.querySelectorAll(".gwac-fg-pw").forEach((formGroup) => {
     const input = formGroup.querySelector("input");
     const countDisplayCont = formGroup.querySelector(".c-cnt");
     const countDisplay = countDisplayCont.querySelector(".c-dsp");
     const feedbackDisplayCont = formGroup.querySelector(".invalid-feedback");
     const feedbackDisplayList = feedbackDisplayCont.querySelectorAll(".frm-fb");
     const togglePassword = formGroup.querySelector(".toggle-password");
     const showPassToggle = formGroup.querySelector(".pw-s");
     const hidePassToggle = formGroup.querySelector(".pw-h");
     
     var typingTimer;
     const doneTypingInterval = 2000;

     input.addEventListener("keyup", (e) => {
          var count = $(input).val().length;

          if (count == 0) {
               window.clearTimeout(typingTimer);

               $(countDisplayCont).removeClass("d-block");
               $(countDisplayCont).addClass("d-none");
               $(feedbackDisplayCont).removeClass("d-block");
               $(feedbackDisplayCont).addClass("d-none");
               $(input).removeClass("is-invalid");

               typingTimer = setTimeout(
                    function () {
                         $(feedbackDisplayList).eq(0).html("This can't be empty.");
                         $(feedbackDisplayList).eq(1).addClass("d-none");
                         $(countDisplayCont).removeClass("d-none");
                         $(countDisplayCont).addClass("d-block");
                         $(feedbackDisplayCont).removeClass("d-none");
                         $(feedbackDisplayCont).addClass("d-block");
                         $(input).addClass("is-invalid");
                    }, doneTypingInterval
               )

          } else if ((count > 0) && (count < 8)) {
               window.clearTimeout(typingTimer);

               $(countDisplayCont).removeClass("d-block");
               $(countDisplayCont).addClass("d-none");
               $(feedbackDisplayCont).removeClass("d-block");
               $(feedbackDisplayCont).addClass("d-none");
               $(input).removeClass("is-invalid");

               typingTimer = setTimeout(
                    function () {
                         $(feedbackDisplayList).eq(0).html("Too short.");
                         $(feedbackDisplayList).eq(1).addClass("d-none");
                         $(countDisplayCont).removeClass("d-none");
                         $(countDisplayCont).addClass("d-block");
                         $(feedbackDisplayCont).removeClass("d-none");
                         $(feedbackDisplayCont).addClass("d-block");
                         $(input).addClass("is-invalid");
                    }, doneTypingInterval
               )

          } else {
               window.clearTimeout(typingTimer);

               $(countDisplayCont).removeClass("d-block");
               $(countDisplayCont).addClass("d-none");
               $(feedbackDisplayCont).removeClass("d-block");
               $(feedbackDisplayCont).addClass("d-none");
               $(input).removeClass("is-invalid");
          }

          $(countDisplay).html(count);
     });

     togglePassword.addEventListener("click", (e) => {
          $(this).toggleClass("eye-slash");

          if ($(input).attr("type") == "password") {
               $(input).attr("type", "text");
          } else {
               $(input).attr("type", "password");
          }

          $(showPassToggle).css("display",
               ($(showPassToggle).css("display") === "flex")
                    ?
                    "none"
                    :
                    "flex"
          );

          $(hidePassToggle).css("display",
               ($(showPassToggle).css("display") === "none")
                    ?
                    "flex"
                    :
                    "none"
          );
     })
});

document.querySelectorAll(".gwac-fg-n").forEach((formGroup) => {
    const input = formGroup.querySelector("input");
    const countDisplayCont = formGroup.querySelector(".c-cnt");
    const countDisplay = countDisplayCont.querySelector(".c-dsp");
    const feedbackDisplayCont = formGroup.querySelector(".invalid-feedback");
    const feedbackDisplayList = feedbackDisplayCont.querySelectorAll(".frm-fb");

    var typingTimer;
    const doneTypingInterval = 2000;

    input.addEventListener("keyup", (e) => {
         var count = $(input).val().length;

         if (count == 0) {
              window.clearTimeout(typingTimer);

              $(countDisplayCont).removeClass("d-block");
              $(countDisplayCont).addClass("d-none");
              $(feedbackDisplayCont).removeClass("d-block");
              $(feedbackDisplayCont).addClass("d-none");
              $(input).removeClass("is-invalid");

              typingTimer = setTimeout(
                   function () {
                        $(feedbackDisplayList).eq(0).html("This can't be empty.");
                        $(feedbackDisplayList).eq(1).addClass("d-none");
                        $(countDisplayCont).removeClass("d-none");
                        $(countDisplayCont).addClass("d-block");
                        $(feedbackDisplayCont).removeClass("d-none");
                        $(feedbackDisplayCont).addClass("d-block");
                        $(input).addClass("is-invalid");
                   }, doneTypingInterval
              )
         
         } else if (count < 2) {
              window.clearTimeout(typingTimer);

              $(countDisplayCont).removeClass("d-block");
              $(countDisplayCont).addClass("d-none");
              $(feedbackDisplayCont).removeClass("d-block");
              $(feedbackDisplayCont).addClass("d-none");
              $(input).removeClass("is-invalid");

              typingTimer = setTimeout(
                   function () {
                        $(feedbackDisplayList).eq(0).html("Too short.");
                        $(feedbackDisplayList).eq(1).addClass("d-none");
                        $(countDisplayCont).removeClass("d-none");
                        $(countDisplayCont).addClass("d-block");
                        $(feedbackDisplayCont).removeClass("d-none");
                        $(feedbackDisplayCont).addClass("d-block");
                        $(input).addClass("is-invalid");
                   }, doneTypingInterval
              )

         } else if (count > 30) {
              window.clearTimeout(typingTimer);

              $(countDisplayCont).removeClass("d-block");
              $(countDisplayCont).addClass("d-none");
              $(feedbackDisplayCont).removeClass("d-block");
              $(feedbackDisplayCont).addClass("d-none");
              $(input).removeClass("is-invalid");

              typingTimer = setTimeout(
                   function () {
                        $(feedbackDisplayList).eq(0).html("Too long.");
                        $(feedbackDisplayList).eq(1).addClass("d-none");
                        $(countDisplayCont).removeClass("d-none");
                        $(countDisplayCont).addClass("d-block");
                        $(feedbackDisplayCont).removeClass("d-none");
                        $(feedbackDisplayCont).addClass("d-block");
                        $(input).addClass("is-invalid");
                   }, doneTypingInterval
              )

         } else {
              window.clearTimeout(typingTimer);

              $(countDisplayCont).removeClass("d-block");
              $(countDisplayCont).addClass("d-none");
              $(feedbackDisplayCont).removeClass("d-block");
              $(feedbackDisplayCont).addClass("d-none");
              $(input).removeClass("is-invalid");
         }

         $(countDisplay).html(count);
    });
});

document.querySelectorAll(".gwac-fg-em").forEach((formGroup) => {
    const input = formGroup.querySelector("input");
    const feedbackDisplayCont = formGroup.querySelector(".invalid-feedback");
    const feedbackDisplayList = feedbackDisplayCont.querySelectorAll(".frm-fb");
    const emailExists = formGroup.querySelector(".frm-fb-emex");

    const regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;

    var typingTimer;
    const doneTypingInterval = 2000;

    input.addEventListener("keyup", (e) => {
         var count = $(input).val().length;

         if (count == 0) {
              window.clearTimeout(typingTimer);

              $(feedbackDisplayCont).removeClass("d-block");
              $(feedbackDisplayCont).addClass("d-none");
              $(input).removeClass("is-invalid");

              typingTimer = setTimeout(
                   function () {
                        $(feedbackDisplayList).eq(0).html("This can't be empty.")
                        $(feedbackDisplayList).eq(1).addClass("d-none");
                        $(feedbackDisplayCont).removeClass("d-none");
                        $(feedbackDisplayCont).addClass("d-block");
                        $(input).addClass("is-invalid");
                   }, doneTypingInterval
              )

         } else if ((emailExists) && ($(input).val() == $(emailExists).html())) {
              window.clearTimeout(typingTimer);

              $(feedbackDisplayCont).removeClass("d-block");
              $(feedbackDisplayCont).addClass("d-none");
              $(input).removeClass("is-invalid");

              typingTimer = setTimeout(
                   function () {
                        $(feedbackDisplayList).eq(0).html("This email has already been taken.")
                        $(feedbackDisplayList).eq(1).addClass("d-none");
                        $(feedbackDisplayCont).removeClass("d-none");
                        $(feedbackDisplayCont).addClass("d-block");
                        $(input).addClass("is-invalid");
                   }, doneTypingInterval
              )

         } else if ((count > 0) && (regex.test($(input).val()) === true)) {
              window.clearTimeout(typingTimer);

              $(feedbackDisplayCont).removeClass("d-block");
              $(feedbackDisplayCont).addClass("d-none");
              $(input).removeClass("is-invalid");

         } else {
              window.clearTimeout(typingTimer);

              $(feedbackDisplayCont).removeClass("d-block");
              $(feedbackDisplayCont).addClass("d-none");
              $(input).removeClass("is-invalid");

              typingTimer = setTimeout(
                   function () {
                        $(feedbackDisplayList).eq(0).html("Invalid email.")
                        $(feedbackDisplayList).eq(1).addClass("d-none");
                        $(feedbackDisplayCont).removeClass("d-none");
                        $(feedbackDisplayCont).addClass("d-block");
                        $(input).addClass("is-invalid");
                   }, doneTypingInterval
              )
         }
    });
});

document.querySelectorAll(".crt-usr").forEach((formGroup) => {
    const loading = formGroup.querySelector(".gwac-ld");
    $(loading).hide();

    const inputs = formGroup.querySelectorAll("input");
    const submit = formGroup.querySelector("input[type='submit']")

    $(formGroup).one("submit", function (e) {
         $(inputs).blur();
         $(submit).prop("disabled", true);
         $(submit).removeClass("btn-primary");
         $(submit).addClass("btn-secondary");

         $(loading).show();
    });
});

document.querySelectorAll(".lgn-usr").forEach((formGroup) => {
    const loading = formGroup.querySelector(".gwac-ld");
    $(loading).hide();

    const inputs = formGroup.querySelectorAll("input");
    const submit = formGroup.querySelector("input[type='submit']")

    $(formGroup).one("submit", function (e) {
         $(inputs).blur();
         $(submit).prop("disabled", true);
         $(submit).removeClass("btn-primary");
         $(submit).addClass("btn-secondary");

         $(loading).show();
    });
});

document.querySelectorAll(".cbf-ot-cont").forEach((container) => {
    var checkbox = container.querySelector("input[type=checkbox]");
    var timeCont = container.querySelector(".cbf-ot-t");

    checkbox.addEventListener('change', function() {
        if (this.checked) {
            timeCont.style.display = "block";
            timeCont.style.pointerEvents = "auto";
            timeCont.querySelectorAll("input").forEach((input) => {
                input.value = "";
                input.required = true;
            });
        } else {
            timeCont.style.display = "none";
            timeCont.style.pointerEvents = "none";
            timeCont.querySelectorAll("input").forEach((input) => {
                input.value = "01:00";
                input.required = false;
            });
        }
    });
});

$(".alert-dismissible").fadeTo(5000, 500).slideUp(500, function (e) {
    $(e).alert("close");
});

document.querySelectorAll("#createPetModal").forEach((creator) => {
    const form = creator.querySelector(".modal-content");
    const specieSelectInput = form.querySelector("#group_input");
    const breedSelectInput = form.querySelector("#subgroup_input");
    const token = form.getAttribute("token");
    const APIDomain = form.getAttribute("api-domain");

    specieSelectInput.addEventListener("change", (e) => {
        breedSelectInput.setAttribute("disabled", "");
   
        specieId = specieSelectInput.value;
   
        $.ajax({
            type: "GET",
            beforeSend: function (request) {
                 request.setRequestHeader("Authorization", "Bearer " + token);

            },
            url: APIDomain + "/breed/parent/" + specieId,

            success: function (response) {
                let breedOptions = "";
                for (let breed of response["data"]) {
                    breedOptions += "<option value='" + breed["public_id"] + "'>" + breed["name"] + "</option>";
                }
                breedSelectInput.innerHTML = breedOptions;
                breedSelectInput.removeAttribute("disabled");
            }
        });
    });
})

var parentInput = document.getElementsByName("ebf-parent_input");
var i;
for (i = 0; i < parentInput.length; i++) {
    var selectedId = parentInput[i].getAttribute("selected");

    for (j = 0; j < parentInput[i].length; j++) {
        if (parentInput[i][j].getAttribute("value") === selectedId) {
            parentInput[i][j].setAttribute("selected", true);
        }
    }
}
// =====================================================================================================================================================================
autocomplete(document.querySelector(".cpof-autocomplete"));
function autocomplete(div) {
     inp = div.querySelectorAll("input")[0];
     pidHolder = div.querySelectorAll("input")[1];

     var currentFocus;

     var typingTimer;
     var doneTypingInterval = 2000;
     inp.addEventListener("input", function(e) {
          window.clearTimeout(typingTimer);
          var a, b, i, val = this.value;
          closeAllLists();
          if (!val) { return false;}
          currentFocus = -1;
          a = document.createElement("DIV");
          a.setAttribute("id", this.id + "autocomplete-list");
          a.setAttribute("class", "autocomplete-items");
          /*append the DIV element as a child of the autocomplete container:*/
          this.parentNode.appendChild(a);

          typingTimer = setTimeout(function () {
               $.ajax({
                    type: "GET",
                    url: "/user/?search=" + val,
     
                    success: function (response) {
                         for (let user of response) {
                              /*create a DIV element for each matching element:*/
                              b = document.createElement("DIV");
                              b.classList.add("d-flex", "d-column");
     
                              var nameSubstringMatchPosition = user.name.toUpperCase().indexOf(val.toUpperCase());
                              var usernameSubstringMatchPosition = user.username.toUpperCase().indexOf(val.toUpperCase());
                              if (nameSubstringMatchPosition !== -1) {
                                   b.innerHTML += "<span>" + [user.name.slice(0, nameSubstringMatchPosition), "<strong>", user.name.slice(nameSubstringMatchPosition, nameSubstringMatchPosition + val.length), "</strong>", user.name.slice(nameSubstringMatchPosition + val.length)].join('') + "</span>";
                              } else {
                                   b.innerHTML += "<span>" + user.name + "</span>";
                              }
                              if (usernameSubstringMatchPosition !== -1) {
                                   b.innerHTML += "<span class='small tex-muted mt-1'>@" + [user.username.slice(0, usernameSubstringMatchPosition), "<strong>", user.username.slice(usernameSubstringMatchPosition, usernameSubstringMatchPosition + val.length), "</strong>", user.username.slice(usernameSubstringMatchPosition + val.length)].join('') + "</span>";
                              } else {
                                   b.innerHTML += "<span class='small tex-muted mt-1'>@" + user.username + "</span>";
                              }
                              /*execute a function when someone clicks on the item value (DIV element):*/
                              b.addEventListener("click", function(e) {
                                   inp.value = user.name;
                                   pidHolder.value = user.public_id;
                                   closeAllLists();
                              });
                              a.appendChild(b);
                         }
                    }
               });
          }, doneTypingInterval);
     });

     inp.addEventListener("keydown", function(e) {
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
       x[currentFocus].scrollIntoView({ behavior: 'smooth' })
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
//    document.addEventListener("click", function (e) {
//        closeAllLists(e.target);
//    });
}