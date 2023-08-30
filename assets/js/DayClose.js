"use strict";

const modal_dayClose = document.querySelector(".modals");
const overlay_dayClose = document.querySelector(".overlay");
const btnCloseModal_dayClose = document.querySelector(".close-modal");
const btnsOpenModal_dayClose = document.querySelector("#show-modal-dayClose");

//open modal
if (btnsOpenModal_dayClose) {
  btnsOpenModal_dayClose.addEventListener("click", function () {
    modal_dayClose.classList.remove("hidden");
    overlay_dayClose.classList.remove("hidden");
  });
}

//close modal
if (btnCloseModal_dayClose) {
  btnCloseModal_dayClose.addEventListener("click", function () {
    modal_dayClose.classList.add("hidden");
    overlay_dayClose.classList.add("hidden");
  });
}

// //open modal
// btnsOpenModal.addEventListener("click", function() {
//   modal.classList.remove("hidden");
//   overlay.classList.remove("hidden");
// });

// //close modal
// btnCloseModal.addEventListener("click", function() {
//   modal.classList.add("hidden");
//   overlay.classList.add("hidden");
// });
let myFunction1 = (event) =>
  (document.getElementById("2000value").value = event.target.value * 2000);
document.getElementById("2000").addEventListener("keyup", function () {
  myFunction1(event);
  data_Calculations();
});
let myFunction2 = (event) =>
  (document.getElementById("500value").value = event.target.value * 500);
document.getElementById("500").addEventListener("keyup", function () {
  myFunction2(event);
  data_Calculations();
});
let myFunction3 = (event) =>
  (document.getElementById("200value").value = event.target.value * 200);
document.getElementById("200").addEventListener("keyup", function () {
  myFunction3(event);
  data_Calculations();
});
let myFunction4 = (event) =>
  (document.getElementById("100value").value = event.target.value * 100);
document.getElementById("100").addEventListener("keyup", function () {
  myFunction4(event);
  data_Calculations();
});
let myFunction5 = (event) =>
  (document.getElementById("50value").value = event.target.value * 50);
document.getElementById("50").addEventListener("keyup", function () {
  myFunction5(event);
  data_Calculations();
});
let myFunction6 = (event) =>
  (document.getElementById("20value").value = event.target.value * 20);
document.getElementById("20").addEventListener("keyup", function () {
  myFunction6(event);
  data_Calculations();
});
let myFunction7 = (event) =>
  (document.getElementById("10value").value = event.target.value * 10);
document.getElementById("10").addEventListener("keyup", function () {
  myFunction7(event);
  data_Calculations();
});
let myFunction8 = (event) =>
  (document.getElementById("5value").value = event.target.value * 5);
document.getElementById("5").addEventListener("keyup", function () {
  myFunction8(event);
  data_Calculations();
});
let myFunction9 = (event) =>
  (document.getElementById("2value").value = event.target.value * 2);
document.getElementById("2").addEventListener("keyup", function () {
  myFunction9(event);
  data_Calculations();
});
let myFunction10 = (event) =>
  (document.getElementById("1value").value = event.target.value * 1);
document.getElementById("1").addEventListener("keyup", function () {
  myFunction10(event);
  data_Calculations();
});
let myFunction11c = (event) =>
  (document.getElementById("20cv").value = event.target.value * 20);
document.getElementById("20c").addEventListener("keyup", function () {
  myFunction11c(event);
  data_Calculations();
});
let myFunction11 = (event) =>
  (document.getElementById("10cv").value = event.target.value * 10);
document.getElementById("10c").addEventListener("keyup", function () {
  myFunction11(event);
  data_Calculations();
});
let myFunction12 = (event) =>
  (document.getElementById("5cv").value = event.target.value * 5);
document.getElementById("5c").addEventListener("keyup", function () {
  myFunction12(event);
  data_Calculations();
});
let myFunction13 = (event) =>
  (document.getElementById("2cv").value = event.target.value * 2);
document.getElementById("2c").addEventListener("keyup", function () {
  myFunction13(event);
  data_Calculations();
});
let myFunction14 = (event) =>
  (document.getElementById("1cv").value = event.target.value * 1);
document.getElementById("1c").addEventListener("keyup", function () {
  myFunction14(event);
  data_Calculations();
});

const data_Calculations = () => {
  const _2000 = Number(document.getElementById("2000value").value);
  const _500 = Number(document.getElementById("500value").value);
  const _200 = Number(document.getElementById("200value").value);
  const _100 = Number(document.getElementById("100value").value);
  const _50 = Number(document.getElementById("50value").value);
  const _20 = Number(document.getElementById("20value").value);
  const _10 = Number(document.getElementById("10value").value);
  const _5 = Number(document.getElementById("5value").value);
  const _2 = Number(document.getElementById("2value").value);
  const _1 = Number(document.getElementById("1value").value);
  const _20c = Number(document.getElementById("20cv").value);
  const _10c = Number(document.getElementById("10cv").value);
  const _5c = Number(document.getElementById("5cv").value);
  const _2c = Number(document.getElementById("2cv").value);
  const _1c = Number(document.getElementById("1cv").value);
  const count =
    _2000 +
    _500 +
    _200 +
    _100 +
    _50 +
    _20 +
    _10 +
    _5 +
    _2 +
    _1 +
    _20c +
    _10c +
    _5c +
    _2c +
    _1c;
  document.getElementById("CalculatedAmount").value = count;
  // console.log(count)
  return count;
};

const CashBookReport = () => {
  try {
    // const BranchName = document.getElementById("CashBookBranchName").value
    // const FromDate = document.getElementById("fromDateRange").value
    // const ToDate = document.getElementById("toDateRange").value
    // $.ajax({
    //     type: "GET",
    //     url: "/CashBookReport",
    //     data: {
    //         Branch_Name: BranchName,
    //         From_Date: FromDate,
    //         To_Date: ToDate
    //     },
    //     success: function(data) {
    //         // console.log(JSON.parse(data.data_json));
    //         console.log(data.ClosingBalance);
    //         // document.getElementById("OTPNUMBER").value = Number(data.OTP);
    //     }
    // })
    document.getElementById("pdf-form").submit();
  } catch (error) {
    console.log("Something Went Wrong");
  }
};
