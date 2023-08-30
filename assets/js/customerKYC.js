// --------- center Id filter start -----------------------//
  // Get the select element and the input field
  // const select = document.getElementById('center');
  // const filterInput = document.getElementById('filterInput');

  // // Add event listener to the input field
  // filterInput.addEventListener('keyup', filterOptions);

  // // Function to filter the options
  // function filterOptions() {
  //   // Get the value entered in the input field
  //   const filterValue = filterInput.value.toUpperCase();

  //   // Get all the options inside the select element
  //   const options = select.getElementsByTagName('option');
  //   select.focus();

  //   // Dispatch a mousedown event to open the options
  //   const event = new MouseEvent('mousedown', {
  //     bubbles: true,
  //     cancelable: true,
  //     view: window
  //   });

  //   select.dispatchEvent(event);

  //   // Loop through the options and hide/show based on the filter value
  //   for (let i = 0; i < options.length; i++) {
  //     const option = options[i];
  //     const text = option.textContent || option.innerText;

  //     if (text.toUpperCase().indexOf(filterValue) > -1) {
  //       option.style.display = '';
  //     } else {
  //       option.style.display = 'none';
  //     }
  //   }
  // }
// --------- center Id filter end -----------------------//



// --------- Region wise Branch start -----------------------//
$("#region").change(function () {
  var Product = $(this).val();
  // console.log(Product);
  $.ajax({
    type: "GET",
    url: "/Region_values",
    data: {
      Region: Product,
    },
    success: function (data) {
      $("#branch").html(data);
    },
  });
});

// --------- Region wise Branch start -----------------------//

// --------- branch wise center id start -----------------------//
$("#branch").change(function () {
  var duct = $(this).val();
  // console.log(duct);
  $.ajax({
    type: "GET",
    url: "/Branch_values",
    data: {
      loan_data: duct,
    },
    success: function (data) {
      // console.log(data);
      $("#center").html(data);
    },
  });
});

// --------- branch wise center id end -----------------------//

// --------- branch wise csoName start -----------------------//
$("#branch").change(function () {
  var branchID = $(this).val();
  $.ajax({
    type: "GET",
    url: "/csoName",
    data: {
      branchID,
    },
    success: function (data) {
      // console.log(data);
      $("#CSO_Name").html(data);
    },
  });
});

// --------- branch wise csoName end -----------------------//

// --------- state wise dist start -----------------------//
$("#id_State").change(function () {
  var dist = $(this).val();
  // console.log(dist);
  $.ajax({
    type: "GET",
    url: "/dist_data",
    data: {
      dist_data: dist,
    },
    success: function (data) {
      // confirm.log(data)
      $("#id_District").html(data);
    },
  });
});

// --------- state wise dist  end -----------------------//

// --------- state wise dist for update kyc-----------------------//
$("#id_State_update").change(function () {
  var dist = $(this).val();
  // console.log(dist);
  $.ajax({
    type: "GET",
    url: "/update_dist_data",
    data: {
      dist_data: dist,
    },
    success: function (data) {
      $("#id_District_update").html(data);
    },
  });
});

// --------- state wise dist for update kyc -----------------------//

// --------- state wise dist for update kyc - -----------------------//
$("#id_confirmState_update").change(function () {
  var dist = $(this).val();
  // console.log(dist);
  $.ajax({
    type: "GET",
    url: "/update_dist_data",
    data: {
      dist_data: dist,
    },
    success: function (data) {
      // console.log(data)
      $("#id_confirmDistricte_update").html(data);
    },
  });
});

// --------- state wise dist for update kyc ------------------------//

// --------- state wise dist start -----------------------//
$("#id_confirmState").change(function () {
  var dist = $(this).val();
  // console.log(dist);
  $.ajax({
    type: "GET",
    url: "/dist_data",
    data: {
      dist_data: dist,
    },
    success: function (data) {
      $("#id_confirmDistrict").html(data);
    },
  });
});

// --------- state wise dist  end -----------------------//

