var currentDate = new Date();

document.querySelectorAll(".sp-pc-bi").forEach((baseCard) => {
     let searchValue = baseCard.getAttribute("search-value");
     let petsUrl = baseCard.getAttribute("pets-url");
     let peopleUrl = baseCard.getAttribute("people-url");
     let loading = $(baseCard).siblings(".spinner-grow");
     let impasseBadge = $(baseCard).siblings(".badge");
     var paginationNo = 1;
     var doneAjax = true;
     var activateScrollPagination = false;
     var queryCont;
     var queryUrl;
     var queryClassRemoved;
     var queryEndResultConfig;
     $(window).scroll(function () {
          if(($(window).scrollTop() + $(window).height() == $(document).height()) && doneAjax && activateScrollPagination) {
               loading.show();
               resultAjax(queryCont, queryUrl, queryClassRemoved, queryEndResultConfig);
          }
     });
     
     if (petsUrl && peopleUrl) {
          $(document.querySelectorAll(".sp-pc-dc-disp")).remove();
          resultAjax(resultContainerCreator("Pets"), petsUrl + "?value=" + searchValue, "sp-pc-bi-us", [0, "/search/pets?value=" + searchValue]);
          resultAjax(resultContainerCreator("People"), peopleUrl + "?search=" + searchValue, "sp-pc-bi-pe", [0, "/search/people?value=" + searchValue]);
     } else if (petsUrl) {
          paginationNo = 1;
          $(document.querySelectorAll(".sp-pc-dc-disp")).remove();
          queryCont = resultContainerCreator("Pets");
          queryUrl = petsUrl + "?value=" + searchValue;
          queryClassRemoved = "sp-pc-bi-us";
          queryEndResultConfig = [1];
          resultAjax(queryCont, queryUrl, queryClassRemoved, queryEndResultConfig);
          let petFilterSideNavbar = document.querySelector(".sfpt-nbc");
          let specieSelectInput = petFilterSideNavbar.querySelectorAll("select")[0];
          let breedSelectInput = petFilterSideNavbar.querySelectorAll("select")[1];
          let statusBoolInput = petFilterSideNavbar.querySelectorAll("select")[2];
          specieSelectInput.addEventListener("change", (e) => {
               breedSelectInput.setAttribute("disabled", "disabled");
               breedSelectInput.innerHTML = "";
               if (specieSelectInput.value != 0) {
                    specieBreedInputDynamicAjax(specieSelectInput, breedSelectInput);
               }
          });
          [specieSelectInput, breedSelectInput, statusBoolInput].forEach((input) => {
               input.addEventListener("change", (e) => {
                    paginationNo = 1;
                    $(document.querySelectorAll(".sp-pc-dc-disp")).remove();
                    queryCont = resultContainerCreator("Pets");
                    let ssiSelected = ($("option:selected", specieSelectInput).attr("param-str") ? $("option:selected", specieSelectInput).attr("param-str") : "");
                    let bsiSelected = ($("option:selected", breedSelectInput).attr("param-str") ? $("option:selected", breedSelectInput).attr("param-str") : "");
                    let stiSelected = ($("option:selected", statusBoolInput).attr("param-str") ? $("option:selected", statusBoolInput).attr("param-str") : "");
                    queryUrl = petsUrl + "?value=" + searchValue + ssiSelected + bsiSelected + stiSelected;
                    queryClassRemoved = "sp-pc-bi-us";
                    queryEndResultConfig = [1];
                    resultAjax(queryCont, queryUrl, queryClassRemoved, queryEndResultConfig);
               });
          });
     } else if (peopleUrl) {
          queryCont = resultContainerCreator("People");
          queryUrl = peopleUrl + "?search=" + searchValue;
          queryClassRemoved = "sp-pc-bi-pe";
          queryEndResultConfig = [1];
          resultAjax(queryCont, queryUrl, queryClassRemoved, queryEndResultConfig);
          let peopleFilterSideNavbar = document.querySelector(".sfppl-nbc");
          let sameFollowedPetsInput = peopleFilterSideNavbar.querySelectorAll("input")[0];
          let sameBreedPreferencesInput = peopleFilterSideNavbar.querySelectorAll("input")[1];
          [sameFollowedPetsInput, sameBreedPreferencesInput].forEach((input) => {
               input.addEventListener("change", (e) => {
                    if (e.currentTarget.checked) {
                         e.currentTarget.setAttribute("param-str", e.currentTarget.getAttribute("param-str").slice(0, -1) + "1");
                    } else {
                         e.currentTarget.setAttribute("param-str", e.currentTarget.getAttribute("param-str").slice(0, -1) + "0");
                    }
                    paginationNo = 1;
                    $(document.querySelectorAll(".sp-pc-dc-disp")).remove();
                    queryCont = resultContainerCreator("People");
                    let sfpiSelected = ($(sameFollowedPetsInput).attr("param-str") ? $(sameFollowedPetsInput).attr("param-str") : "");
                    let sbpiSelected = ($(sameBreedPreferencesInput).attr("param-str") ? $(sameBreedPreferencesInput).attr("param-str") : "");
                    
                    queryUrl = peopleUrl + "?search=" + searchValue + sfpiSelected  + sbpiSelected;
                    queryClassRemoved = "sp-pc-bi-pe";
                    queryEndResultConfig = [1];
                    resultAjax(queryCont, queryUrl, queryClassRemoved, queryEndResultConfig);
               });
          });
     }

     function resultContainerCreator (title) {
          let cont = document.createElement("div");
          cont.setAttribute("hidden", "true");
          cont.classList.add("d-flex", "flex-column", "container-fluid", "py-4", "sp-pc-dc-disp");
          let titleCont = document.createElement("span");
          titleCont.classList.add("h5", "font-weight-bold");
          titleCont.innerHTML = title;
          cont.append(titleCont);
          $(cont).insertBefore(baseCard);
          return cont;
     }

     function resultAjax (cont, url, classRemoved, endResultConfig) {
          $.ajax({
               type: "GET",
               url: url + "&pagination_no=" + paginationNo,
               beforeSend: function () {
                    loading.show();
                    doneAjax = false;
                    impasseBadge.attr("hidden", "true");
               },
               success: function (response) {
                    cont.removeAttribute("hidden");
                    for (item of response) {
                         let card = $(baseCard).clone().removeAttr("hidden").removeClass("sp-pc-bi");
                         
                         card.find("." + classRemoved).remove();
                         card.find("img").attr("src", card.find("img").attr("src") + item["photo"]);

                         if (item["username"]) {
                              let nameCont = card.find(".pc-us-n").html(item["name"]);
                              nameCont.attr("href", nameCont.attr("href") + item["username"]);
                              card.find(".pc-us-un").html("@" + item["username"]);
                         }

                         if (item["bio"]) {
                              let nameCont = card.find(".pc-pe-n").html(item["name"]);
                              nameCont.attr("href", nameCont.attr("href").replace("//", "/" + item["public_id"] + "/"));
                              if (item["status"] == 1) {
                                   card.find(".pc-pe-st").html("Status: <span class='badge badge-pill badge-primary'>Open for adoption</span>");
                              } else if (item["status"] == 2) {
                                   card.find(".pc-pe-st").html("Status: <span class='badge badge-pill badge-secondary'>Deceased</span>");
                              }
                              card.find(".pc-pe-bi").html(card.find(".pc-pe-bi").html() + item["bio"]);
                              card.find(".pc-pe-bd").html(card.find(".pc-pe-bd").html() + moment(item["birthday"]).format('LL'));
                              card.find(".pc-pe-sx").html(card.find(".pc-pe-sx").html() + item["sex"]);
                              card.find(".pc-pe-sp").html(card.find(".pc-pe-sp").html() + item["group_name"]);
                              card.find(".pc-pe-br").html(card.find(".pc-pe-br").html() + item["subgroup_name"]);
                         }
                         cont.append(card[0]);
                    }
                    if (endResultConfig[0] == 0) {
                         // all end result card
                         let endCard = document.createElement("a");
                         endCard.setAttribute("href", endResultConfig[1]);
                         endCard.classList.add("btn", "mx-auto", "btn-primary", "mt-3", "btn-block");
                         endCard.innerHTML = "See more";
                         cont.append(endCard);
                    } else if (endResultConfig[0] == 1) {
                         activateScrollPagination = true;
                    }
                    loading.hide();
               },
               complete: function (xhr) {
                    if (xhr.status == 404) {
                         doneAjax = false;
                         loading.hide();
                         impasseBadge.removeAttr("hidden");
                         if (endResultConfig[0] == 0) {
                              $(cont).remove();
                         }
                         if (paginationNo == 1) {
                              impasseBadge.html("No results found.");
                         } else {
                              impasseBadge.html("Nothing more to load.");
                         }
                    } else {
                         doneAjax = true;
                         paginationNo += 1;
                    }
               }
          });
     }

     function specieBreedInputDynamicAjax (specieSelectInput, breedSelectInput) {
          let specieId = specieSelectInput.value;
          $.ajax({
               type: "GET",
               url: "/breed/parent/" + specieId,
               success: function (response) {
                    breedSelectInput.append(createOptionElem ("All", 0, null));
                    for (let breed of response) {
                         let opt = createOptionElem (breed["name"], breed["public_id"], [["param-str", "&subgroup_id=" + breed["public_id"]]]);
                         breedSelectInput.append(opt);
                    }
               },
               complete: function () {
                    breedSelectInput.removeAttribute("disabled");
               }
          });
     }

     function createOptionElem (innerHTML, value, attribTupleList) {
          let opt = document.createElement("option");
          opt.innerHTML = innerHTML;
          opt.value = value;
          if (attribTupleList) {
               for (attribTuple of attribTupleList) {
                    opt.setAttribute(attribTuple[0], attribTuple[1]);
               }
          }
          return opt;
     }
});

