from urllib import request
from django.contrib.auth.models import *
from django import forms
from django.contrib.auth import password_validation , hashers
from django.contrib.auth.forms import *
from LOAN.models import *
# from LOAN.models import customerKYC
from django.db.models import Max


class newLoanForm(forms.ModelForm):
    class Meta:
        model = LoanDetails
        fields = [
            "loanName",
            "Product",
            "loanMode",
            "LoanAmount",
            "InterestRate",
            "Number_of_months",
            "RepayFrequency",
            "loanProcessingCharge",
            "loanProcessingFee"
        ]


class customerKYCform(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(customerKYCform, self).__init__(*args, **kwargs)
        self.fields['CenterId'] = forms.ModelChoiceField(
            queryset=center.objects.filter(agents_Name=request.user),label="Center Id"
        )
        self.fields['BranchName'] = forms.ModelChoiceField(
            queryset=userWithRole.objects.filter(userName=request.user),label="Branch Name"
        )  
        self.fields['ProductCategory'] = forms.ModelChoiceField(
            queryset=LoanDetails.objects.filter(activateStatus = True),label="Product Category"
        )
        self.fields['Product'] = forms.ModelChoiceField(
            queryset=LoanDetails.objects.filter(activateStatus = True),label="Product"
        )
        # self.fields["BranchName"] = forms.ChoiceField(  # choice filter in list form
        #     choices=[
        #         (
        #             o.id,
        #             o.branchName.branch_Name,
        #         )  
        #         for o in userWithRole.objects.filter(userName=request.user)
        #     ],
        #     label="Branc Name",
        #     error_messages={
        #         "required": "Please Enter Branch Name",
        #     },
        # )
        self.fields["OtherKYCIdtype"].required = False
        self.fields["OtherKYCId"].required = False
        self.fields["LastName"].required = False
        self.fields["Member_Relationship_Proof"].required = False

    class Meta:
        model = customerKYC
        fields = [
            "Aadhaar",
            "VoterCard",
            "OtherKYCIdtype",
            "OtherKYCId",
            "Custimage",
            "Member_Aadhar_Card_front",
            "Member_Aadhar_Card_back",
            "Member_Voter_Card_front",
            "Member_Voter_Card_back",
            "Co_Insurer_Aadhaar_front",
            "Co_Insurer_Aadhaar_back",
            "Member_Bank_Details",
            "Member_Relationship_Proof",
            "FirstName",
            "LastName",
            "Gender",
            "DateOfBirth",
            "Age",
            "MaritalStatus",
            "FSName",
            "FSType",
            "FSDateOfBirth",
            "FSAdhaar",
            "MothersName",
            "Caste",
            "Religion",
            "Qualification",
            "Occupation",
            "PhoneNumber",
            "PreferredLanguage",
            "AddressLine1",
            "AddressLine2",
            "AddressLine3",
            "Village",
            "District",
            "State",
            "Pincode",
            "confirmAddressLine1",
            "confirmAddressLine2",
            "confirmAddressLine3",
            "confirmPincode",
            "confirmVillage",
            "confirmState",
            "confirmDistrict",
            "HouseType",
            "LandInAcre",
            "NumberofAnimals",
            "PovertyLine",
            "BankName",
            "BankAccountNo",
            "ConfirmBankAccountNo",
            "BankIFSCCode",
            "ConfirmBankIFSCCode",
            "BranchName",
            "CenterId",
            "GroupName",
            "ProductCategory",
            "CategoryType",
            "Product",
            "PurposeId",
            "LoanAmount",
            "InterestRate",
            "RepayFrequency",
            "CoInsurerRelation",
            "CoInsurerName",
            "CoInsurerDOB",
            "CoInsurerAge",
            "KYCIDType",
            "KYCID",
            "CoOccupation",
            "RemarkComments",
        ]
        labels = {
            "Aadhaar": "Aadhar Number",
            "Application_No": "Application No.",
            "VoterCard": "Voter Card",
            "OtherKYCId": "Other KYC Id",
            "DateOfBirth": "Date Of Birth",
            "MaritalStatus": "Marital Status",
            "FSDateOfBirth": "FS Date Of Birth",
            "Custimage": "Customer Image",
            "Member_Aadhar_Card_front": "Front Side Upload",
            "Member_Aadhar_Card_back": "Back Side Upload",
            "Member_Voter_Card_front": "Front Side Upload",
            "Member_Voter_Card_back": "Back Side Upload",
            "Co_Insurer_Aadhaar_front": "Front Side Upload",
            "Co_Insurer_Aadhaar_back": "Back Side Upload",
            "Member_Bank_Details": "UPLOAD",
            "Member_Relationship_Proof": "UPLOAD",
            "FirstName": "First Name",
            "LastName": "Last Name",
            "FSAdhaar": "FS Adhaar",
            "FSName": "FS Name",
            "MothersName": "Mothers Name",
            "PreferredLanguage": "Preferred Language",
            "HouseType": "House Type",
            "LandInAcre": "Land In Acre",
            "NumberofAnimals": "Number of Animals",
            "PovertyLine": "Poverty Line",
            "AddressLine1": "Address Line1",
            "AddressLine2": "Address Line2",
            "AddressLine3": "Address Line3",
            "Pincode": "Pin Code",
            "confirmPincode": "Confirm Pin Code",
            "confirmAddressLine1": "Confirm Address Line1",
            "confirmAddressLine2": "Confirm Address Line2",
            "confirmAddressLine3": "Confirm Address Line3",
            "District": "District",
            "confirmState": "Confirm State",
            "BankName": "Bank Name",
            "BankAccountNo": "Bank Account Number",
            "ConfirmBankAccountNo": "Confirm Bank Account Number",
            "BankIFSCCode": "Bank IFSC Code",
            "ConfirmBankIFSCCode": "Confirm Bank IFSC Code",
            "GroupName": "Group Name",
            "ProductCategory": "Product Category",
            "CategoryType": "Category Type",
            "PurposeId": "Purpose Id",
            "LoanAmount": "Loan Amount",
            "InterestRate": "Interest Rate",
            "RepayFrequency": "Repay Frequency",
            "CoInsurerRelation": "Co Insurer Relation",
            "CoInsurerName": "Co Insurer Name",
            "CoInsurerDOB": "Co Insurer DOB",
            "CoInsurerAge": "Co Insurer Age",
            "KYCID": "KYC ID",
            "CoOccupation": "Co Occupation",
            "RemarkComments": "Remark Comments",
            "PhoneNumber": "Phone Number",
        }
        help_text = {
            "Aadhaar": "Enter Your Aadhar Number",
            "VoterCard": "Enter Your VoterID Number",
        }
        error_messages = {
            "Aadhaar": {
                "required": "Please Enter Your Aadhar Number",
            },
            "VoterCard": {
                "required": "Please Enter Your Voter Card Number",
            },
            "Custimage": {
                "required": "Please Enter Customer Image",
            },
            "FirstName": {
                "required": "Please Enter Your First Name",
            },
            "Member_Aadhar_Card_front": {
                "required": "Please Enter Your Aadhar Card front Side Image",
            },
            "Member_Aadhar_Card_back": {
                "required": "Please Enter Your Aadhar Card back Side Image",
            },
            "Member_Voter_Card_front": {
                "required": "Please Enter Your Voter Card front Side Image",
            },
            "Member_Voter_Card_back": {
                "required": "Please Enter Your Voter Card back Side Image",
            },
            "Co_Insurer_Aadhaar_front": {
                "required": "Please Enter Your Co-Insurer Aadhaar front Side Image",
            },
            "Co_Insurer_Aadhaar_back": {
                "required": "Please Enter Your Co-Insurer Aadhaar back Side Image",
            },
            "Member_Bank_Details": {
                "required": "Please Enter Your Bank Details",
            },
            "Member_Relationship_Proof": {
                "required": "Please Enter Your Relationship Proof",
            },
            "LastName": {
                "required": "Please Enter Your Last Name",
            },
            "Gender": {
                "required": "Please Enter Your Gender",
            },
            "DateOfBirth": {
                "required": "Please Enter Your Date Of Birth",
            },
            "Age": {
                "required": "Please Enter Your Age",
            },
            "MaritalStatus": {
                "required": "Please Enter Your Marital Status",
            },
            "FSName": {
                "required": "Please Enter Your FS Name",
            },
            "Occupation": {
                "required": "Please Enter Your Occupation",
            },
            "FSType": {
                "required": "Please Enter Your FS Type",
            },
            "FSDateOfBirth": {
                "required": "Please Enter Your  FS Date Of Birth",
            },
            "FSAdhaar": {
                "required": "Please Enter Your FS Adhaar Card Number",
            },
            "MothersName": {
                "required": "Please Enter Your Mothers Name",
            },
            "Caste": {
                "required": "Please Enter Your Caste",
            },
            "Religion": {
                "required": "Please Enter Your Religion",
            },
            "Qualification": {
                "required": "Please Enter Your Qualification",
            },
            "PhoneNumber": {
                "required": "Please Enter Your Phone Number",
            },
            "AddressLine1": {
                "required": "Please Enter Your Address Line 1",
            },
            "AddressLine2": {
                "required": "Please Enter Your Address Line 2",
            },
            "AddressLine3": {
                "required": "Please Enter Your Address Line 3",
            },
            "PreferredLanguage": {
                "required": "Please Enter Your Preferred Language",
            },
            "Pincode": {
                "required": "Please Enter Your Pincode",
            },
            "Village": {
                "required": "Please Enter Your Village Name",
            },
            "State": {
                "required": "Please Enter Your State",
            },
            "District": {
                "required": "Please Enter Your District",
            },
            "confirmAddressLine1": {
                "required": "Please Enter Your Address Line 1",
            },
            "confirmAddressLine2": {
                "required": "Please Enter Your Address Line 2",
            },
            "confirmAddressLine3": {
                "required": "Please Enter Your Address Line 3",
            },
            "confirmVillage": {
                "required": "Please Enter Your Village Name",
            },
            "confirmPincode": {
                "required": "Please Enter Your Confirm Pincode",
            },
            "confirmState": {
                "required": "Please Enter Your State Name",
            },
            "confirmDistrict": {
                "required": "Please Enter Your Confirm District",
            },
            "HouseType": {
                "required": "Please Enter Your House Type",
            },
            "LandInAcre": {
                "required": "Please Enter Your Land In Acre",
            },
            "NumberofAnimals": {
                "required": "Please Enter Your Number of Animals",
            },
            "PovertyLine": {
                "required": "Please Enter Your Poverty Line",
            }, 
            "BankName": {
                "required": "Please Enter Your Bank Name",
            },
             "BranchName": {
                "required": "Please Enter Your Branch Name",
            },
            "BankAccountNo": {
                "required": "Please Enter Your Bank Account Number",
            },
            "ConfirmBankAccountNo": {
                "required": "Please Enter Your Confirm Bank Account Number",
            },
            "BankIFSCCode": {
                "required": "Please Enter Your Bank IFSC Code",
            },
            "ConfirmBankIFSCCode": {
                "required": "Please Enter Your Confirm Bank IFSC Code",
            },
            "GroupName": {
                "required": "Please Enter Group Name",
            },
            "CategoryType": {
                "required": "Please Enter Your Category Type",
            },
            "PurposeId": {
                "required": "Please Enter Your Purpose Id",
            },
            "LoanAmount": {
                "required": "Please Enter Your Loan Amount",
            },
            "InterestRate": {
                "required": "Please Enter Your Interest Rate",
            },
            "RepayFrequency": {
                "required": "Please Enter Your Repay Frequency",
            },
            "CoInsurerRelation": {
                "required": "Please Enter Your Co-Insurer Relation",
            },
            "CoInsurerName": {
                "required": "Please Enter Your Co-Insurer Name",
            },
            "CoInsurerDOB": {
                "required": "Please Enter Your Co-Insurer DOB",
            },
            "CoInsurerAge": {
                "required": "Please Enter Your Co-Insurer Age",
            },
            "KYCIDType": {
                "required": "Please Enter Your KYC ID Type",
            },
            "KYCID": {
                "required": "Please Enter Your KYC ID",
            },
            "CoOccupation": {
                "required": "Please Enter Your Co-Occupation",
            },
            "RemarkComments": {
                "required": "Please Enter Your Remark Comments",
            },
        }
        widgets = {
            "FirstName": forms.TextInput(
                attrs={"onkeypress": "return blockSpecialChar(event)"}
            ),
            "LastName": forms.TextInput(
                attrs={"onkeypress": "return blockSpecialChar(event)"}
            ),
            "FSName": forms.TextInput(
                attrs={"onkeypress": "return blockSpecialChar(event)"}
            ),
            "MothersName": forms.TextInput(
                attrs={"onkeypress": "return blockSpecialChar(event)"}
            ),
            "Occupation": forms.TextInput(
                attrs={"onkeypress": "return blockSpecialChar(event)"}
            ),
            "CoInsurerRelation": forms.TextInput(
                attrs={"onkeypress": "return blockSpecialChar(event)"}
            ),
            "CoInsurerName": forms.TextInput(
                attrs={"onkeypress": "return blockSpecialChar(event)"}
            ),
            "Custimage": forms.ClearableFileInput(
                attrs={"type": "file", "id": "image-preview__image9", "class": "image-preview__image10"}
            ),
            "Member_Aadhar_Card_front": forms.ClearableFileInput(
                attrs={"type": "file", "id": "image-preview__image1", "class": "custom-file-input"}
            ),
            "Member_Aadhar_Card_back": forms.ClearableFileInput(
                attrs={"type": "file", "id": "image-preview__image2", "class": "custom-file-input"}
            ),
            "Member_Voter_Card_front": forms.ClearableFileInput(
                attrs={
                    "type": "file",
                    "id": "image-preview__image3",
                    "name": "voter-card-frontSide",
                }
            ),
            "Member_Voter_Card_back": forms.ClearableFileInput(
                attrs={
                    "type": "file",
                    "id": "image-preview__image4",
                    "name": "voter-card-backSide",
                }
            ),
            "Co_Insurer_Aadhaar_front": forms.ClearableFileInput(
                attrs={"type": "file", "id": "image-preview__image5", "class": "custom-file-input"}
            ),
            "Co_Insurer_Aadhaar_back": forms.ClearableFileInput(
                attrs={"type": "file", "id": "image-preview__image6", "class": "custom-file-input"}
            ),
            "Member_Bank_Details": forms.ClearableFileInput(
                attrs={"type": "file", "id": "image-preview__image7", "class": "custom-file-input"}
            ),
            "Member_Relationship_Proof": forms.ClearableFileInput(
                attrs={"type": "file", "id": "image-preview__image8", "class": "custom-file-input"}
            ),
            "DateOfBirth": forms.DateInput(
                attrs={
                    "type": "date",
                    "id": "txtDOB",
                    "name": "dob",
                    "onchange": "fnCalculateAge();",
                }
            ),
            "Age": forms.NumberInput(
                attrs={"id": "age", "readonly": "readonly", "value": ""}
            ),
            "FSDateOfBirth": forms.DateInput(
                attrs={
                    "type": "date",
                    "id": "fsDOB",
                    "name": "fsDOB",
                    "onchange": "fnCalculateAge4();",
                }
            ),
            "CoInsurerDOB": forms.DateInput(
                attrs={
                    "type": "date",
                    "id": "coInsurerdob",
                    "name": "coInsurerdob",
                    "onchange": "fnCalculateAge2();",
                }
            ),
            "CoInsurerAge": forms.NumberInput(
                attrs={"id": "co-Insurerage", "readonly": "readonly", "value": ""}
            ),
            "NomineeDateOfBirth": forms.DateInput(
                attrs={
                    "type": "date",
                    "id": "NomineeDob",
                    "name": "NomineeDob",
                    "onchange": "fnCalculateAge3();",
                }
            ),
            "NomineeAge": forms.NumberInput(
                attrs={"id": "NomineeAge", "readonly": "readonly", "value": ""}
            ),
            "District": forms.Select(attrs={"id": "id_District"}),
            "confirmDistrict": forms.Select(attrs={"id": "id_confirmDistrict"}),
            "ConfirmBankAccountNo": forms.PasswordInput(),
            "ConfirmBankIFSCCode": forms.PasswordInput(),
        }

    def clean(self):
        super(customerKYCform, self).clean()
        Account = self.cleaned_data.get("BankAccountNo")
        confirmAccount = self.cleaned_data.get("ConfirmBankAccountNo")
        BankIFSCCode = self.cleaned_data.get("BankIFSCCode")
        ConfirmBankIFSCCode = self.cleaned_data.get("ConfirmBankIFSCCode")
        groupName = self.cleaned_data.get("GroupName")
        centerId = self.cleaned_data.get("CenterId")
        group = len(
            customerKYC.objects.filter(GroupName=groupName, CenterId__center_Id=centerId)
        )
        Pincode = str(self.cleaned_data.get("Pincode"))
        confirmPincode = str(self.cleaned_data.get("confirmPincode"))
        PhoneNumber = str(self.cleaned_data.get("PhoneNumber"))

        if group > 4:
            raise forms.ValidationError(
                "You can not create member in this group try other group"
            )

        if Account != confirmAccount:
            raise forms.ValidationError(
                "Bank Account Number and Confirm Bank Account Number Must be Same"
            )
        elif BankIFSCCode != ConfirmBankIFSCCode:
            raise forms.ValidationError(
                "Bank IFCS Code and Confirm IFCS Code Must be Same"
            )
        elif 6 < len(Pincode) < 6:
            raise forms.ValidationError("Pin Code Must have 6 digits")
        elif 6 < len(confirmPincode) < 6:
            raise forms.ValidationError("confirm Pincode Must have 6 digits")
        elif 10 < len(PhoneNumber) < 10:
            raise forms.ValidationError("Moble Number Must have 10 digits")
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Old Password:"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "current-password",
                "autofocus": True,
            }
        ),
    )
    new_password1 = forms.CharField(
        label=("New Password:"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("Confirm New Password:"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        ),
    )
    user = forms.CharField(
        label=(" User Id:"),
        strip=False,
        widget=forms.TextInput(
            attrs={"class": "form-control"}
        ),
    )
    


class MypasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "autocomplete": "email"}
        )
    )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=("New Password:"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("Confirm New Password:"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )


class haed_officeform(forms.Form):
    haed_office_name = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    created_by = forms.CharField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    Remember_me = forms.CharField(widget=forms.CheckboxInput)


class Regionform(forms.ModelForm):
    class Meta:
        model = region
        fields = ["haed_office_name", "circle_name", "zone", "region", "created_by"]
        widgets = {
            "haed_office_name": forms.Select(attrs={"class": "form-control"}),
            "circle_name": forms.Select(attrs={"class": "form-control"}),
            "zone": forms.Select(attrs={"class": "form-control"}),
            "region": forms.TextInput(attrs={"class": "form-control"}),
            "created_by": forms.TextInput(attrs={"class": "form-control"}),
        }


class circleform(forms.ModelForm):
    class Meta:
        model = circle
        fields = ["haed_office_name", "circle_name", "created_by"]
        widgets = {
            "haed_office_name": forms.Select(attrs={"class": "form-control"}),
            "circle_name": forms.TextInput(attrs={"class": "form-control"}),
            "created_by": forms.TextInput(attrs={"class": "form-control"}),
        }


class zoneform(forms.ModelForm):
    class Meta:
        model = zone
        fields = ["haed_office_name", "circle_name", "zone", "created_by"]
        widgets = {
            "haed_office_name": forms.Select(attrs={"class": "form-control"}),
            "circle_name": forms.Select(attrs={"class": "form-control"}),
            "zone": forms.TextInput(attrs={"class": "form-control"}),
            "created_by": forms.TextInput(attrs={"class": "form-control"}),
        }

class userProfile(forms.ModelForm):
    class Meta:
        model = userProfileRole
        fields = ["profileRoleName",]
        labels = {
            "profileRoleName" : "Profile Role Name"
        }


class userForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(userForm, self).__init__(*args, **kwargs)
        self.fields["branchName"] = forms.ChoiceField(
            choices=[(o.id, str(o.branch_Name)) for o in branch.objects.all().order_by("branch_Name")]
        )
        self.fields["userName"] = forms.ChoiceField(
            choices=[(o.id, str(f"{o.first_name.title()} {o.username}")) for o in User.objects.all()]
            ,label="User ID" ,widget=forms.Select(attrs={'onchange': 'fun("id_user_Id");'})
        )
        self.fields['group'] = forms.ModelChoiceField(
            queryset=Group.objects.all().exclude(name = 'admin'),label="Group Name" 
        )

    class Meta:
        model = userWithRole
        fields = ["userName", "user_actual_Name", "branchName","user_role"]
        labels = {
            "user_role" : "User Role",
            "user_actual_Name" : "User Name"
        }
        

class branchform(forms.ModelForm):
    class Meta:
        model = branch
        fields = [
            "haed_office_name",
            "circle_name",
            "zone",
            "region",
            "branch_Name",
            "created_by",
        ]
        widgets = {
            "haed_office_name": forms.Select(attrs={"class": "form-control"}),
            "circle_name": forms.Select(attrs={"class": "form-control"}),
            "zone": forms.Select(attrs={"class": "form-control"}),
            "region": forms.TextInput(attrs={"class": "form-control"}),
            "branch_Name": forms.TextInput(attrs={"class": "form-control"}),
            "created_by": forms.TextInput(attrs={"class": "form-control"}),
        }


class centerform(forms.ModelForm):
    class Meta:
        model = center
        fields = [
            "haed_office_name",
            "circle_name",
            "zone",
            "region",
            "branch_Name",
            "center_name",
            "created_by",
        ]
        widgets = {
            "haed_office_name": forms.Select(attrs={"class": "form-control"}),
            "circle_name": forms.Select(attrs={"class": "form-control"}),
            "zone": forms.Select(attrs={"class": "form-control"}),
            "region": forms.TextInput(attrs={"class": "form-control"}),
            "branch_Name": forms.TextInput(attrs={"class": "form-control"}),
            "center_name": forms.TextInput(attrs={"class": "form-control"}),
            "created_by": forms.TextInput(attrs={"class": "form-control"}),
        }


class centerIdform(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(centerIdform, self).__init__(*args, **kwargs)
        
        # self.fields['agents_Name'] = forms.ModelChoiceField(
        #     queryset=User.objects.filter(is_staff = False),label="Agent ID"
        # )
        managerBranch = userWithRole.objects.get(userName =request.user)
        try:
            groups = userWithRole.objects.get(userName =request.user)
            if groups.group.name == "Branch Manager":
                self.fields['branch_Name'] = forms.ChoiceField(
                choices=[(o.branchName.id, str(f"{o.branchName}")) for o in userWithRole.objects.filter(userName =request.user)]
                ,label="Branch Name"
                )
                self.fields["agents_Name"] = forms.ChoiceField(
                choices=[(o.userName.id, str(f"{o.userName.first_name.title()} {o.userName.username}")) for o in userWithRole.objects.filter(branchName__id = managerBranch.branchName.id).exclude(user_role__id = 2)]
                ,label="Agent ID" 
            )
        except userWithRole.DoesNotExist:
            self.fields["agents_Name"] = forms.ChoiceField(
                choices=[(o.id, str(f"{o.first_name.title()} {o.username}")) for o in User.objects.filter(is_staff = False)]
                ,label="Agent ID" 
            )
    class Meta:
        model = center
        fields = [
            "branch_Name",
            "center_name",
            "agents_Name",
            "center_meeting_time",
            "center_meeting_day",
            "center_leader"
        ]
        labels = {
            "center_meeting_time": "Center Meeting Time",
            "center_name": "Center Name",
            "branch_Name": "Branch Name",
            "center_meeting_day":"Center Meeting Date",
            "center_leader":"Center Leader Name"
        }
        widgets = {
            "center_meeting_day": forms.DateInput(
                attrs={"type": "date"}
            ),
            "center_meeting_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
        }
class calculatorForm(forms.ModelForm):
    class Meta:
        model = calculator
        fields = [
            "calculation_type",
            "loanMode",
            "rateOfIntrest",
            "loan_amount",
            "terms",
        ]
        widgets = {
            "calculation_type": forms.Select(attrs={"class": "form-control"}),
            "loanMode": forms.Select(attrs={"class": "form-control"}),
        }

class customerRegistraionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            "username" : forms.TextInput(
                attrs={"readonly": "readonly" }
            ), 
         }
        labels = {
            "username": "User ID",
        }
