// --------- Region wise Branch start -----------------------//
$("#region").change(function () {
    var Product = $(this).val();
    console.log(Product);
    $.ajax({
        type: "GET",
        url: "/Region_values",
        data: {
            Region: Product
        },
        success: function (data) {
            $("#branch").html(data);
        }
    })
});

// --------- Region wise Branch start -----------------------//



// --------- branch wise center id start -----------------------//
$("#branch").change(function () {
    var duct = $(this).val();
    console.log(duct);
    $.ajax({
        type: "GET",
        url: "/Branch_values",
        data: {
            loan_data: duct
        },
        success: function (data) {
            $("#center").html(data);
        }
    })
});

// --------- branch wise center id end -----------------------//



// --------- state wise dist start -----------------------//
$("#id_State").change(function () {
    var dist = $(this).val();
    // console.log(dist);
    $.ajax({
        type: "GET",
        url: "/dist_data",
        data: {
            dist_data: dist
        },
        success: function (data) {
            confirm.log(data)
            $("#id_District").html(data);
        }
    })
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
            dist_data: dist
        },
        success: function (data) {
            $("#id_District_update").html(data);
        }
    })
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
            dist_data: dist
        },
        success: function (data) {
            // console.log(data)
            $("#id_confirmDistricte_update").html(data);
        }
    })
});

// --------- state wise dist for update kyc ------------------------//





// --------- state wise dist start -----------------------//
$("#id_confirmState").change(function () {
    var dist = $(this).val();
    console.log(dist);
    $.ajax({
        type: "GET",
        url: "/dist_data",
        data: {
            dist_data: dist
        },
        success: function (data) {
            $("#id_confirmDistrict").html(data);
        }
    })
});

// --------- state wise dist  end -----------------------//







// --------- Customer Details from Aadhar card start -----------------------//
$('#Customer_data').on('click', function () {
    var data = $("#id_Aadhaar").val();
    // console.log(data);
    $.ajax({
        type: "GET",
        url: "/Customer_data",
        data: {
            customer_data: data
        },
        success: function (data) {
            if (data.Customer_data === -1) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'No Customer found Please add new Record',
                });
            } else {
                // console.log(data.MaritalStatus);
                document.getElementById("id_FirstName").value = data.FirstName;
                document.getElementById("id_LastName").value = data.LastName;
                document.getElementById("age").value = data.Age;
                $('#id_MaritalStatus').val(data.MaritalStatus);
                $('#id_Gender').val(data.Gender);
                document.getElementById("id_VoterCard").value = data.VoterCard;
                document.getElementById("txtDOB").value = data.DateOfBirth;
            }
        }
    })
});

// --------- Customer Details from Aadhar card end -----------------------//





// --------- Customer Details for Approved table start -----------------------//
// $('#Approved_Status').on('click', function () {
//     var data = $("#Approved_Application_No").val();
//     console.log(data);
//     $.ajax({
//         type: "GET",
//         url: "/Approved_Customer_data",
//         data: {
//             customer_data: data
//         },
//         success: function (data) {
//             console.log(data.Gender)
//             $("#id_OtherKYCIdtype").html(data.kycIdType)
//             // $("#id_Gender").html(data.Gender)
//             document.getElementById("id_Gender").innerHTML = "<option value='" + data.Gender + "'>" + data.Gender + "</option>";
//         }
//     })
// });

// --------- Customer Details for Approved tableend -----------------------//









// --------- get input field data start (under observation)-----------------------//

$('#id_LastName').on('click', function () {
    var data = $("#id_FirstName").val();
    // console.log(typeof(data));
    if (data == "12") {
        console.log(typeof (data));
    }
})

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
    if ((calculatedAge < 18) || (calculatedAge > 58)) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Age must be greater than 18 year and less than 56 year!',
        });
        document.getElementById("txtDOB").value = " "
    } else {
        document.getElementById('age').value = calculatedAge;
    };

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
            icon: 'error',
            title: 'Oops...',
            text: 'Age must be greater than 18 year and less than 56 year!',
        });
        document.getElementById("coInsurerdob").value = " "
    } else if (calculatedAge > 58) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Age must be greater than 18 year and less than 56 year!',
        });
        document.getElementById("coInsurerdob").value = " "
    } else {
        document.getElementById('co-Insurerage').value = calculatedAge;
    };

};

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
            icon: 'error',
            title: 'Oops...',
            text: 'Age must be greater than 18 year and less than 56 year!',
        });
        document.getElementById("NomineeDob").value = " "
    } else if (calculatedAge > 58) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Age must be greater than 18 year and less than 56 year!',
        });
        document.getElementById("NomineeDob").value = " "
    } else {
        document.getElementById('NomineeAge').value = calculatedAge;
    };


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
            icon: 'error',
            title: 'Oops...',
            text: 'Age must be greater than 18 year and less than 56 year!',
        });
        document.getElementById("fsDOB").value = " "
    } else if (calculatedAge > 58) {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Age must be greater than 18 year and less than 56 year!',
        });
        document.getElementById("fsDOB").value = " "
    } else {
        document.getElementById('NomineeAge').value = calculatedAge;
    };


}

