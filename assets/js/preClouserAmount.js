// ---------  -----------------------//
$("#Preclosure_Amount_add").click(function (event) {
  var custId = $(this).val();
  event.preventDefault();
  console.log("button clicked", custId);
  $.ajax({
    type: "GET",
    url: "/Preclosure_Amount",
    data: {
      cust_Id: custId,
    },
    success: function (data) {
      const Preclosure_Amount_Lable_Handler = document.getElementById(
        "Preclosure_Amount_add"
      ).innerHTML;
      LPF = Number((data.amount) * 0.0125)
      LPC = Number((data.amount) * 0.0375)
      netDisburseAmount = Number(data.amount) - (LPF + LPC + data.preclosureAmount)
      if (Preclosure_Amount_Lable_Handler !== "Remove Preclosure Amount") {
        document.getElementById("Preclosure_Amount_div").value = Math.round(data.preclosureAmount);
        document.getElementById("Net_Pay_Amount").value = Math.round(netDisburseAmount);
        document.getElementById("Preclosure_Amount_add").innerHTML =
          "Remove Preclosure Amount"; 
      } else {
        document.getElementById("Preclosure_Amount_div").value = Math.round(data.preclosureAmount);
        document.getElementById("Net_Pay_Amount").value = Number(data.amount) - (LPF + LPC );
        document.getElementById("Preclosure_Amount_add").innerHTML =
          "Add Preclosure Amount";
      }
      // $("#Net_Pay_Amount").val(Net_Pay_Amount);
    },
  });
});

// ---------  -----------------------//