document.querySelectorAll(".autocomplete").forEach((div) => {
     let inp = div.querySelectorAll("input")[0];
     let pidHolder = div.querySelectorAll("input")[1];
     let mediaStorage = div.getAttribute("media-storage");
     let url = div.getAttribute("href");
     let itemBaseUrl = div.getAttribute("item-base-url");
     let searchType = div.getAttribute("search-type");
     let searchInputWidthBL = 209;
     let fillerInputWidthBL = 313;
     var currentFocus;
     var typingTimer;
     var doneTypingInterval = 1000;
     inp.addEventListener("input", function(e) {
          window.clearTimeout(typingTimer);
          var a, b, i, val = this.value;
          closeAllLists();
          if (!val) { return false;}
          currentFocus = -1;
          a = document.createElement("DIV");
          a.style.overflowY = "scroll"
          a.setAttribute("id", this.id + "autocomplete-list");
          a.setAttribute("class", "autocomplete-items");
          this.parentNode.appendChild(a);
          typingTimer = setTimeout(function () {
               $.ajax({
                    type: "GET",
                    url: url + "?search=" + val,
                    beforeSend: function () {
                         let b = document.createElement("DIV");
                         b.classList.add("d-flex", "flex-row", "justify-content-start", "align-items-center");
                         if (searchType == "filler") {
                              b.style.width = fillerInputWidthBL + "px";
                         } else if (searchType == "searcher") {
                              b.style.width = searchInputWidthBL + "px";
                         }
                         let spinner = document.createElement("div");
                         spinner.classList.add("spinner-grow", "text-primary", "mx-auto");
                         spinner.setAttribute("role", "status");
                         b.append(spinner);
                         a.append(b);
                    },
                    success: function (response) {
                         a.innerHTML = "";
                         userAutocomplete(a, val, response);
                    },
                    complete: function (xhr) {
                         if (xhr.status == 404) {
                              a.innerHTML = "";
                              let b = document.createElement("DIV");
                              b.classList.add("d-flex", "justify-content-center");
                              if (searchType == "filler") {
                                   b.style.width = fillerInputWidthBL + "px";
                              } else if (searchType == "searcher") {
                                   b.style.width = searchInputWidthBL + "px";
                              }
                              b.innerHTML = "No results found";
                              a.append(b);
                         }
                    }
               });
          }, doneTypingInterval);
     });

     function userAutocomplete (a, val, response) {
          if (searchType == "filler") {
               for (let user of response) {
                    let b = document.createElement("DIV");
                    b.style.width = fillerInputWidthBL + "px";
                    b.classList.add("d-flex", "flex-row", "justify-content-start", "align-items-center");
                    let profPic = document.createElement("img");
                    profPic.setAttribute("src", mediaStorage + user["photo"]);
                    profPic.classList.add("home-content-profPic", "mr-3");
                    b.append(profPic);
                    let b0 = document.createElement("DIV");
                    b0.classList.add("d-flex", "flex-column");
                    var nameSubstringMatchPosition = user.name.toUpperCase().indexOf(val.toUpperCase());
                    var usernameSubstringMatchPosition = user.username.toUpperCase().indexOf(val.toUpperCase());
                    if (nameSubstringMatchPosition !== -1) {
                         b0.innerHTML += "<span>" + [user.name.slice(0, nameSubstringMatchPosition), "<strong>", user.name.slice(nameSubstringMatchPosition, nameSubstringMatchPosition + val.length), "</strong>", user.name.slice(nameSubstringMatchPosition + val.length)].join('') + "</span>";
                    } else {
                         b0.innerHTML += "<span>" + user.name + "</span>";
                    }
                    if (usernameSubstringMatchPosition !== -1) {
                         b0.innerHTML += "<span class='small tex-muted mt-1'>@" + [user.username.slice(0, usernameSubstringMatchPosition), "<strong>", user.username.slice(usernameSubstringMatchPosition, usernameSubstringMatchPosition + val.length), "</strong>", user.username.slice(usernameSubstringMatchPosition + val.length)].join('') + "</span>";
                    } else {
                         b0.innerHTML += "<span class='small tex-muted mt-1'>@" + user.username + "</span>";
                    }
                    b.append(b0);
                    b.addEventListener("click", function(e) {
                         inp.value = user.name;
                         pidHolder.value = user.public_id;
                         closeAllLists();
                    });
                    a.appendChild(b);
               }
          } else if (searchType == "searcher") {
               for (let user of response) {
                    let b = document.createElement("div");
                    b.style.width = searchInputWidthBL + "px";
                    let bi = document.createElement("a");
                    bi.classList.add("d-flex", "flex-row", "justify-content-start", "align-items-center", "text-dark", "text-decoration-none");
                    bi.setAttribute("href", itemBaseUrl + "/" + user["username"]);
                    let profPic = document.createElement("img");
                    profPic.setAttribute("src", mediaStorage + user["photo"]);
                    profPic.classList.add("home-content-profPic", "mr-3");
                    bi.append(profPic);
                    let b0 = document.createElement("div");
                    b0.classList.add("d-flex", "flex-column");
                    var nameSubstringMatchPosition = user.name.toUpperCase().indexOf(val.toUpperCase());
                    var usernameSubstringMatchPosition = user.username.toUpperCase().indexOf(val.toUpperCase());
                    if (nameSubstringMatchPosition !== -1) {
                         b0.innerHTML += "<span>" + [user.name.slice(0, nameSubstringMatchPosition), "<strong>", user.name.slice(nameSubstringMatchPosition, nameSubstringMatchPosition + val.length), "</strong>", user.name.slice(nameSubstringMatchPosition + val.length)].join('') + "</span>";
                    } else {
                         b0.innerHTML += "<span>" + user.name + "</span>";
                    }
                    if (usernameSubstringMatchPosition !== -1) {
                         b0.innerHTML += "<span class='small tex-muted mt-1'>@" + [user.username.slice(0, usernameSubstringMatchPosition), "<strong>", user.username.slice(usernameSubstringMatchPosition, usernameSubstringMatchPosition + val.length), "</strong>", user.username.slice(usernameSubstringMatchPosition + val.length)].join('') + "</span>";
                    } else {
                         b0.innerHTML += "<span class='small tex-muted mt-1'>@" + user.username + "</span>";
                    }
                    bi.append(b0);
                    b.append(bi);
                    a.appendChild(b);
               }
               let b = document.createElement("DIV");
               b.style.width = searchInputWidthBL + "px";
               let bi = document.createElement("a");
               bi.classList.add("d-flex", "justify-content-center", "align-items-center", "text-dark", "text-decoration-none");
               bi.setAttribute("href", "/search/all?value=" + val);
               bi.innerHTML = "Search more for&nbsp;<span class='font-weight-bold'>" + val + "</span>" ;
               b.append(bi);
               a.append(b);
          }
     }

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
});

