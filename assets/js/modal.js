const sendOTP = () => {
    try {
        const PhoneNumber = document.getElementById("id_PhoneNumber").value
        const OtpCount = Math.floor(Math.random() * (12 - 6 + 1)) + 6
            // console.log("customer phone number", PhoneNumber)
            // console.log(Math.floor(Math.random() * (12 - 6 + 1)) + 6)
        $.ajax({
            type: "GET",
            url: "/sendOTP",
            data: {
                Phone_Number: PhoneNumber,
                Otp_Count: OtpCount
            },
            success: function(data) {
                console.log(data);
                document.getElementById("OTPNUMBER").value = Number(data.OTP);
            }
        })
    } catch (error) {
        console.log("Something Went Wrong")
    }

}




const OTPverify = () => {
    try {
        if (Number(document.getElementById("OTPVALUE").value) === Number(document.getElementById("OTPNUMBER").value)) {
            Swal.fire({
                icon: 'success',
                title: 'Great!',
                text: 'Your OTP is correct',
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Oops...!',
                text: 'Your Enter Wrong OTP',
            });
        }

    } catch (error) {
        console.log("Something Went Wrong")
    }
}




