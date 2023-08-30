// --------- Region wise Branch start -----------------------//
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

// --------- Region wise Branch start -----------------------//

const fun = (name) => {
  fun2(name)
};


const fun2 = (num) =>{
    console.log(num)
    return num
}