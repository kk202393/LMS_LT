$('#branchname').change(function() {
    var id = $(this).find(":selected").text();
    // var eml = this.parentNode.children[2]
    console.log(id)
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
})




// $('#age').change(function() {
//     var id = $(this).find(":selected").val();
//     console.log(id.getTime());
//     if (id < 18) {
//         alert("age????")
//     }


// })