// ---------age calculated function-----------------------

// --------------------state and district------------------

// var AndraPradesh = [
//     "Anantapur",
//     "Chittoor",
//     "East Godavari",
//     "Guntur",
//     "Kadapa",
//     "Krishna",
//     "Kurnool",
//     "Prakasam",
//     "Nellore",
//     "Srikakulam",
//     "Visakhapatnam",
//     "Vizianagaram",
//     "West Godavari",
// ];
// var ArunachalPradesh = [
//     "Anjaw",
//     "Changlang",
//     "Dibang Valley",
//     "East Kameng",
//     "East Siang",
//     "Kra Daadi",
//     "Kurung Kumey",
//     "Lohit",
//     "Longding",
//     "Lower Dibang Valley",
//     "Lower Subansiri",
//     "Namsai",
//     "Papum Pare",
//     "Siang",
//     "Tawang",
//     "Tirap",
//     "Upper Siang",
//     "Upper Subansiri",
//     "West Kameng",
//     "West Siang",
//     "Itanagar",
// ];
// var Assam = [
//     "Baksa",
//     "Barpeta",
//     "Biswanath",
//     "Bongaigaon",
//     "Cachar",
//     "Charaideo",
//     "Chirang",
//     "Darrang",
//     "Dhemaji",
//     "Dhubri",
//     "Dibrugarh",
//     "Goalpara",
//     "Golaghat",
//     "Hailakandi",
//     "Hojai",
//     "Jorhat",
//     "Kamrup Metropolitan",
//     "Kamrup (Rural)",
//     "Karbi Anglong",
//     "Karimganj",
//     "Kokrajhar",
//     "Lakhimpur",
//     "Majuli",
//     "Morigaon",
//     "Nagaon",
//     "Nalbari",
//     "Dima Hasao",
//     "Sivasagar",
//     "Sonitpur",
//     "South Salmara Mankachar",
//     "Tinsukia",
//     "Udalguri",
//     "West Karbi Anglong",
// ];
// var Bihar = [
//     "Araria",
//     "Arwal",
//     "Aurangabad",
//     "Banka",
//     "Begusarai",
//     "Bhagalpur",
//     "Bhojpur",
//     "Buxar",
//     "Darbhanga",
//     "East Champaran",
//     "Gaya",
//     "Gopalganj",
//     "Jamui",
//     "Jehanabad",
//     "Kaimur",
//     "Katihar",
//     "Khagaria",
//     "Kishanganj",
//     "Lakhisarai",
//     "Madhepura",
//     "Madhubani",
//     "Munger",
//     "Muzaffarpur",
//     "Nalanda",
//     "Nawada",
//     "Patna",
//     "Purnia",
//     "Rohtas",
//     "Saharsa",
//     "Samastipur",
//     "Saran",
//     "Sheikhpura",
//     "Sheohar",
//     "Sitamarhi",
//     "Siwan",
//     "Supaul",
//     "Vaishali",
//     "West Champaran",
// ];
// var Chhattisgarh = [
//     "Balod",
//     "Baloda Bazar",
//     "Balrampur",
//     "Bastar",
//     "Bemetara",
//     "Bijapur",
//     "Bilaspur",
//     "Dantewada",
//     "Dhamtari",
//     "Durg",
//     "Gariaband",
//     "Janjgir Champa",
//     "Jashpur",
//     "Kabirdham",
//     "Kanker",
//     "Kondagaon",
//     "Korba",
//     "Koriya",
//     "Mahasamund",
//     "Mungeli",
//     "Narayanpur",
//     "Raigarh",
//     "Raipur",
//     "Rajnandgaon",
//     "Sukma",
//     "Surajpur",
//     "Surguja",
// ];
// var Goa = ["North Goa", "South Goa"];
// var Gujarat = [
//     "Ahmedabad",
//     "Amreli",
//     "Anand",
//     "Aravalli",
//     "Banaskantha",
//     "Bharuch",
//     "Bhavnagar",
//     "Botad",
//     "Chhota Udaipur",
//     "Dahod",
//     "Dang",
//     "Devbhoomi Dwarka",
//     "Gandhinagar",
//     "Gir Somnath",
//     "Jamnagar",
//     "Junagadh",
//     "Kheda",
//     "Kutch",
//     "Mahisagar",
//     "Mehsana",
//     "Morbi",
//     "Narmada",
//     "Navsari",
//     "Panchmahal",
//     "Patan",
//     "Porbandar",
//     "Rajkot",
//     "Sabarkantha",
//     "Surat",
//     "Surendranagar",
//     "Tapi",
//     "Vadodara",
//     "Valsad",
// ];
// var Haryana = [
//     "Ambala",
//     "Bhiwani",
//     "Charkhi Dadri",
//     "Faridabad",
//     "Fatehabad",
//     "Gurugram",
//     "Hisar",
//     "Jhajjar",
//     "Jind",
//     "Kaithal",
//     "Karnal",
//     "Kurukshetra",
//     "Mahendragarh",
//     "Mewat",
//     "Palwal",
//     "Panchkula",
//     "Panipat",
//     "Rewari",
//     "Rohtak",
//     "Sirsa",
//     "Sonipat",
//     "Yamunanagar",
// ];
// var HimachalPradesh = [
//     "Bilaspur",
//     "Chamba",
//     "Hamirpur",
//     "Kangra",
//     "Kinnaur",
//     "Kullu",
//     "Lahaul Spiti",
//     "Mandi",
//     "Shimla",
//     "Sirmaur",
//     "Solan",
//     "Una",
// ];
// var JammuKashmir = [
//     "Anantnag",
//     "Bandipora",
//     "Baramulla",
//     "Budgam",
//     "Doda",
//     "Ganderbal",
//     "Jammu",
//     "Kargil",
//     "Kathua",
//     "Kishtwar",
//     "Kulgam",
//     "Kupwara",
//     "Leh",
//     "Poonch",
//     "Pulwama",
//     "Rajouri",
//     "Ramban",
//     "Reasi",
//     "Samba",
//     "Shopian",
//     "Srinagar",
//     "Udhampur",
// ];
// var Jharkhand = [
//     "Bokaro",
//     "Chatra",
//     "Deoghar",
//     "Dhanbad",
//     "Dumka",
//     "East Singhbhum",
//     "Garhwa",
//     "Giridih",
//     "Godda",
//     "Gumla",
//     "Hazaribagh",
//     "Jamtara",
//     "Khunti",
//     "Koderma",
//     "Latehar",
//     "Lohardaga",
//     "Pakur",
//     "Palamu",
//     "Ramgarh",
//     "Ranchi",
//     "Sahebganj",
//     "Seraikela Kharsawan",
//     "Simdega",
//     "West Singhbhum",
// ];
// var Karnataka = [
//     "Bagalkot",
//     "Bangalore Rural",
//     "Bangalore Urban",
//     "Belgaum",
//     "Bellary",
//     "Bidar",
//     "Vijayapura",
//     "Chamarajanagar",
//     "Chikkaballapur",
//     "Chikkamagaluru",
//     "Chitradurga",
//     "Dakshina Kannada",
//     "Davanagere",
//     "Dharwad",
//     "Gadag",
//     "Gulbarga",
//     "Hassan",
//     "Haveri",
//     "Kodagu",
//     "Kolar",
//     "Koppal",
//     "Mandya",
//     "Mysore",
//     "Raichur",
//     "Ramanagara",
//     "Shimoga",
//     "Tumkur",
//     "Udupi",
//     "Uttara Kannada",
//     "Yadgir",
// ];
// var Kerala = [
//     "Alappuzha",
//     "Ernakulam",
//     "Idukki",
//     "Kannur",
//     "Kasaragod",
//     "Kollam",
//     "Kottayam",
//     "Kozhikode",
//     "Malappuram",
//     "Palakkad",
//     "Pathanamthitta",
//     "Thiruvananthapuram",
//     "Thrissur",
//     "Wayanad",
// ];
// var MadhyaPradesh = [
//     "Agar Malwa",
//     "Alirajpur",
//     "Anuppur",
//     "Ashoknagar",
//     "Balaghat",
//     "Barwani",
//     "Betul",
//     "Bhind",
//     "Bhopal",
//     "Burhanpur",
//     "Chhatarpur",
//     "Chhindwara",
//     "Damoh",
//     "Datia",
//     "Dewas",
//     "Dhar",
//     "Dindori",
//     "Guna",
//     "Gwalior",
//     "Harda",
//     "Hoshangabad",
//     "Indore",
//     "Jabalpur",
//     "Jhabua",
//     "Katni",
//     "Khandwa",
//     "Khargone",
//     "Mandla",
//     "Mandsaur",
//     "Morena",
//     "Narsinghpur",
//     "Neemuch",
//     "Panna",
//     "Raisen",
//     "Rajgarh",
//     "Ratlam",
//     "Rewa",
//     "Sagar",
//     "Satna",
//     "Sehore",
//     "Seoni",
//     "Shahdol",
//     "Shajapur",
//     "Sheopur",
//     "Shivpuri",
//     "Sidhi",
//     "Singrauli",
//     "Tikamgarh",
//     "Ujjain",
//     "Umaria",
//     "Vidisha",
// ];
// var Maharashtra = [
//     "Ahmednagar",
//     "Akola",
//     "Amravati",
//     "Aurangabad",
//     "Beed",
//     "Bhandara",
//     "Buldhana",
//     "Chandrapur",
//     "Dhule",
//     "Gadchiroli",
//     "Gondia",
//     "Hingoli",
//     "Jalgaon",
//     "Jalna",
//     "Kolhapur",
//     "Latur",
//     "Mumbai City",
//     "Mumbai Suburban",
//     "Nagpur",
//     "Nanded",
//     "Nandurbar",
//     "Nashik",
//     "Osmanabad",
//     "Palghar",
//     "Parbhani",
//     "Pune",
//     "Raigad",
//     "Ratnagiri",
//     "Sangli",
//     "Satara",
//     "Sindhudurg",
//     "Solapur",
//     "Thane",
//     "Wardha",
//     "Washim",
//     "Yavatmal",
// ];
// var Manipur = [
//     "Bishnupur",
//     "Chandel",
//     "Churachandpur",
//     "Imphal East",
//     "Imphal West",
//     "Jiribam",
//     "Kakching",
//     "Kamjong",
//     "Kangpokpi",
//     "Noney",
//     "Pherzawl",
//     "Senapati",
//     "Tamenglong",
//     "Tengnoupal",
//     "Thoubal",
//     "Ukhrul",
// ];
// var Meghalaya = [
//     "East Garo Hills",
//     "East Jaintia Hills",
//     "East Khasi Hills",
//     "North Garo Hills",
//     "Ri Bhoi",
//     "South Garo Hills",
//     "South West Garo Hills",
//     "South West Khasi Hills",
//     "West Garo Hills",
//     "West Jaintia Hills",
//     "West Khasi Hills",
// ];
// var Mizoram = [
//     "Aizawl",
//     "Champhai",
//     "Kolasib",
//     "Lawngtlai",
//     "Lunglei",
//     "Mamit",
//     "Saiha",
//     "Serchhip",
//     "Aizawl",
//     "Champhai",
//     "Kolasib",
//     "Lawngtlai",
//     "Lunglei",
//     "Mamit",
//     "Saiha",
//     "Serchhip",
// ];
// var Nagaland = [
//     "Dimapur",
//     "Kiphire",
//     "Kohima",
//     "Longleng",
//     "Mokokchung",
//     "Mon",
//     "Peren",
//     "Phek",
//     "Tuensang",
//     "Wokha",
//     "Zunheboto",
// ];
// var Odisha = [
//     "Angul",
//     "Balangir",
//     "Balasore",
//     "Bargarh",
//     "Bhadrak",
//     "Boudh",
//     "Cuttack",
//     "Debagarh",
//     "Dhenkanal",
//     "Gajapati",
//     "Ganjam",
//     "Jagatsinghpur",
//     "Jajpur",
//     "Jharsuguda",
//     "Kalahandi",
//     "Kandhamal",
//     "Kendrapara",
//     "Kendujhar",
//     "Khordha",
//     "Koraput",
//     "Malkangiri",
//     "Mayurbhanj",
//     "Nabarangpur",
//     "Nayagarh",
//     "Nuapada",
//     "Puri",
//     "Rayagada",
//     "Sambalpur",
//     "Subarnapur",
//     "Sundergarh",
// ];
// var Punjab = [
//     "Amritsar",
//     "Barnala",
//     "Bathinda",
//     "Faridkot",
//     "Fatehgarh Sahib",
//     "Fazilka",
//     "Firozpur",
//     "Gurdaspur",
//     "Hoshiarpur",
//     "Jalandhar",
//     "Kapurthala",
//     "Ludhiana",
//     "Mansa",
//     "Moga",
//     "Mohali",
//     "Muktsar",
//     "Pathankot",
//     "Patiala",
//     "Rupnagar",
//     "Sangrur",
//     "Shaheed Bhagat Singh Nagar",
//     "Tarn Taran",
// ];
// var Rajasthan = [
//     "Ajmer",
//     "Alwar",
//     "Banswara",
//     "Baran",
//     "Barmer",
//     "Bharatpur",
//     "Bhilwara",
//     "Bikaner",
//     "Bundi",
//     "Chittorgarh",
//     "Churu",
//     "Dausa",
//     "Dholpur",
//     "Dungarpur",
//     "Ganganagar",
//     "Hanumangarh",
//     "Jaipur",
//     "Jaisalmer",
//     "Jalore",
//     "Jhalawar",
//     "Jhunjhunu",
//     "Jodhpur",
//     "Karauli",
//     "Kota",
//     "Nagaur",
//     "Pali",
//     "Pratapgarh",
//     "Rajsamand",
//     "Sawai Madhopur",
//     "Sikar",
//     "Sirohi",
//     "Tonk",
//     "Udaipur",
// ];
// var Sikkim = ["East Sikkim", "North Sikkim", "South Sikkim", "West Sikkim"];
// var TamilNadu = [
//     "Ariyalur",
//     "Chennai",
//     "Coimbatore",
//     "Cuddalore",
//     "Dharmapuri",
//     "Dindigul",
//     "Erode",
//     "Kanchipuram",
//     "Kanyakumari",
//     "Karur",
//     "Krishnagiri",
//     "Madurai",
//     "Nagapattinam",
//     "Namakkal",
//     "Nilgiris",
//     "Perambalur",
//     "Pudukkottai",
//     "Ramanathapuram",
//     "Salem",
//     "Sivaganga",
//     "Thanjavur",
//     "Theni",
//     "Thoothukudi",
//     "Tiruchirappalli",
//     "Tirunelveli",
//     "Tiruppur",
//     "Tiruvallur",
//     "Tiruvannamalai",
//     "Tiruvarur",
//     "Vellore",
//     "Viluppuram",
//     "Virudhunagar",
// ];
// var Telangana = [
//     "Adilabad",
//     "Bhadradri Kothagudem",
//     "Hyderabad",
//     "Jagtial",
//     "Jangaon",
//     "Jayashankar",
//     "Jogulamba",
//     "Kamareddy",
//     "Karimnagar",
//     "Khammam",
//     "Komaram Bheem",
//     "Mahabubabad",
//     "Mahbubnagar",
//     "Mancherial",
//     "Medak",
//     "Medchal",
//     "Nagarkurnool",
//     "Nalgonda",
//     "Nirmal",
//     "Nizamabad",
//     "Peddapalli",
//     "Rajanna Sircilla",
//     "Ranga Reddy",
//     "Sangareddy",
//     "Siddipet",
//     "Suryapet",
//     "Vikarabad",
//     "Wanaparthy",
//     "Warangal Rural",
//     "Warangal Urban",
//     "Yadadri Bhuvanagiri",
// ];
// var Tripura = [
//     "Dhalai",
//     "Gomati",
//     "Khowai",
//     "North Tripura",
//     "Sepahijala",
//     "South Tripura",
//     "Unakoti",
//     "West Tripura",
// ];
// var UttarPradesh = [
//     "Agra",
//     "Aligarh",
//     "Allahabad",
//     "Ambedkar Nagar",
//     "Amethi",
//     "Amroha",
//     "Auraiya",
//     "Azamgarh",
//     "Baghpat",
//     "Bahraich",
//     "Ballia",
//     "Balrampur",
//     "Banda",
//     "Barabanki",
//     "Bareilly",
//     "Basti",
//     "Bhadohi",
//     "Bijnor",
//     "Budaun",
//     "Bulandshahr",
//     "Chandauli",
//     "Chitrakoot",
//     "Deoria",
//     "Etah",
//     "Etawah",
//     "Faizabad",
//     "Farrukhabad",
//     "Fatehpur",
//     "Firozabad",
//     "Gautam Buddha Nagar",
//     "Ghaziabad",
//     "Ghazipur",
//     "Gonda",
//     "Gorakhpur",
//     "Hamirpur",
//     "Hapur",
//     "Hardoi",
//     "Hathras",
//     "Jalaun",
//     "Jaunpur",
//     "Jhansi",
//     "Kannauj",
//     "Kanpur Dehat",
//     "Kanpur Nagar",
//     "Kasganj",
//     "Kaushambi",
//     "Kheri",
//     "Kushinagar",
//     "Lalitpur",
//     "Lucknow",
//     "Maharajganj",
//     "Mahoba",
//     "Mainpuri",
//     "Mathura",
//     "Mau",
//     "Meerut",
//     "Mirzapur",
//     "Moradabad",
//     "Muzaffarnagar",
//     "Pilibhit",
//     "Pratapgarh",
//     "Raebareli",
//     "Rampur",
//     "Saharanpur",
//     "Sambhal",
//     "Sant Kabir Nagar",
//     "Shahjahanpur",
//     "Shamli",
//     "Shravasti",
//     "Siddharthnagar",
//     "Sitapur",
//     "Sonbhadra",
//     "Sultanpur",
//     "Unnao",
//     "Varanasi",
// ];
// var Uttarakhand = [
//     "Almora",
//     "Bageshwar",
//     "Chamoli",
//     "Champawat",
//     "Dehradun",
//     "Haridwar",
//     "Nainital",
//     "Pauri",
//     "Pithoragarh",
//     "Rudraprayag",
//     "Tehri",
//     "Udham Singh Nagar",
//     "Uttarkashi",
// ];
// var WestBengal = [
//     "Alipurduar",
//     "Bankura",
//     "Birbhum",
//     "Cooch Behar",
//     "Dakshin Dinajpur",
//     "Darjeeling",
//     "Hooghly",
//     "Howrah",
//     "Jalpaiguri",
//     "Jhargram",
//     "Kalimpong",
//     "Kolkata",
//     "Malda",
//     "Murshidabad",
//     "Nadia",
//     "North 24 Parganas",
//     "Paschim Bardhaman",
//     "Paschim Medinipur",
//     "Purba Bardhaman",
//     "Purba Medinipur",
//     "Purulia",
//     "South 24 Parganas",
//     "Uttar Dinajpur",
// ];
// var AndamanNicobar = ["Nicobar", "North Middle Andaman", "South Andaman"];
// var Chandigarh = ["Chandigarh"];
// var DadraHaveli = ["Dadra Nagar Haveli"];
// var DamanDiu = ["Daman", "Diu"];
// var Delhi = [
//     "Central Delhi",
//     "East Delhi",
//     "New Delhi",
//     "North Delhi",
//     "North East Delhi",
//     "North West Delhi",
//     "Shahdara",
//     "South Delhi",
//     "South East Delhi",
//     "South West Delhi",
//     "West Delhi",
// ];
// var Lakshadweep = ["Lakshadweep"];
// var Puducherry = ["Karaikal", "Mahe", "Puducherry", "Yanam"];

