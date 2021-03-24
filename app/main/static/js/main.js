var currentDate = new Date();

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