function abbreviateNumber(value) {
    var newValue = value;
    if (value >= 1000) {
        var suffixes = ["", "k", "m", "b","t"];
        var suffixNum = Math.floor( (""+value).length/3 );
        var shortValue = '';
        for (var precision = 2; precision >= 1; precision--) {
            shortValue = parseFloat( (suffixNum != 0 ? (value / Math.pow(1000,suffixNum) ) : value).toPrecision(precision));
            var dotLessShortValue = (shortValue + '').replace(/[^a-zA-Z 0-9]+/g,'');
            if (dotLessShortValue.length <= 2) { break; }
        }
        if (shortValue % 1 != 0)  shortValue = shortValue.toFixed(1);
        newValue = shortValue+suffixes[suffixNum];
    }
    return newValue;
}

document.querySelectorAll(".ctf-c").forEach((cont) => {
     let loading = $(cont).find(".ctf-c-ld");
     let baseCard = $(cont).find(".ctf-c-bi");

     ajaxToFollow();
     function ajaxToFollow() {
          var cardsDown = 3;
          $.ajax({
               type: "GET",
               url: "/circle/preference?pagination_no=1",
               success: function (data) {
                    for (circle of data) {
                         let newCard = baseCard.clone().addClass("list-item-disposable").attr("hidden", false); 
                         let followBtn = newCard.find("button").attr("circle-pid", circle["public_id"]);
                         followBtn.one("click", function (e) {
                              $.ajax({
                                   type: "POST",
                                   url: "/circle/" + $(this).attr("circle-pid") + "/join?is_async=1",
                         
                                   success: function () {
                                        newCard.closest(".ctf-c").find(".ctf-c-bi").addClass("border-top");
                                        newCard.fadeTo(50, 0).slideUp(250, function (e) {
                                             newCard.closest(".ctf-c").find(".ctf-c-bi").removeClass("border-top");
                                             newCard.remove();
                                        });
                                        cardsDown -= 1;
                                        if (cardsDown == 0) {
                                             loading.show();
                                             ajaxToFollow();
                                        }
                                   }
                              });
                         });
                         newCard.find("img").attr("src", newCard.find("img").attr("src") + "/" + circle["photo"]);
                         let nameCont = newCard.find(".font-weight-bold");
                         nameCont.html(circle["name"]).attr("href", nameCont.attr("base-url").replace("//", "/" + circle["public_id"] + "/")).removeAttr("base-url");
                         let typeCont = newCard.find(".ctf-c-bi-t");
                         for (type of circle["_type"]) {
                              typeCont.html(typeCont.html() + " " + type["name"]);
                         }
                         newCard.find(".ctf-c-bi-mc").html((circle["member_count"] != 0 ? abbreviateNumber(circle["member_count"]) : "No") + " member" + (circle["member_count"] != 1 ? "s" : ""));
                         newCard.insertBefore(loading, null);
                    }
                    loading.hide();
               }
          });
     }
});

document.querySelectorAll(".btf-c").forEach((cont) => {
     let loading = $(cont).find(".btf-c-ld");
     let baseCard = $(cont).find(".btf-c-bi");
     ajaxToFollow();
     function ajaxToFollow() {
          var cardsDown = 3;
          $.ajax({
               type: "GET",
               url: "/business/preference?pagination_no=1",
               success: function (data) {
                    for (business of data) {
                         let newCard = baseCard.clone().addClass("list-item-disposable").attr("hidden", false);
                         let followBtn = newCard.find("button").attr("business-pid", business["public_id"]);
                         followBtn.one("click", function (e) {
                              $.ajax({
                                   type: "POST",
                                   url: "/business/" + $(this).attr("business-pid") + "/follow?is_async=1",
                                   success: function () {
                                        newCard.closest(".btf-c").find(".btf-c-bi").addClass("border-top");
                                        newCard.fadeTo(50, 0).slideUp(250, function (e) {
                                             newCard.closest(".btf-c").find(".btf-c-bi").removeClass("border-top");
                                             newCard.remove();
                                        });
                                        cardsDown -= 1;
                                        if (cardsDown == 0) {
                                             loading.show();
                                             ajaxToFollow();
                                        }
                                   }
                              });
                         });
                         newCard.find("img").attr("src", newCard.find("img").attr("src") + "/" + business["photo"]);
                         let nameCont = newCard.find(".font-weight-bold");
                         nameCont.html(business["name"]).attr("href", nameCont.attr("base-url").replace("//", "/" + business["public_id"] + "/")).removeAttr("base-url");
                         let typeCont = newCard.find(".btf-c-bi-t");
                         for (type of business["_type"]) {
                              typeCont.html(typeCont.html() + " " + type["name"]);
                         }
                         newCard.find(".btf-c-bi-fc").html((business["follower_count"] != 0 ? abbreviateNumber(business["follower_count"]) : "No") + " follower" + (business["follower_count"] != 1 ? "s" : ""));
                         newCard.insertBefore(loading, null);
                    }
                    loading.hide();
               }
          });
     }
});