// $("#id_State").change(function () {
//     var StateSelected = $(this).val();
//     console.log(StateSelected)
//     var optionsList;
//     var htmlString = "";

//     switch (StateSelected) {
//         case "Andhra Pradesh":
//             optionsList = AndraPradesh;
//             break;
//         case "Arunachal Pradesh":
//             optionsList = ArunachalPradesh;
//             break;
//         case "Assam":
//             optionsList = Assam;
//             break;
//         case "Bihar":
//             optionsList = Bihar;
//             break;
//         case "Chhattisgarh":
//             optionsList = Chhattisgarh;
//             break;
//         case "Goa":
//             optionsList = Goa;
//             break;
//         case "Gujarat":
//             optionsList = Gujarat;
//             break;
//         case "Haryana":
//             optionsList = Haryana;
//             break;
//         case "Himachal Pradesh":
//             optionsList = HimachalPradesh;
//             break;
//         case "Jammu and Kashmir":
//             optionsList = JammuKashmir;
//             break;
//         case "Jharkhand":
//             optionsList = Jharkhand;
//             break;
//         case "Karnataka":
//             optionsList = Karnataka;
//             break;
//         case "Kerala":
//             optionsList = Kerala;
//             break;
//         case "Lakshadweep":
//             optionsList = Lakshadweep;
//             break;
//         case "Madhya Pradesh":
//             optionsList = MadhyaPradesh;
//             break;
//         case "Maharashtra":
//             optionsList = Maharashtra;
//             break;
//         case "Manipur":
//             optionsList = Manipur;
//             break;
//         case "Meghalaya":
//             optionsList = Meghalaya;
//             break;
//         case "Mizoram":
//             optionsList = Mizoram;
//             break;
//         case "Nagaland":
//             optionsList = Nagaland;
//             break;
//         case "Odisha":
//             optionsList = Odisha;
//             break;
//         case "Punjab":
//             optionsList = Punjab;
//             break;
//         case "Puducherry":
//             optionsList = Puducherry;
//             break;
//         case "Rajasthan":
//             optionsList = Rajasthan;
//             break;
//         case "Sikkim":
//             optionsList = Sikkim;
//             break;
//         case "Tamil Nadu":
//             optionsList = TamilNadu;
//             break;
//         case "Telangana":
//             optionsList = Telangana;
//             break;
//         case "Tripura":
//             optionsList = Tripura;
//             break;
//         case "Uttar Pradesh":
//             optionsList = UttarPradesh;
//             break;
//         case "Uttarakhand":
//             optionsList = Uttarakhand;
//             break;
//         case "West Bengal":
//             optionsList = WestBengal;
//             break;
//         case "Andaman and Nicobar Islands":
//             optionsList = AndamanNicobar;
//             break;
//         case "Chandigarh":
//             optionsList = Chandigarh;
//             break;
//         case "Dadra and Nagar Haveli":
//             optionsList = DadraHaveli;
//             break;
//         case "Daman and Diu":
//             optionsList = DamanDiu;
//             break;
//         case "Delhi":
//             optionsList = Delhi;
//             break;
//         case "Lakshadeep":
//             optionsList = Lakshadeep;
//             break;
//         case "Pondicherry":
//             optionsList = Pondicherry;
//             break;
//     }