// --------- Customer Details from Aadhar card start -----------------------//
$("#Customer_data").on("click", function () {
  var data = $("#id_Aadhaar").val();
  // console.log(data);
  $.ajax({
    type: "GET",
    url: "/Customer_data",
    data: {
      customer_data: data,
    },
    success: function (data) {
      if (data.Customer_data === -1) {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "No Customer found Please add new Record",
        });
      } else {
        // console.log(data.MaritalStatus);
        document.getElementById("id_FirstName").value = data.FirstName;
        document.getElementById("id_LastName").value = data.LastName;
        document.getElementById("age").value = data.Age;
        $("#id_MaritalStatus").val(data.MaritalStatus);
        $("#id_Gender").val(data.Gender);
        document.getElementById("id_VoterCard").value = data.VoterCard;
        document.getElementById("txtDOB").value = data.DateOfBirth;
      }
    },
  });
});

// --------- Customer Details from Aadhar card end -----------------------//

// --------- get input field data start (under observation)-----------------------//

$("#id_LastName").on("click", function () {
  var data = $("#id_FirstName").val();
  // console.log(typeof(data));
  if (data == "12") {
    console.log(typeof data);
  }
});

// --------- get input field data start -----------------------//

// ---------age calculated function 1 -----------------------
function fnCalculateAge() {
  var userDateinput = document.getElementById("txtDOB").value;

  // convert user input value into date object
  var birthDate = new Date(userDateinput);
  // console.log(" birthDate" + birthDate);

  // get difference from current date;
  var difference = Date.now() - birthDate.getTime();

  var ageDate = new Date(difference);
  var calculatedAge = Math.abs(ageDate.getUTCFullYear() - 1970);
  console.log(`age in years: ${calculatedAge}`);
  if (calculatedAge < 18 || calculatedAge > 58) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Age must be greater than 18 year and less than 56 year!",
    });
    document.getElementById("txtDOB").value = " ";
  } else {
    document.getElementById("age").value = calculatedAge;
  }
}

// ---------age calculated function-----------------------

// ---------age calculated function 2 -----------------------
function fnCalculateAge2() {
  var userDateinput = document.getElementById("coInsurerdob").value;
  // console.log(userDateinput);

  // convert user input value into date object
  var birthDate = new Date(userDateinput);
  console.log(" birthDate" + birthDate);

  // get difference from current date;
  var difference = Date.now() - birthDate.getTime();

  var ageDate = new Date(difference);
  var calculatedAge = Math.abs(ageDate.getUTCFullYear() - 1970);
  if (calculatedAge < 18) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Age must be greater than 18 year and less than 56 year!",
    });
    document.getElementById("coInsurerdob").value = " ";
  } else if (calculatedAge > 58) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Age must be greater than 18 year and less than 56 year!",
    });
    document.getElementById("coInsurerdob").value = " ";
  } else {
    document.getElementById("co-Insurerage").value = calculatedAge;
  }
}

// ---------age calculated function-----------------------

// ---------age calculated function 3 -----------------------
function fnCalculateAge3() {
  var userDateinput = document.getElementById("NomineeDob").value;
  // console.log(userDateinput);

  // convert user input value into date object
  var birthDate = new Date(userDateinput);
  console.log(" birthDate" + birthDate);

  // get difference from current date;
  var difference = Date.now() - birthDate.getTime();

  var ageDate = new Date(difference);
  var calculatedAge = Math.abs(ageDate.getUTCFullYear() - 1970);
  if (calculatedAge < 18) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Age must be greater than 18 year and less than 56 year!",
    });
    document.getElementById("NomineeDob").value = " ";
  } else if (calculatedAge > 58) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Age must be greater than 18 year and less than 56 year!",
    });
    document.getElementById("NomineeDob").value = " ";
  } else {
    document.getElementById("NomineeAge").value = calculatedAge;
  }
}

// ---------age calculated function-----------------------

