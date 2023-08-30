const Calculated_Amount = () => {
  document.getElementById("ClosingAmount").value =
    document.getElementById("closingAmount").value;
  document.getElementById("BranchName").value =
    document.getElementById("Branch_Name").value;
};

const dataCalculations = async () => {
  let modal = document.querySelector(".modals");
  let overlay = document.querySelector(".overlay");
  let btnCloseModal = document.querySelector(".close-modal");
  let btnsOpenModal = document.querySelector("#show-modal");
  const paidAmount = Number(document.getElementById("closingAmount").value);
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
  const count = Number(
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
      _1c
  );
  document.getElementById("CalculatedAmount").value = count;
  // console.log(count)
  if (count !== paidAmount) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "You Enter Wrong Amount!",
    });
  } else {
    await currencyCount(count);
    // console.log("this condition run")
    modal.classList.add("hidden");
    overlay.classList.add("hidden");
    $.ajax({
      type: "GET",
      url: "/TotalAmount",
      data: {
        TotalAmount: count,
      },
      success: function (data) {
        if (data.TotalAmount) {
          Swal.fire({
            icon: "success",
            title: "Great Job",
            text: "Day Close Amount Submitted Successfully",
          });
          document.getElementById("CalculatedBalance").value = data.TotalAmount;
        }
      },
    });
  }
  return count;
};
const currencyCount = (TotalAmount) => {
  const _2000 = Number(document.getElementById("2000").value);
  const _500 = Number(document.getElementById("500").value);
  const _200 = Number(document.getElementById("200").value);
  const _100 = Number(document.getElementById("100").value);
  const _50 = Number(document.getElementById("50").value);
  const _20 = Number(document.getElementById("20").value);
  const _10 = Number(document.getElementById("10").value);
  const _5 = Number(document.getElementById("5").value);
  const _2 = Number(document.getElementById("2").value);
  const _1 = Number(document.getElementById("1").value);
  const _20c = Number(document.getElementById("20c").value);
  const _10c = Number(document.getElementById("10c").value);
  const _5c = Number(document.getElementById("5c").value);
  const _2c = Number(document.getElementById("2c").value);
  const _1c = Number(document.getElementById("1c").value);
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
  const NoteCount = {
    branchDayCloseDate: document.getElementById("branchDayCloseDateId").value,
    Branch_name: document.getElementById("BranchName").value,
    Count: TotalAmount,
    Note2000: _2000,
    Note500: _500,
    Note200: _200,
    Note100: _100,
    Note50: _50,
    Note20: _20,
    Note10: _10,
    Note5: _5,
    Note2: _2,
    Note1: _1,
    coin20: _20c,
    coin10: _10c,
    Coin5: _5c,
    Coin2: _2c,
    Coin1: _1c,
  };
  $.ajax({
    type: "GET",
    url: "/cashNumber",
    data: {
      Amount: JSON.stringify(NoteCount),
    },
    success: function (data) {
      try {
        // console.log("try condition run")
        if (data.msg) {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: data.msg,
          }).then(() => {
            window.location.reload();
          });
        }
      } catch (error) {
        console.log("Somthing went wrong")
      }
    },
  });
};

$(document).ready(function () {
  $("#delete-button").click(function () {
    var record_id = $(this).data("record-id");
    $.ajax({
      type: "GET",
      url: "/deleteCassBookRecord",
      data: {
        accountTransactionId: record_id,
      },
      success: function (data) {
        if (data.success) {
          Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Record deleted successfully",
          }).then(() => {
            location.reload();
          });
        }
      },
      error: function (xhr, status, error) {
        console.error(xhr.responseText);
      },
    });
  });
});
