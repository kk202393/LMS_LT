// --------- start -----------------------//
$("#id_user_Id").change(function () {
  var agentID = $(this).val();
  // console.log(agentID);
  $.ajax({
    type: "GET",
    url: "/agentDetails",
    data: {
      agent_ID: agentID,
    },
    success: function (data) {
      document.getElementById(
        "id_agents_Name"
      ).value = `${data[0].first_name} ${data[0].last_name}`;
    },
  });
});

// ---------  start -----------------------//

// ---------Loan EMI Calculate start -----------------------//
const installmentAmountCalculation = document.getElementById(
  "installmentAmountButton"
);
if (installmentAmountCalculation) {
  installmentAmountCalculation.addEventListener("click", loanEmi);
}
function loanEmi() {
  // var agentID = $(this).val();
  const loanAmount = document.getElementById("id_LoanAmount").value;
  const loanInterestRate = document.getElementById("id_InterestRate").value;
  const loanRepayFrequency = document.getElementById("id_RepayFrequency").value;
  const loanEmiMode = document.getElementById("id_loanMode").value;
  if (!loanAmount || !loanInterestRate || !loanRepayFrequency || !loanEmiMode) {
    window.alert("Please fill all fields");
  } else {
    $.ajax({
      type: "GET",
      url: "/installmentAmountButton",
      data: {
        loanAmount: loanAmount,
        loanInterestRate: loanInterestRate,
        loanRepayFrequency: loanRepayFrequency,
        loanEmiMode: loanEmiMode,
      },
      success: function (data) {
        document.getElementById("installmentAmount").value = Math.round(
          data.loanEmi
        );
      },
    });
  }
}

// ---------  Loan EMI Calculate end -----------------------//

//-----------center ID data -------------------------------//
const centerIdDetail = document.getElementById("centerIdButton");
if (centerIdDetail) {
  centerIdDetail.addEventListener("click", centerIdDetails);
}
function centerIdDetails() {
  const centerID = document.getElementById("centerID").value;
  if (!centerID) {
    window.alert("Please enter center ID");
  } else {
    $.ajax({
      type: "GET",
      url: "/centerIdDetail",
      data: {
        centerID: centerID,
      },
      success: function (data) {
        document.getElementById("id_center_name").value = data.centerName;
        document.getElementById("id_center_leader").value = data.centerLeader;
        $("#id_branch_Name")
          .find("option")
          .remove()
          .end()
          .append(
            `<option value="${data.branchName}">${data.branchName}</option>`
          );
        $("#id_agents_Name")
          .find("option")
          .remove()
          .end()
          .append(
            `<option value="${data.agentID}">${data.agentName}(${data.agentID})</option>`
          );
        console.log(data);
      },
    });
  }
}

//------------------------------- Edit Loan Data  -------------------------------//
const selectInput = document.getElementById('selectInput');
  const selectDropdown = document.getElementById('selectDropdown');
  const select = document.getElementById('center');
  const options = select.getElementsByTagName('option');


  const allOptions = [];
  // const options = ['Option 1', 'Option 2', 'Option 3', 'Another Option', 'Filtered Option'];

  // Function to populate the dropdown with filtered options
  function populateDropdown() {
    for (let i = 0; i < options.length; i++) {
      const option = options[i];
      // console.log(option.value)
      const text = option.textContent || option.innerText;
      if (!allOptions.includes(option)) {
        allOptions.push(option)
      }

      // if (text.toUpperCase().indexOf(filterValue) > -1) {
      //   optio.style.display = '';
      // } else {
      //   optio.style.display = 'none';
      // }
    }
    const filterValue = selectInput.value.toLowerCase();
    selectDropdown.innerHTML = '';

    const filteredOptions = allOptions.filter(option =>
      option.textContent.toLowerCase().includes(filterValue)
    );

    filteredOptions.forEach(allOptions => {
      const selectOption = document.createElement('div');
      selectOption.className = 'select-option';
      selectOption.textContent = allOptions.textContent;
      selectOption.addEventListener('click', () => {
        selectInput.value = allOptions.textContent || allOptions.innerText;
        document.getElementById("centerID").value = allOptions.value;
        selectDropdown.innerHTML = '';
      });
      selectDropdown.appendChild(selectOption);
    });
  }

  // Event listener for input changes
  selectInput.addEventListener('input', populateDropdown);

  // Event listener for opening the dropdown on input click
  selectInput.addEventListener('click', () => {
    if (selectDropdown.innerHTML !== '') {
      selectDropdown.innerHTML = '';
    } else {
      populateDropdown();
    }
  });
//-------------------------------------  Edit Loan Data  -------------------------//

//------------------------------------ update loan data -------------------------//
$(".button").click(function () {
  var loanID = $(this).val();
  $.ajax({
    type: "GET",
    url: "/updateLoanData",
    data: {
      loanID,
    },
    success: function (data) {
      if (data.loanActivateStatus === true) {
        Swal.fire({
          icon: "success",
          title: "Great!",
          text: "Loan is activated successfully",
        }).then((result) => {
          if (result.isConfirmed) {
            location.reload();
          }
        });
      } else if (data.loanActivateStatus === false) {
        Swal.fire({
          icon: "success",
          title: "Great!",
          text: "Loan is deactivated successfully",
        }).then((result) => {
          if (result.isConfirmed) {
            location.reload();
          }
        });
      }
    },
    error: function (xhr, status, error) {
      console.error(xhr.responseText);
    },
  });
});

//------------------------------------ update loan data -------------------------//

//-----------center ID data -------------------------------//

$("#branchname").change(function () {
  var id = $(this).find(":selected").text();
  // var eml = this.parentNode.children[2]
  console.log(id);
  // $.ajax({
  //     type: "GET",
  //     url: "/india/pluscart",
  //     data: {
  //         prod_id: id
  //     },
  //     success: function(data) {
  //         eml.innerText = data.quantity
  //         document.getElementById("amount").innerText = data.amount
  //         document.getElementById("totalamount").innerText = data.totalamount
  //         document.getElementById("totalamoun").innerText = data.totalamount
  //         document.getElementById("shippingamount").innerText = data.shipping_amount
  //         document.getElementById("discount").innerText = data.discount
  //         document.getElementById("dis").innerText = data.dis
  //     }
  // })
});

// $('#age').change(function() {
//     var id = $(this).find(":selected").val();
//     console.log(id.getTime());
//     if (id < 18) {
//         alert("age????")
//     }

// })