document.querySelectorAll(".ptf-c").forEach((cont) => {
     let loading = $(cont).find(".ptf-c-ld");
     let baseCard = $(cont).find(".ptf-c-bi");
     ajaxToFollow();
     function ajaxToFollow() {
          var cardsDown = 3;
          $.ajax({
               type: "GET",
               url: "/pet/preference?pagination_no=1",
               success: function (data) {
                    for (pet of data) {
                         let newCard = baseCard.clone().addClass("list-item-disposable").attr("hidden", false);
                         let followBtn = newCard.find("button").attr("pet-pid", pet["public_id"]);
                         followBtn.one("click", function (e) {
                              $.ajax({
                                   type: "POST",
                                   url: "/pet/" + $(this).attr("pet-pid") + "/follow?is_async=1",
                                   success: function () {
                                        newCard.closest(".ptf-c").find(".ptf-c-bi").addClass("border-top");
                                        newCard.fadeTo(50, 0).slideUp(250, function (e) {
                                             newCard.closest(".ptf-c").find(".ptf-c-bi").removeClass("border-top");
                                             newCard.remove();
                                        });
                                        cardsDown -= 1;
                                        if (cardsDown == 0) {
                                             loading.show();
                                             ajaxToFollow();
                                        }
                                   }
                              });
                         });
                         newCard.find("img").attr("src", newCard.find("img").attr("src") + "/" + pet["photo"]);
                         let nameCont = newCard.find(".font-weight-bold");
                         nameCont.html(pet["name"]).attr("href", nameCont.attr("base-url").replace("//", "/" + pet["public_id"] + "/")).removeAttr("base-url");
                         newCard.find(".ptf-c-bi-s").html(pet["group_name"]);
                         newCard.find(".ptf-c-bi-b").html(pet["subgroup_name"]);
                         newCard.find(".ptf-c-bi-fc").html((pet["follower_count"] != 0 ? abbreviateNumber(pet["follower_count"]) : "No") + " follower" + (pet["follower_count"] != 1 ? "s" : ""));
                         newCard.insertBefore(loading, null);
                    }
                    loading.hide();
               }
          });
     }
});

$(function () {
     let cont = document.querySelector(".ccprf-c");
 
     let circleInput = $(cont).find("#ccpf-circle_type_input");
     let circleItems = circleInput.find("option");
     let circleBtnCont = $(cont).find(".ccpf-bc").eq(0);
     let circleBaseBtn = circleBtnCont.find(".ccpf-bi-b");
     for (item of circleItems) {
          let newButton = $(circleBaseBtn).clone().removeClass("cppf-bi").attr("hidden", false).val($(item).val());
          if ($(item).attr("selected")) {
               newButton.removeClass("btn-outline-secondary").addClass("btn-secondary");
          }
          newButton.html($(item).html());
 
          newButton.on("click", function (e) {
               if ($(this).hasClass("btn-secondary")) {
                    $(this).removeClass("btn-secondary").addClass("btn-outline-secondary");
               } else if ($(this).hasClass("btn-outline-secondary")) {
                    $(this).removeClass("btn-outline-secondary").addClass("btn-secondary");
               }
          });
 
          newButton.insertBefore(circleBaseBtn, null);
     }
 
     $(cont).one("submit", function (e) {
          e.preventDefault();
 
          circleInput.html("");
          activeCircles = circleBtnCont.find(".btn-secondary");
          for (breed of activeCircles) {
               let newOption = document.createElement("option");
               newOption.setAttribute("selected", "selected");
               newOption.value = $(breed).val();
               circleInput.append(newOption)
          }
          $(this).submit();
     });
});

$(function () {
     let cont = document.querySelector(".cbprf-c");
 
     let businessInput = $(cont).find("#cbpf-business_type_input");
     let businessItems = businessInput.find("option");
     let businessBtnCont = $(cont).find(".cbpf-bc").eq(0);
     let businessBaseBtn = businessBtnCont.find(".cbpf-bi-b");
     for (item of businessItems) {
          let newButton = $(businessBaseBtn).clone().removeClass("cppf-bi").attr("hidden", false).val($(item).val());
          if ($(item).attr("selected")) {
               newButton.removeClass("btn-outline-secondary").addClass("btn-secondary");
          }
          newButton.html($(item).html());
 
          newButton.on("click", function (e) {
               if ($(this).hasClass("btn-secondary")) {
                    $(this).removeClass("btn-secondary").addClass("btn-outline-secondary");
               } else if ($(this).hasClass("btn-outline-secondary")) {
                    $(this).removeClass("btn-outline-secondary").addClass("btn-secondary");
               }
          });
 
          newButton.insertBefore(businessBaseBtn, null);
     }
 
     $(cont).one("submit", function (e) {
          e.preventDefault();
 
          businessInput.html("");
          activeBusinesses = businessBtnCont.find(".btn-secondary");
          for (breed of activeBusinesses) {
               let newOption = document.createElement("option");
               newOption.setAttribute("selected", "selected");
               newOption.value = $(breed).val();
               businessInput.append(newOption)
          }
          $(this).submit();
     });
});