// ---------age calculated function 4 -----------------------
function fnCalculateAge4() {
  var userDateinput = document.getElementById("fsDOB").value;
  console.log(userDateinput);

  // convert user input value into date object
  var birthDate = new Date(userDateinput);
  console.log(" birthDate" + birthDate);

  // get difference from current date;
  var difference = Date.now() - birthDate.getTime();

  var ageDate = new Date(difference);
  var calculatedAge = Math.abs(ageDate.getUTCFullYear() - 1970);
  if (calculatedAge < 18) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Age must be greater than 18 year and less than 56 year!",
    });
    document.getElementById("fsDOB").value = " ";
  } else if (calculatedAge > 58) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "Age must be greater than 18 year and less than 56 year!",
    });
    document.getElementById("fsDOB").value = " ";
  } else {
    document.getElementById("NomineeAge").value = calculatedAge;
  }
}

function OnClick() {
  var AddLine1 = document.getElementById("id_AddressLine1").value;
  var AddLine2 = document.getElementById("id_AddressLine2").value;
  var AddLine3 = document.getElementById("id_AddressLine3").value;
  var pcode = document.getElementById("id_Pincode").value;
  var village = document.getElementById("id_Village").value;
  var id_State = document.getElementById("id_State").value;
  var id_District = document.getElementById("id_District").value;
  // console.log(id_State);
  // console.log(id_District);
  let check = document.getElementById("check");
  document.getElementById("id_confirmAddressLine1").value = check.checked
    ? AddLine1
    : null;
  document.getElementById("id_confirmAddressLine2").value = check.checked
    ? AddLine2
    : null;
  document.getElementById("id_confirmAddressLine3").value = check.checked
    ? AddLine3
    : null;
  document.getElementById("id_confirmPincode").value = check.checked
    ? pcode
    : null;
  document.getElementById("id_confirmVillage").value = check.checked
    ? village
    : null;
  document.getElementById("id_confirmState").value = check.checked
    ? id_State
    : null;
  {
    $.ajax({
      type: "GET",
      url: "/confirm_dist_data",
      data: {
        dist_data: id_District,
      },
      success: function (data) {
        // $("#id_District").html(data);
        // console.log(data.Dist_list)
        // console.log(data.Dist_id)
        // console.log(Dist_list)
        document.getElementById("id_confirmDistrict").innerHTML = check.checked
          ? "<option value='" +
            data.Dist_id +
            "'>" +
            data.Dist_list +
            "</option>"
          : null;
      },
    });
  }
}

// new js start

// variables
const inputs = document.querySelectorAll(".container-button input");
const body = document.body;
const modal = document.querySelector(".crop-modal");
const overlay = document.querySelector(".overlay");
const btnCloseModal = document.querySelector(".close-modal");
const cropImage = document.getElementById("cropImage");
const saveBtn = document.querySelector(".saveBtn");
let cropper = "";

// functions

const openModal = function () {
  // console.log("button clicked");
  modal.classList.remove("hidden");
  overlay.classList.remove("hidden");
  body.classList.add("stop-scroll");
};

const closeModal = function () {
  // console.log("close button clicked");
  modal.classList.add("hidden");
  overlay.classList.add("hidden");
  body.classList.remove("stop-scroll");
};

// event handler
if (btnCloseModal){
  btnCloseModal.addEventListener("click", closeModal);
  overlay.addEventListener("click", closeModal);
}