//     for (var i = 0; i < optionsList.length; i++) {
//         htmlString =
//             htmlString +
//             "<option value='" + optionsList[i] + "'>" + optionsList[i] + "</option>";
//     }
//     $("#id_District").html(htmlString);
// });

// // ---------------second time--------------
// $("#id_confirmState").change(function () {
//     var StateSelected = $(this).val();
//     var optionsList;
//     var htmlString = "";

//     switch (StateSelected) {
//         case "Andhra Pradesh":
//             optionsList = AndraPradesh;
//             break;
//         case "Arunachal Pradesh":
//             optionsList = ArunachalPradesh;
//             break;
//         case "Assam":
//             optionsList = Assam;
//             break;
//         case "Bihar":
//             optionsList = Bihar;
//             break;
//         case "Chhattisgarh":
//             optionsList = Chhattisgarh;
//             break;
//         case "Goa":
//             optionsList = Goa;
//             break;
//         case "Gujarat":
//             optionsList = Gujarat;
//             break;
//         case "Haryana":
//             optionsList = Haryana;
//             break;
//         case "Himachal Pradesh":
//             optionsList = HimachalPradesh;
//             break;
//         case "Jammu and Kashmir":
//             optionsList = JammuKashmir;
//             break;
//         case "Jharkhand":
//             optionsList = Jharkhand;
//             break;
//         case "Karnataka":
//             optionsList = Karnataka;
//             break;
//         case "Kerala":
//             optionsList = Kerala;
//             break;
//         case "Madya Pradesh":
//             optionsList = MadhyaPradesh;
//             break;
//         case "Maharashtra":
//             optionsList = Maharashtra;
//             break;
//         case "Manipur":
//             optionsList = Manipur;
//             break;
//         case "Meghalaya":
//             optionsList = Meghalaya;
//             break;
//         case "Mizoram":
//             optionsList = Mizoram;
//             break;
//         case "Nagaland":
//             optionsList = Nagaland;
//             break;
//         case "Odisha":
//             optionsList = Odisha;
//             break;
//         case "Punjab":
//             optionsList = Punjab;
//             break;
//         case "Rajasthan":
//             optionsList = Rajasthan;
//             break;
//         case "Sikkim":
//             optionsList = Sikkim;
//             break;
//         case "Tamil Nadu":
//             optionsList = TamilNadu;
//             break;
//         case "Telangana":
//             optionsList = Telangana;
//             break;
//         case "Tripura":
//             optionsList = Tripura;
//             break;
//         case "Uttaranchal":
//             optionsList = Uttaranchal;
//             break;
//         case "Uttar Pradesh":
//             optionsList = UttarPradesh;
//             break;
//         case "West Bengal":
//             optionsList = WestBengal;
//             break;
//         case "Andaman and Nicobar Islands":
//             optionsList = AndamanNicobar;
//             break;
//         case "Chandigarh":
//             optionsList = Chandigarh;
//             break;
//         case "Dadar and Nagar Haveli":
//             optionsList = DadraHaveli;
//             break;
//         case "Daman and Diu":
//             optionsList = DamanDiu;
//             break;
//         case "Delhi":
//             optionsList = Delhi;
//             break;
//         case "Lakshadeep":
//             optionsList = Lakshadeep;
//             break;
//         case "Pondicherry":
//             optionsList = Pondicherry;
//             break;
//     }