$(function () {
     let cont = document.querySelector(".cpprf-c");

     let breedInput = $(cont).find("#cppf-breed_subgroup_input");
     let breedItems = breedInput.find("option");
     let breedBtnCont = $(cont).find(".cppf-bbc").eq(0);
     let breedBaseButton = breedBtnCont.find(".cppf-bi-bb");
     for (item of breedItems) {
          let newButton = $(breedBaseButton).clone().removeClass("cppf-bi-b").attr("hidden", false).val($(item).val());
          if ($(item).attr("selected")) {
               newButton.removeClass("btn-outline-secondary").addClass("btn-secondary");
          }
          newButton.attr("parent-pid", $(item).attr("parent-pid"));
          newButton.html($(item).html());

          newButton.on("click", function (e) {
               if ($(this).hasClass("btn-secondary")) {
                    $(this).removeClass("btn-secondary").addClass("btn-outline-secondary");
               } else if ($(this).hasClass("btn-outline-secondary")) {
                    $(this).removeClass("btn-outline-secondary").addClass("btn-secondary");
               }
          });

          newButton.insertBefore(breedBaseButton, null);
     }

     let specieInput = $(cont).find("#cppf-specie_group_input");
     let specieItems = specieInput.find("option");
     let specieBtnCont = $(cont).find(".cppf-sbc");
     let specieBaseButton = specieBtnCont.find(".cppf-bi-sb");
     for (item of specieItems) {
          let newButton = $(specieBaseButton).clone().removeClass("cppf-bi-b").attr("hidden", false).val($(item).val());
          if ($(item).attr("selected")) {
               newButton.removeClass("btn-outline-secondary").addClass("btn-secondary");
          }
          newButton.html($(item).html());

          newButton.on("click", function (e) {
               if ($(this).hasClass("btn-secondary")) {
                    breedBtnCont.find("[parent-pid='" + $(this).val() + "']").remove();
                    $(this).removeClass("btn-secondary").addClass("btn-outline-secondary");
               } else if ($(this).hasClass("btn-outline-secondary")) {
                    $.ajax({
                         type: "GET",
                         url: "/breed/parent/" + $(this).val(),
               
                         success: function (data) {
                              for (breed of data) {
                                   let newButton = $(breedBaseButton).clone().removeClass("cppf-bi-b").attr("hidden", false).val(breed["public_id"]);
                                   newButton.attr("parent-pid", breed["parent_id"]);
                                   newButton.html(breed["name"]);

                                   newButton.on("click", function (e) {
                                        if ($(this).hasClass("btn-secondary")) {
                                             $(this).removeClass("btn-secondary").addClass("btn-outline-secondary");
                                        } else if ($(this).hasClass("btn-outline-secondary")) {
                                             $(this).removeClass("btn-outline-secondary").addClass("btn-secondary");
                                        }
                                   });

                                   newButton.insertBefore(breedBaseButton, null);
                              }
                         }
                    });

                    $(this).removeClass("btn-outline-secondary").addClass("btn-secondary");
               }
          });

          newButton.insertBefore(specieBaseButton, null);
     }

     $(cont).one("submit", function (e) {
          e.preventDefault();

          breedInput.html("");
          activeBreeds = breedBtnCont.find(".btn-secondary");
          for (breed of activeBreeds) {
               let newOption = document.createElement("option");
               newOption.setAttribute("selected", "selected");
               newOption.value = $(breed).val();
               breedInput.append(newOption)
          }
          $(this).submit();
     });
});

function outerHTML(node){
     return node.outerHTML || new XMLSerializer().serializeToString(node);
}

document.querySelectorAll(".cd-cont").forEach((commentCont) => {
     var paginationNo = 1;
     let commentLoading = $(commentCont).find(".cd-ld")[0];
     let commentStatus = $(commentCont).find(".cd-st")[0];
     let commentBaseItem = $(commentCont).find(".cd-ci")[0];
     var doneAjax = true;
     commentPopulate();
     $(window).scroll(function () {
          if(($(window).scrollTop() + $(window).height() == $(document).height()) && doneAjax) {
               paginationNo += 1;
               $(commentLoading).find(".spinner-grow").show();
               commentPopulate();
          }
     });
     function commentPopulate () {
          $.ajax({
               beforeSend: function () {
                    doneAjax = false;
               },
               type: "GET",
               url: $(commentBaseItem).attr("query-url") + "?pagination_no=" + paginationNo,
               success: function (data) {
                    if (data.length > 0) {
                         for (comment of data) {
                              let item = $(commentBaseItem).clone().removeAttr("hidden");
                              item.find(".post-user-photo").attr("src", item.find(".post-user-photo").attr("src") + comment["creator_photo"]);
                              item.find(".f-pi-dt-cn").html(comment["creator_name"]).attr("href", "/user/" + comment["creator_username"] + "/pets");
                              item.find(".p-dt").html(moment(comment["registered_on"]).fromNow());
                              if (comment["is_mine"] == 1) {
                                   item.find(".f-pi-dt-dd").find(".dc-mb").attr("method-action", "/comment/" + comment["public_id"] + "/delete").on("click", function(e) {
                                        $($(this).attr("data-target")).find(".modal-content").attr("action", $(this).attr("method-action"));
                                   });
                              } else {
                                   item.find(".f-pi-dt-dd").remove();
                              }
                              item.find(".f-pi-db-un").attr("href", "/user/" + comment["creator_username"] + "/pets").html("@" + comment["creator_username"]);
                              item.find(".post-body").html(comment["content"]);
                              if (comment["photo"]) {
                                   item.find(".f-pi-c-ph").find(".f-pi-c-pp").not(".f-pi-c-pp-i").remove();
                                   item.find(".f-pi-c-ph").find("img").eq(0).attr("src", item.find(".f-pi-c-ph").find("img").eq(0).attr("src") + comment["photo"][i]["filename"]);
                              } else {
                                   item.find(".f-pi-c-ph").remove();
                              }
                              item.insertBefore(commentLoading, null);
                         }
                         $(commentLoading).find(".spinner-grow").hide();
                         doneAjax = true;
                    } else {
                         $(commentLoading).find(".spinner-grow").hide();
                         doneAjax = false;
                         $(commentStatus).find(".badge").html((paginationNo > 1) ? "Nothing more to load." : "No comments found.")
                    }
                    
               }
          });
     }
});

document.querySelectorAll(".md-cont").forEach((mediaCont) => {
     var paginationNo = 1;
     let mediaLoading = $(mediaCont).find(".md-ld")[0];
     let mediaStatus = $(mediaCont).find(".md-st")[0];
     let mediaBaseItem = $(mediaCont).find(".md-pi")[0];
     var doneAjax = true;
     mediaPopulate();
     $(window).scroll(function () {
          if(($(window).scrollTop() + $(window).height() == $(document).height()) && doneAjax) {
               paginationNo += 1;
               $(mediaLoading).find(".spinner-grow").show();
               mediaPopulate();
          }
     });
     function mediaPopulate () {
          $.ajax({
               beforeSend: function () {
                    doneAjax = false;
               },
               type: "GET",
               url: $(mediaBaseItem).attr("query-url") + "?w_media_only=1&pagination_no=" + paginationNo,
               success: function (data) {
                    if (data.length > 0) {
                         let mediaItem = $(mediaBaseItem).clone().removeAttr("hidden");
                         var photoList = new Array();
                         for (post of data) {
                              for (media of post["photo"]) {
                                   let mediaObj = {
                                        public_id: post["public_id"],
                                        filename: media["filename"]
                                   }
                                   photoList.push(mediaObj);
                              }
                         }
                         if (photoList.length <= 3) {
                              mediaItem.find(".mc-ip").not(".mc-ip-" + "i".repeat(photoList.length)).remove();

                         } else {
                              mediaItem.find(".mc-ip").not(".mc-ip-iiii").remove();
                              if (photoList.length <= 6) {
                                   mediaItem.find(".mc-ip-iiii-m").remove();
                              } else {
                                   // 12 - (3 + 0) = 9/3 = 3        12 - 6 = 6 / 3 = 2
                                   let multiplyMiddleLength = ((photoList.length - (3 + (photoList.length % 3 == 0 ? 3 : photoList.length % 3)))/3);
                                   let baseMiddleItem = mediaItem.find(".mc-ip-iiii-m").eq(0);
                                   for (var i = 0; i < multiplyMiddleLength; i++) {
                                        let item = baseMiddleItem.clone();
                                        item.insertBefore(baseMiddleItem, null);
                                   }
                                   baseMiddleItem.remove();
                              }
                              if (photoList.length % 3 == 1) {
                                   mediaItem.find(".mc-ip-iiii-b").not(".mc-ip-iiii-b-i").remove();
                              } else if (photoList.length % 3 == 2) {
                                   mediaItem.find(".mc-ip-iiii-b").not(".mc-ip-iiii-b-ii").remove();
                              } else if (photoList.length % 3 == 0) {
                                   mediaItem.find(".mc-ip-iiii-b").not(".mc-ip-iiii-b-iii").remove();
                              }

                         }
          
                         for (let i = 0; i < photoList.length; i++) {
                              mediaItem.find("a").eq(i).attr("href", "/post/" + photoList[i]["public_id"] + "/comments");
                              mediaItem.find("img").eq(i).attr("src", mediaItem.find("img").eq(i).attr("src") + photoList[i]["filename"]);
                         }

                         $(mediaLoading).find(".spinner-grow").hide();
                         doneAjax = true;
                         mediaItem.insertBefore(mediaLoading, null);
                    } else {
                         $(mediaLoading).find(".spinner-grow").hide();
                         doneAjax = false;
                         $(mediaStatus).find(".badge").html((paginationNo > 1) ? "Nothing more to load." : "No media found.")
                    }
               }
          });
     };
});