// file size formatter
const formatFileSize = function (bytes) {
  const sufixes = ["B", "kB", "MB", "GB", "TB"];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sufixes[i]}`;
};

// remove image
function removeImage(id) {
  const Remove = document.querySelector(`.remove-img${id}`);
  Remove.addEventListener("click", function () {
    //declare variable
    const previewImage = document.querySelector(`.image-preview__image${id}`);
    const previewDefaultText = document.querySelector(
      `.image-preview__default-text${id}`
    );
    const Text = document.getElementById(`image-details${id}`);
    const Input = document.getElementById(`inputFile${id}`);

    //operation
    previewImage.src = "";
    //Input.value = null; //SO happy to write this statments!!!!!!
    // console.log("Input value:  " + Input.value);
    previewImage.style.display = "none";
    previewDefaultText.style.display = "block";
    Text.style.display = "none";
    document.getElementsByClassName("image-preview")[id - 1].style.border =
      "2px dotted lightgrey";
  });
}

// crop functionality
inputs.forEach((input) => {
  input.addEventListener("change", function (e) {
    e.preventDefault();
    openModal();

    // create variables
    const inputId = e.target.id;
    const inputIdUniqueNumber = inputId.charAt(inputId.length - 1);

    // create reader object
    const reader = new FileReader();
    reader.readAsDataURL(e.target.files[0]);
    reader.onload = function (e) {
      let image = document.createElement("img");
      image.id = `image-${inputIdUniqueNumber}`;
      image.src = e.target.result;

      //clear cropImage
      cropImage.innerHTML = "";

      cropImage.appendChild(image);

      cropper = new Cropper(image, {
        viewMode: 1,
      });
    };
  });
});

// save button: preview Image + show file name & size + close modal+ REMOVE IMAGE
if(saveBtn){
saveBtn.addEventListener("click", function (e) {
  //create new variables
  const cropImageId = document
    .getElementById("cropImage")
    .querySelector("img").id;
  const cropImageUniqueNumber = cropImageId.charAt(cropImageId.length - 1);
  const savedImageSourceAddress = document.querySelector(
    `.image-preview__image${cropImageUniqueNumber}`
  );

  const previewDefaultText = document.querySelector(
    `.image-preview__default-text${cropImageUniqueNumber}`
  );
  const Text = document.querySelector(`#image-details${cropImageUniqueNumber}`);
  const inputFile = document.querySelector(
    `#inputFile${cropImageUniqueNumber}`
  );

  // canvas url
  const canvasSourceAddress = cropper
    .getCroppedCanvas({ width: "300" })
    .toDataURL();

  // assign canvas url
  savedImageSourceAddress.src = canvasSourceAddress;
  
  const uniqueId = new Date().getTime();
  var blob = dataURLtoBlob(canvasSourceAddress);
  var img = new File([blob], `${uniqueId}${cropImageUniqueNumber}.png`, {
    type: "image/png",
  });
  const container = new DataTransfer();
  container.items.add(img);
  function dataURLtoBlob(dataurl) {
    var arr = dataurl.split(","),
      mime = arr[0].match(/:(.*?);/)[1],
      bstr = atob(arr[1]),
      n = bstr.length,
      u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
  }
  // console.log(container.files);
  document.querySelector(
    `#image-preview__image${cropImageUniqueNumber}`
  ).files = container.files;
  //change css elements
  savedImageSourceAddress.style.display = "block";
  previewDefaultText.style.display = "none";
  Text.style.display = "block";
  Text.style.fontSize = "13px";

  //   Text.innerText = `${inputFile.files[0].name} \n ${formatFileSize(
  //     inputFile.files[0].size
  //   )}`;

  // callback functions
  closeModal();
  removeImage(cropImageUniqueNumber);
})};

// new js end
//--------Loan details fatch data from table start -------//
$("#id_Product").change(function () {
  var Product = $(this).val();
  $.ajax({
    type: "GET",
    url: "/loanDetailsAmount",
    data: {
      Product_name: Product,
    },
    success: function (data) {
      document.getElementById("id_LoanAmount").value = data.LoanAmount;
      document.getElementById("id_InterestRate").value = data.InterestRate;
      document.getElementById("id_RepayFrequency").value = data.RepayFrequency;
    },
  });
});

//--------Loan details fatch data from table end -------//

//--------Loan Form confermation code start -------//
function clicked() {
  if (confirm("Do you want to submit?")) {
    yourformelement.submit();
  } else {
    return false;
  }
}

//--------Loan Form confermation code end -------//

function blockSpecialChar(e) {
  var k;
  document.all ? (k = e.keyCode) : (k = e.which);
  return (k > 64 && k < 91) || (k > 96 && k < 123);
}
