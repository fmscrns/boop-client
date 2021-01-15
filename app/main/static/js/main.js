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

document.querySelectorAll("#editProfileModal").forEach((creator) => {
    var bioInput = creator.querySelector("#epf-bio_input");
    var valueBio = bioInput.getAttribute("value");
    bioInput.innerHTML = valueBio;
});

document.querySelectorAll("#editBusinessModal").forEach((creator) => {
    var bioInput = creator.querySelector("#ebf-bio_input");
    var valueBio = bioInput.getAttribute("value");
    bioInput.innerHTML = valueBio;
});