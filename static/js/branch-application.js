$(document).ready(function () {
  $("input[type=file]").on("change", function () {
    // console.log($(this)[0].files.item(0).size);
  });

$("#dob").on("keypress,keyup, keydown", function (e) {
  e.preventDefault();
  $("#dob").val("");
  return false;
})
  var stateList = getStateListHTML();
  $("#centerState").html(stateList);
  $("#centerState").on("change", function () {
    $("#centerDistrict").html(getDistrictListHTML($(this).val()));
  });

  $(".aff-category").on("change", function () {
    var total = 0;
    $(".total-amt-wrap").hide();
    $.each($(".aff-category"), function (i, input) {
      var value = $(input).val();
      var isChecked = $(input).is(":checked");
      if (isChecked) {
        switch (value) {
          case "COMPUTER_AND_IT":
          case "BEAUTICIAN_SOFT_SKILL":
            total += 5000;
            break;
          case "PARAMEDICAL":
            total += 10000;
            break;
          case "TEACHER_TRAINING":
          case "AMANAT_TRAINING":
          case "MECHANICAL_AND_TECHNICIAN":
          case "FIRE_AND_SAFETY":
            total += 10000;
            break;
        }
      }
    });
    $("#totalAmount").html("₹" + total + "/-");
    if (total > 0) {
      $(".total-amt-wrap").show();
    }
  });

  $("#branchApplication input").on("change", function () {
    if ($(this).attr("type") !== "file") {
      var val = $(this).val();
      $(this).val(val.trim());
    }
  });

  $("#branchApplication #dob").on("keyup", function(e){
    var keycode = e.keyCode;
    var date = $(this).val().trim();
    if(!(keycode == 8 || keycode ==46) &&  (date.length === 5 || date.length === 2)) {
      date += "/";
      $(this).val(date);
    } else if((keycode == 8 || keycode ==46) && date.length ===2 || date.length === 5) {
      date = date.slice(0, -1);
      $(this).val(date);
    }
  });

  $("#branchApplication").submit(function (e) {
    var errorList = [];
    $("#successWrapper").hide();
    $("#errorWrapper").hide();
    var isValid = validateBranchApplication();
    if (isValid) {
      var formData = new FormData(this);
      $(".branch-app-overlay").show();
      $.ajax({
        type: 'POST',
        url: "api/branch-application.php",
        enctype: 'multipart/form-data',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data, textStatus, xhr) {
          data = JSON.parse(data);
          $(".refNumber").html(data.referenceNumber);
          $(".application-wrapper")[0].scrollIntoView({ behavior: "smooth" });
          $("#successWrapper").show();
          $(".branch-app-overlay").hide();
          document.getElementById("branchApplication").reset();
        }, 
        error: function (xhr, ajaxOptions, thrownError) {
          var msg = "Something went wrong"; 
          if(xhr.statusText) {
            msg = xhr.statusText;
          }
          if(xhr.responseText){
            msg = msg + ": "+ xhr.responseText; 
          }
          $("#errorWrapper").html(msg).show();
          $(".branch-app-overlay").hide();
          $(".application-wrapper")[0].scrollIntoView({ behavior: "smooth" });
        }
    });
    } else {
      $(".application-wrapper")[0].scrollIntoView({ behavior: "smooth" });
    }
    e.preventDefault();
   
  });
});


function validateBranchApplication() {
  $(".error-wrapper").html("");
  var errorList = [];
  var mobileNumber = $("#mobileNumber").val().trim();
  var whatsappNumber = $("#whatsappNumber").val().trim();
  var referrerMobileNo = $("#referrerContactNo").val().trim();
  var centerPin = $("#centerPin").val().trim();
  var dob = $("#dob").val().trim();
  // var dateRegExp = new RegExp(/^((0[1-9]|[12][0-9]|3[01])(\/)(0[13578]|1[02]))|((0[1-9]|[12][0-9])(\/)(02))|((0[1-9]|[12][0-9]|3[0])(\/)(0[469]|11))(\/)\d{4}$/);

  if (mobileNumber.length < 10 || mobileNumber.length > 10 || isNaN(mobileNumber)) {
    errorList.push("Please enter a valid Mobile number.");
  }

  if (whatsappNumber.length < 10 || whatsappNumber.length > 10  || isNaN(whatsappNumber)) {
    errorList.push("Please enter a valid WhatsApp number.");
  }
  
  if (referrerMobileNo && (referrerMobileNo.length < 10 || referrerMobileNo.length > 10  || isNaN(referrerMobileNo))) {
    errorList.push("Please enter a valid referrer Mobile number.");
  }

  if (centerPin.length < 6 || centerPin.length > 6  || isNaN(centerPin)) {
    errorList.push("Please enter a valid PIN Code.");
  }


  // if(!dateRegExp.test(dob)) {
  //   errorList.push("Please enter a valid Date Of Birth");
  // }

  isAffiliationCategorySelected(errorList);

  if (errorList.length) {
    var errorHtml = "";
    errorList.forEach(function (error) {
      errorHtml += "<li>" + error + "</li>";
    });
    $(".error-wrapper").html("<ul>" + errorHtml + "</ul>");
    $(".error-wrapper").show();
  }

  return !errorList?.length;
}

function isAffiliationCategorySelected(errorList) {
  var isSelected = false;
  $.each($(".aff-category"), function (i, input) {
    if ($(input).is(":checked")) {
      isSelected = true;
    }
  });
  if (!isSelected) {
    errorList.push("Please select Affiliation Category.");
  }
  return isSelected;
}