//     for (var i = 0; i < optionsList.length; i++) {
//         htmlString =
//             htmlString +
//             "<option value='" + optionsList[i] + "'>" + optionsList[i] + "</option>";
//     }
//     $("#id_confirmDistrict").html(htmlString);
// });




// --------------------state and district------------------

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
    let check = document.getElementById('check');
    document.getElementById("id_confirmAddressLine1").value = check.checked ? AddLine1 : null;
    document.getElementById("id_confirmAddressLine2").value = check.checked ? AddLine2 : null;
    document.getElementById("id_confirmAddressLine3").value = check.checked ? AddLine3 : null;
    document.getElementById("id_confirmPincode").value = check.checked ? pcode : null;
    document.getElementById("id_confirmVillage").value = check.checked ? village : null;
    document.getElementById("id_confirmState").value = check.checked ? id_State : null; {
        $.ajax({
            type: "GET",
            url: "/confirm_dist_data",
            data: {
                dist_data: id_District
            },
            success: function (data) {
                // $("#id_District").html(data);    
                // console.log(data.Dist_list)
                // console.log(data.Dist_id)
                // console.log(Dist_list)
                document.getElementById("id_confirmDistrict").innerHTML = check.checked ? "<option value='" + data.Dist_id + "'>" + data.Dist_list + "</option>" : null;
            }
        })
    }
}