function alertElemCreator (message, key="") {
     let asd = document.querySelector(".alert-frame");
     let alertCont = asd.querySelector(".container");
     let alert = document.createElement("div");
     alert.classList.add("toast", "alert-dismissible", "mt-2", "p-0", (key == "" ? "alert-primary" : "alert-danger"));

     // HEADER
     let toastHeader = document.createElement("div");
     toastHeader.classList.add("toast-header", "d-flex", "justify-content-between");
     let senderDetailsCont = document.createElement("div");
     senderDetailsCont.classList.add("d-flex", "flex-row", "mr-5");
     let senderPhoto = document.createElement("img");
     senderPhoto.setAttribute("src", asd.getAttribute("cu-pu"));
     senderPhoto.classList.add("toast-photo", "mr-2");
     senderDetailsCont.append(senderPhoto);
     let senderName = document.createElement("strong");
     senderName.classList.add("mr-auto");
     senderName.innerHTML = asd.getAttribute("cu-n");
     senderDetailsCont.append(senderName);
     toastHeader.append(senderDetailsCont);
     let timeSentCont = document.createElement("span");
     timeSentCont.classList.add("ml-5");
     timeSentCont.innerHTML = "Just now";
     toastHeader.append(timeSentCont);
     alert.append(toastHeader);

     // BODY
     let toastBody = document.createElement("div");
     toastBody.classList.add("toast-body");
     toastBody.innerHTML = (key == "" ? key : key + ": ") + message;
     alert.append(toastBody);

     $(alert).fadeTo(5000, 500).slideUp(500, function (e) {
          $(this).remove();
     });
     alertCont.append(alert);
}

document.querySelectorAll(".fd-cont").forEach((feedCont) => {
     var paginationNo = 1;
     let postCreatorCont = $(feedCont).find(".cr-pst-c")[0];
     let feedLoading = $(feedCont).find(".fd-ld")[0];
     let feedStatus = $(feedCont).find(".fd-st")[0];
     let feedPostItem = $(feedCont).find(".fd-pi")[0];
     var doneAjax = true;

     let postCreator = $(postCreatorCont).find(".pst-crt")[0];

     $(postCreator).on("submit", function (e) {
          e.preventDefault();
          $.ajax({
               type: "POST",
               url: $(this).attr("method-action"),
               data: $(this).serialize(),
               beforeSend: function () {
                    $(postCreator).find(".ldg-dbg").removeAttr("hidden");
                    $(postCreator).find(':input[type="submit"]').prop('disabled', true);
               },
               success: function (data) {
                    $(postCreator).find(".ldg-dbg").attr("hidden", "True");
                    $(postCreator).find(':input[type="submit"]').prop('disabled', false);
                    $(postCreator).closest(".modal").modal("hide");
                    $(postCreator).trigger("reset");
                    $(postCreator.querySelector(".crp-gallc-disposable")).remove();
                    if (data["status"] == 200) {
                         postElemCreator(feedPostItem, data["payload"], true).insertAfter(postCreatorCont, null);
                         alertElemCreator("Post created successfully.");
                    } else {
                         for (error of data["payload"]) {
                              alertElemCreator(error["message"], error["key"]);
                         }
                    }
               }
          });
     });

     postPopulate();
     $(window).scroll(function () {
          if(($(window).scrollTop() + $(window).height() == $(document).height()) && doneAjax) {
               paginationNo += 1;
               $(feedLoading).find(".spinner-grow").show();
               postPopulate();
          }
     });
     function postPopulate () {
          $.ajax({
               beforeSend: function () {
                    doneAjax = false;
               },
               type: "GET",
               url: $(feedPostItem).attr("query-url") + "?pagination_no=" + paginationNo,
               success: function (data) {
                    if (data.length > 0) {
                         for (post of data) {
                              postElemCreator(feedPostItem, post).insertBefore(feedLoading, null);
                         }
                         $(feedLoading).find(".spinner-grow").hide();
                         doneAjax = true;
                    } else {
                         $(feedLoading).find(".spinner-grow").hide();
                         doneAjax = false;
                         $(feedStatus).find(".badge").html((paginationNo > 1) ? "Nothing more to load." : "No posts found.")
                    }
                    
               }
          });
     }
});

function postElemCreator (feedPostItem, post, isNew=false) {
     let item = $(feedPostItem).clone().removeAttr("hidden");
     if (isNew == true) {
          item.find(".aff-new").addClass("border-primary");
     }
     item.find(".post-user-photo").attr("src", item.find(".post-user-photo").attr("src") + post["creator_photo"]);
     item.find(".f-pi-dt-cn").html(post["creator_name"]).attr("href", "/user/" + post["creator_username"] + "/pets");
     if (post["pinboard_id"]) {
          item.find(".p-anc-c").removeAttr("hidden");
          item.find(".f-pi-dt-pbcf").removeAttr("hidden").attr("href", "/business/" + post["pinboard_id"] + "/posts").html(post["pinboard_name"]);
     } else if (post["confiner_id"]) {
          item.find(".p-anc-c").removeAttr("hidden");
          item.find(".f-pi-dt-pbcf").removeAttr("hidden").attr("href", "/circle/" + post["confiner_id"] + "/posts").html(post["confiner_name"]);
     } else {
          item.find(".p-anc-c").remove();
          item.find(".f-pi-dt-pbcf").remove();
     }
     item.find(".p-dt").html(moment(post["registered_on"]).fromNow());
     if (post["is_mine"] == 1) {
          item.find(".f-pi-dt-dd").find(".dc-mb").attr("method-action", "/post/" + post["public_id"] + "/delete").on("click", function(e) {
               $($(this).attr("data-target")).find(".modal-content").attr("action", $(this).attr("method-action"));
          });
     } else {
          item.find(".f-pi-dt-dd").remove();
     }
     item.find(".f-pi-db-un").attr("href", "/user/" + post["creator_username"] + "/pets").html("@" + post["creator_username"]);
     item.find(".post-body").html(post["content"]);
     if (post["photo"]) {
          let photoListLength = post["photo"].length;

          item.find(".f-pi-c-ph").find(".f-pi-c-pp").not(".f-pi-c-pp-" + "i".repeat(photoListLength)).remove();

          for (let i = 0; i < photoListLength; i++) {
               item.find(".f-pi-c-ph").find("img").eq(i).attr("src", item.find(".f-pi-c-ph").find("img").eq(i).attr("src") + post["photo"][i]["filename"]);
          }
     } else {
          item.find(".f-pi-c-ph").remove();
     }
     let taggedPetsCont = item.find(".f-pi-prp");
     let petBaseTooltip = taggedPetsCont.find(".tooltip-cont");
     let taggedPetBaseItem = taggedPetsCont.find(".pt-tt-c");
     for (pet of post["subject"]) {
          let newTaggedPetItem = taggedPetBaseItem.clone().removeAttr("hidden").attr("href", "/pet/" + pet["public_id"] + "/posts");
          let petTooltip = petBaseTooltip.clone().removeAttr("hidden");
          petTooltip.find("img").attr("src", petBaseTooltip.find("img").attr("src") + pet["photo"]);
          petTooltip.find(".mt-1").html(pet["name"]);
          petTooltip.find(".small").html(pet["group_name"] + " &middot; " + pet["subgroup_name"]);
          petTooltip.find(".btn").attr("href", "/pet/" + pet["public_id"] + "/posts");
          newTaggedPetItem.find("img").attr("src", newTaggedPetItem.find("img").attr("src") + pet["photo"]).attr("title", outerHTML(petTooltip[0]));
          newTaggedPetItem.tooltip();
          newTaggedPetItem.on("mouseenter", function() {
               newTaggedPetItem.find(".rounded-circle").tooltip('show');
               let tooltipCont = document.querySelector(".tooltip");
               $(tooltipCont).on("mouseenter", function() {
                    newTaggedPetItem.find(".rounded-circle").tooltip('show');
               });
               $(tooltipCont).on("mouseleave", function() {
                    newTaggedPetItem.find(".rounded-circle").tooltip('hide');
               });
          });
          newTaggedPetItem.on("mouseleave", function() {
               newTaggedPetItem.find(".rounded-circle").tooltip('hide');
          });
          taggedPetsCont.append(newTaggedPetItem);
     } 
     petBaseTooltip.remove();
     taggedPetBaseItem.remove();

     $(item).attr("href", "/post/" + post["public_id"] + "/comments");
     [".f-pi-dt", ".post-body", ".f-pi-c-ph"].forEach((cont) => {
          item.find(cont).on("click", function () {
               window.location = $(item).attr("href");
          });
     });
     let likeCont = item.find(".post-footer").find(".pst-lk").attr("post-pid", post["public_id"]);
     likeCont.find(".p-lc").html(post["like_count"] + "&nbsp;&nbsp;");
     if (post["is_liked"] == 1) {
          likeCont.addClass("pst-lk-active").find("path").eq(1).removeClass("d-none");
     }
     likeCont.find("a").on("click", function () {
          if (likeCont.hasClass("pst-lk-active")) {
               likeCont.removeClass("pst-lk-active").find(".p-lc").html(parseInt(likeCont.find(".p-lc").html()) - 1);
               likeCont.find("path").eq(1).addClass("d-none");
          } else {
               likeCont.addClass("pst-lk-active").find(".p-lc").html(parseInt(likeCont.find(".p-lc").html()) + 1);
               likeCont.find("path").eq(1).removeClass("d-none");
          }
          $.ajax({
               type: "POST",
               url: "/post/" + likeCont.attr("post-pid") + "/like"
          });
     });
     let commentCont = item.find(".post-footer").find(".pst-cmt");
     commentCont.find("span").html(post["comment_count"] + "&nbsp;&nbsp;");
     commentCont.find("a").attr("href", "/post/" + post["public_id"] + "/comments");
     return item;
}

$(function () {
     $('[data-toggle="tooltip"]').tooltip();
     document.querySelectorAll(".pt-tt-c").forEach((cont) => {
          $(cont).on("mouseenter", function(e) {
               $(cont.querySelector(".rounded-circle")).tooltip('show');

               let tooltipCont = document.querySelector(".tooltip");
               $(tooltipCont).on("mouseenter", function(e) {
                    $(cont.querySelector(".rounded-circle")).tooltip('show');
               })
               $(tooltipCont).on("mouseleave", function(e) {
                    $(cont.querySelector(".rounded-circle")).tooltip('hide');
               })
          })
          $(cont).on("mouseleave", function(e) {
               $(cont.querySelector(".rounded-circle")).tooltip('hide');
          })
     })
})

document.querySelectorAll(".dp-mb").forEach((button) => {
     modal = document.querySelector(button.getAttribute("data-target"));
     button.addEventListener("click", (e) => {
          methodAction = button.getAttribute("method-action");
          modal.querySelector(".modal-content").setAttribute("action", methodAction);
     });
});