// Attach documents

// Convert the file size to a readable format
const formatFileSize = function (bytes) {
    const sufixes = ["B", "kB", "MB", "GB", "TB"];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sufixes[i]}`;
};

// remove button function
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
        Input.value = null; //SO happy to write this statments!!!!!!
        // console.log("Input value:  " + Input.value);
        previewImage.style.display = "none";
        previewDefaultText.style.display = "block";
        Text.style.display = "none";
        document.getElementsByClassName("image-preview")[id - 1].style.border =
            "2px dotted lightgrey";
    });
}

// preview before upload function
function previewBeforeUpload(id) {
    const inputFile = document.getElementById(`inputFile${id}`);
    removeImage(id);

    inputFile.addEventListener("change", function (e) {
        const file = this.files[0];
        const Text = document.getElementById(`image-details${id}`);
        const previewImage = document.querySelector(`.image-preview__image${id}`);
        const previewDefaultText = document.querySelector(
            `.image-preview__default-text${id}`
        );
        const Input = document.getElementById(`inputFile${id}`);

        // console.log(Input.value);
        if (file && file.size <= 350000) {
            const reader = new FileReader();
            const Remove = document.querySelector(`.remove-img${id}`);
            // Remove.style.display = "inline-block";
            // Text.style.display = "block";
            // Text.innerText = `${file.name} \n ${formatFileSize(file.size)}`;
            // Text.style.fontSize = "13px";
            document.getElementsByClassName("image-preview")[id - 1].style.border =
                "none";
            // document.getElementsByClassName("image-preview")[
            //   id - 1
            // ].style.backgroundColor = "transparent";

            previewDefaultText.style.display = "none";
            previewImage.style.display = "block";

            reader.addEventListener("load", function () {
                previewImage.setAttribute("src", this.result);
            });

            reader.readAsDataURL(file);
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Image size must be less than 350KB!',
            });
        }
    });
}
/************general variables***********/
const previewContainer = document.getElementById("imagePreview");

/***********function call to client image********/
previewBeforeUpload(9);

/***********function call to member aadhar card********/
previewBeforeUpload(1);
previewBeforeUpload(2);

/***********function call to member voter card********/

previewBeforeUpload(3);
previewBeforeUpload(4);

/***********function call to co-insurer aadhaar card********/
previewBeforeUpload(5);
previewBeforeUpload(6);
id_Product

/***********function call to bank details********/

previewBeforeUpload(7);
previewBeforeUpload(8);



//--------Loan details fatch data from table start -------//
$("#id_Product").change(function () {
    var Product = $(this).val();
    console.log(Product);
    $.ajax({
        type: "GET",
        url: "/loanDetailsAmount",
        data: {
            Product_name: Product
        },
        success: function (data) {
            document.getElementById("id_LoanAmount").value = data.LoanAmount;
            document.getElementById("id_InterestRate").value = data.InterestRate;
            document.getElementById("id_RepayFrequency").value = data.RepayFrequency;
        }
    })
});

//--------Loan details fatch data from table end -------//




//--------Loan Form confermation code start -------//
function clicked() {
    if (confirm('Do you want to submit?')) {
        yourformelement.submit();
    } else {
        return false;
    }
}



//--------Loan Form confermation code end -------//

function blockSpecialChar(e) {
    var k;
    document.all ? k = e.keyCode : k = e.which;
    return ((k > 64 && k < 91) || (k > 96 && k < 123));
}


//--------Function for block element start -------//


//--------Function for block element end -------//








//--------Get fianl customer data after submitted  start-------//


// const aadharNumber = document.getElementById('id_Aadhaar').value;
// const userData = document.getElementById("user_data").textContent;
// document.getElementById("d1").innerHTML = aadharNumber;
// document.getElementById("d2").value = userData;
// document.getElementById("d3").value = userData;



//--------Get fianl customer data after submitted  end-------//