document.querySelectorAll(".ntf-nb").forEach((notifCont) => {
     let notifUnreadCount = notifCont.querySelector(".position-absolute");
     let notifMenu = notifCont.querySelector(".dropdown-menu");

     let postBaseUrl = notifCont.getAttribute("post-base-url");
     let petBaseUrl = notifCont.getAttribute("pet-base-url");
     let petPendFollBaseUrl = notifCont.getAttribute("pet-pf-base-url");
     let businessBaseUrl = notifCont.getAttribute("business-base-url");
     let circleBaseUrl = notifCont.getAttribute("circle-base-url");
     let circlePendFollBaseUrl = notifCont.getAttribute("circle-pf-base-url");

     $.ajax({
          type: "GET",
          url: "/notification/get",

          success: function (data) {
               notifUnreadCount.innerHTML = 0;
               if (data.length > 0) {
                    for (let notification of data) {
                         thisNotif = document.createElement("a");
                         thisNotif.classList.add("dropdown-item", "p-3", "d-flex", "flex-row", "align-items-center", "justify-content-between");
     
                         if (notification["is_read"] == false) {
                              notifUnreadCount.classList.remove("d-none");
                              notifUnreadCount.innerHTML = parseInt(notifUnreadCount.innerHTML) + 1;
                              thisNotif.classList.add("ntf-nb-unr");
                         }
                         notifImageCont = document.createElement("div");
                         notifImageCont.classList.add("mr-3", "ntf-nb-img-c");
                         notifImage = document.createElement("img");
                         notifImage.setAttribute("src", "/static/images/" + notification["sender_photo"]);
                         notifImageCont.append(notifImage);
                         thisNotif.append(notifImageCont);

                         notifMessage = document.createElement("span");
                         notifMessage.classList.add("small", "mr-3");
                         notifMessage.innerHTML = notification["content"];
                         thisNotif.append(notifMessage);

                         notifDatetime = document.createElement("div");
                         notifDatetime.classList.add("text-muted", "d-flex", "justify-content-end", "ntf-dt-vs");
                         notifDatetime.innerHTML =  moment(notification["registered_on"]).fromNow();
                         thisNotif.append(notifDatetime);

                         if (notification["post_subject_id"]) {
                              thisNotif.setAttribute("href", postBaseUrl.replace("//", "/" + notification["post_subject_id"] + "/"));
                         } else if (notification["circle_subject_id"]) {
                              if (notification["_type"] == 1) {
                                   thisNotif.setAttribute("href", circlePendFollBaseUrl.replace("//", "/" + notification["circle_subject_id"] + "/"));
                              } else {
                                   thisNotif.setAttribute("href", circleBaseUrl.replace("//", "/" + notification["circle_subject_id"] + "/"));
                              }
                         } else if (notification["pet_subject_id"]) {
                              if (notification["_type"] == 1) {
                                   thisNotif.setAttribute("href", petPendFollBaseUrl.replace("//", "/" + notification["pet_subject_id"] + "/"));
                              } else {
                                   thisNotif.setAttribute("href", petBaseUrl.replace("//", "/" + notification["pet_subject_id"] + "/"));
                              }
                         } else if (notification["business_subject_id"]) {
                              thisNotif.setAttribute("href", businessBaseUrl.replace("//", "/" + notification["business_subject_id"] + "/"));
                         }

                         notifMenu.append(thisNotif);
                         dividerCont = document.createElement("li");
                         notifMenu.append(dividerCont);
                    }
               } else {
                    let noNotifMessage = document.createElement("div");
                    noNotifMessage.style.width = "200px";
                    noNotifMessage.classList.add("ntf-e", "pt-2", "mx-4", "text-muted", "h6");
                    noNotifMessage.innerHTML = "You have no notifications as of now."
                    notifMenu.append(noNotifMessage);
               }
          }
     });
});

disablePostCreator(document.querySelector(".cr-post-facade-input"));
function disablePostCreator(input) {
     $(input).one("click", function(e) {
          petCount = parseInt(input.getAttribute("user-pet-count"));
          if (petCount === 0) {
               alertElemCreator("Create pet profile first.");
          } else {
               postCreatorMechanism(document.getElementById("createPostModal"));
          }
     });
}
function postCreatorMechanism (modal) {
     const modalBody = modal.querySelector(".modal-body");
     const form = modal.querySelector(".modal-content");
     const inputs = form.querySelectorAll("input");
     const submit = form.querySelector("input[type='submit']");

     const uploadPhotoFormGroup = modal.querySelector(".crp-ump-fg");
     const facadeUploadInput = uploadPhotoFormGroup.querySelector(".input-pretend-reverse");
     const actualUploadInput = uploadPhotoFormGroup.querySelector("input");

     facadeUploadInput.addEventListener("click", (e) => {
          actualUploadInput.click();
     });

     var photosArr = [];
     actualUploadInput.addEventListener("change", (e) => {
          $(".crp-gallc-disposable").remove();
          photosArr = [];
          if (actualUploadInput.files.length <= 4) {
               for (let file of actualUploadInput.files) {
                    photosArr.push(file);
               }
               displayLoadedPostPhotos();
          } else {
               alertElemCreator("You can choose up to 4 photos only.");
               actualUploadInput.value = ""
               $(modal).modal("hide");
          }
     });
     function readyGallDisp () {
          let baseGall = modalBody.querySelector("#crp-gallc-" + photosArr.length);  
          let gallDisp = $(baseGall).clone().removeAttr("id").removeClass("d-none").addClass("crp-gallc-disposable");
          let photoDispList = gallDisp.find(".inc-cnt");
          for (var i = 1; i <= 4; i++) {
               let file = photosArr[i-1];
               let disp =  $(photoDispList[i-1]).find(".inc-c");
               let imageClose = disp.find("span");
               let loading = $(photoDispList[i-1]).find(".inc-c-ld");
               let photo = disp.find(".img-fluid");
               let base64ContInput = modalBody.querySelector("#photo_" + i + "_input");
               base64ContInput.value = "";
               if (file) {
                    let reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.onload = () => {
                         photo.css("background-image", "url('" + reader.result + "')");
                         base64ContInput.value = reader.result;
                         loading.hide();
                    }
                    imageClose.one("click", function(e) {
                         let index = photosArr.indexOf(file);
                         if (index > -1) {
                              photosArr.splice(index, 1);
                         }
                         displayLoadedPostPhotos();
                    });
               }
          }
          return gallDisp[0];
     }
     function displayLoadedPostPhotos () {
          $(".crp-gallc-disposable").remove();
          if (photosArr.length) {     
               modalBody.insertBefore(readyGallDisp(), uploadPhotoFormGroup);
          } else {
               actualUploadInput.value = "";
          }
     }

     form.addEventListener("dragover", (e) => {
          e.preventDefault();

          form.classList.add("anticipate-drop-dark");
     });

     ["dragleave", "dragend"].forEach((type) => {
          form.addEventListener(type, (e) => {
               form.classList.remove("anticipate-drop-dark");
          });
     });

     form.addEventListener("drop", (e) => {
          if (e.dataTransfer.files.length) {
               let regex = /^.*\.(jpg|jpeg|png)$/;

               if (regex.test(e.dataTransfer.files[0].name)) {
                    actualUploadInput.files = e.dataTransfer.files;
               }
          }

          form.classList.remove("anticipate-drop-dark");
     });
};

document.querySelectorAll(".pst-lk").forEach((buttonCont) => {
     buttonCont.querySelector("a").addEventListener("click", (e) => {
          if ($(buttonCont).hasClass("pst-lk-active")) {
               buttonCont.querySelector(".p-lc").innerHTML = parseInt(buttonCont.querySelector(".p-lc").innerHTML) - 1;
               $(buttonCont).removeClass("pst-lk-active");
               $(buttonCont.querySelectorAll("path")[1]).addClass("d-none");

          } else {
               buttonCont.querySelector(".p-lc").innerHTML = parseInt(buttonCont.querySelector(".p-lc").innerHTML) + 1;
               $(buttonCont).addClass("pst-lk-active");
               $(buttonCont.querySelectorAll("path")[1]).removeClass("d-none");
          }
          $.ajax({
               type: "POST",
               beforeSend: function (request) {

               },
               url: "/post/" + buttonCont.getAttribute("post-pid") + "/like"
          });
     });
});

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
    $(this).remove();
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

document.querySelectorAll(".p-dt").forEach((dateCont) => {
     dateCont.innerHTML = moment(dateCont.innerHTML).fromNow()
});

document.querySelectorAll(".pi-bd").forEach((dateCont) => {
     dateCont.innerHTML = moment(dateCont.innerHTML).format('LL');
});