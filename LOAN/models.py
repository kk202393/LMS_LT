from email.policy import default
from django.db import models
from django.contrib.auth.models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Max
from django.utils.timezone import datetime
from datetime import date
import uuid

# Create your models here.
class haed_office(models.Model):
    haed_office_name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.haed_office_name)

    class Meta:
        verbose_name_plural = "1. head_office"


class circle(models.Model):
    haed_office_name = models.ForeignKey(
        haed_office, on_delete=models.CASCADE, null=True
    )
    circle_name = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "2. circle"

    def __str__(self):
        return str(self.circle_name)


class zone(models.Model):
    haed_office_name = models.ForeignKey(
        haed_office, on_delete=models.CASCADE, null=True
    )
    circle_name = models.ForeignKey(circle, on_delete=models.CASCADE, null=True)
    zone = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "3. Zone"

    def __str__(self):
        return str(self.zone)


class region(models.Model):
    haed_office_name = models.ForeignKey(
        haed_office, on_delete=models.CASCADE, null=True
    )
    circle_name = models.ForeignKey(circle, on_delete=models.CASCADE, null=True)
    zone = models.ForeignKey(zone, on_delete=models.CASCADE, null=True)
    region = models.CharField(max_length=100, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "4. region"

    def __str__(self):
        return str(self.region)


class branch(models.Model):
    haed_office_name = models.ForeignKey(haed_office, on_delete=models.CASCADE)
    circle_name = models.ForeignKey(circle, on_delete=models.CASCADE, null=True)
    zone = models.ForeignKey(zone, on_delete=models.CASCADE)
    region = models.ForeignKey(region, on_delete=models.CASCADE)
    branch_Name = models.CharField(max_length=100, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "5. branch"

    def __str__(self):
        return str(self.branch_Name)


class center(models.Model):
    haed_office_name = models.ForeignKey(
        haed_office, on_delete=models.CASCADE, null=True
    )
    circle_name = models.ForeignKey(circle, on_delete=models.CASCADE, null=True)
    zone = models.ForeignKey(zone, on_delete=models.CASCADE)
    region = models.ForeignKey(region, on_delete=models.CASCADE)
    branch_Name = models.ForeignKey(branch, on_delete=models.CASCADE, null=True)
    center_name = models.CharField(max_length=100)
    center_Id = models.CharField(max_length=100)
    agents_Name = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    center_leader = models.CharField(max_length=100, null=True)
    center_meeting_time = models.TimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    center_meeting_day = models.DateField(null=True)
    Charfield10 = models.CharField(null=True, max_length=50)
    Charfield02 = models.CharField(null=True, max_length=50)
    Charfield03 = models.CharField(null=True, max_length=50)
    Charfield04 = models.CharField(null=True, max_length=50)
    Charfield05 = models.CharField(null=True, max_length=50)
    Charfield06 = models.CharField(null=True, max_length=50)
    Charfield07 = models.CharField(null=True, max_length=50)
    Charfield08 = models.CharField(null=True, max_length=50)
    Charfield09 = models.CharField(null=True, max_length=50)

    class Meta:
        verbose_name_plural = "6. center"

    def __str__(self):
        return str(f"{self.center_Id}-{self.center_name.title()}")

    def save(self, *args, **kwargs):
        if self.center_Id:
            pass
        else:
            maxCenterID =  center.objects.aggregate(max=Max("id"))["max"] + 1
            self.center_Id = f"10{self.branch_Name.id}0{maxCenterID}"
        super().save(*args, **kwargs)

class userProfileRole(models.Model):
    profileRoleName = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    Charfield10 = models.CharField(null=True, max_length=50)
    Charfield20 = models.CharField(null=True, max_length=50)
    Charfield30 = models.CharField(null=True, max_length=50)
    Charfield40 = models.CharField(null=True, max_length=50)
    Charfield50 = models.CharField(null=True, max_length=50)
    Charfield60 = models.CharField(null=True, max_length=50)
    Charfield70 = models.CharField(null=True, max_length=50)
    Charfield80 = models.CharField(null=True, max_length=50)
    Charfield90 = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.profileRoleName
    
    def save(self, *args, **kwargs):
        if self.created_date is None:
            self.created_date = date.today()
        self.updated_date = date.today()
        super().save(*args, **kwargs)


class userWithRole(models.Model):
    user_role = models.ForeignKey(userProfileRole, on_delete=models.PROTECT)
    group = models.ForeignKey(Group, on_delete=models.PROTECT) 
    user_actual_Name = models.CharField(null=True, max_length=50)
    branchName = models.ForeignKey(branch, on_delete=models.PROTECT) 
    userName = models.ForeignKey(User, on_delete=models.PROTECT) 
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    Charfield10 = models.CharField(null=True, max_length=50)
    Charfield20 = models.CharField(null=True, max_length=50)
    Charfield30 = models.CharField(null=True, max_length=50)
    Charfield40 = models.CharField(null=True, max_length=50)
    Charfield50 = models.CharField(null=True, max_length=50)
    Charfield60 = models.CharField(null=True, max_length=50)
    Charfield70 = models.CharField(null=True, max_length=50)
    Charfield80 = models.CharField(null=True, max_length=50)
    Charfield90 = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.branchName.branch_Name


class Agent(models.Model):
    user_Id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    agents_Name = models.CharField(null=True, max_length=50)
    branch_Name = models.ForeignKey(branch, null=True, on_delete=models.CASCADE)
    Charfield10 = models.CharField(null=True, max_length=50)
    Charfield20 = models.CharField(null=True, max_length=50)
    Charfield30 = models.CharField(null=True, max_length=50)
    Charfield40 = models.CharField(null=True, max_length=50)
    Charfield50 = models.CharField(null=True, max_length=50)
    Charfield60 = models.CharField(null=True, max_length=50)
    Charfield70 = models.CharField(null=True, max_length=50)
    Charfield80 = models.CharField(null=True, max_length=50)
    Charfield90 = models.CharField(null=True, max_length=50)

    def __str__(self):
        return str(self.branch_Name)

class dropDownList(models.Model):
    hLookupId = models.IntegerField()
    hLookupName = models.CharField(max_length=100)
    hLookupValue = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.hLookupValue)


# drop down list of table start


class OTHERKYCTYPE(models.Model):
    OTHERKYCTYPE_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.OTHERKYCTYPE_value)


class GENDER(models.Model):
    GENDER_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.GENDER_value)


class MaritalStatus(models.Model):
    MaritalStatus_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.MaritalStatus_value)


class FSType(models.Model):
    FSType_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.FSType_value)


class CAST(models.Model):
    CAST_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.CAST_value)


class Religion(models.Model):
    Religion_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.Religion_value)


class Qualification(models.Model):
    Qualification_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.Qualification_value)


class PreferredLanguage(models.Model):
    PreferredLanguage_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.PreferredLanguage_value)


class HouseType(models.Model):
    HouseType_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.HouseType_value)


class PovertyLine(models.Model):
    PovertyLine_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.PovertyLine_value)


class PurposeId(models.Model):
    PurposeId_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.PurposeId_value)


class categoryType(models.Model):
    categoryType_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.categoryType_value)


class GroupName(models.Model):
    GroupName_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.GroupName_value)


class BankName(models.Model):
    BankName_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.BankName_value)


class Disbursement_Mode(models.Model):
    Disbursement_Mode_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.Disbursement_Mode_value)


class form_STATUS(models.Model):
    form_STATUS_value = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.form_STATUS_value)


# drop down list of table end


class Loan_mode_data(models.Model):
    loan_name = models.CharField(max_length=100)
    loan_days = models.IntegerField()
    loan_name_value = models.IntegerField()

    def __str__(self):
        return self.loan_name


class LoanDetails(models.Model):
    loanName = models.CharField(null=True, max_length=50)
    Product = models.CharField(null=True, max_length=50)
    loanMode = models.ForeignKey(Loan_mode_data, on_delete=models.CASCADE, null=True)
    LoanAmount = models.IntegerField()
    InterestRate = models.FloatField()
    Number_of_months = models.IntegerField(null=True)
    RepayFrequency = models.IntegerField(blank=True)
    loanProcessingCharge = models.FloatField(null=True)
    loanProcessingFee = models.FloatField(null=True)
    created_by = models.CharField(max_length=100,null=True)
    updated_date = models.DateTimeField(auto_now_add=True,null=True)
    updated_by = models.CharField(max_length=100,null=True)
    activateStatus = models.BooleanField(default=True)
    intfield4 = models.IntegerField(null=True)
    intfield5 = models.IntegerField(null=True)
    DateField1 = models.DateTimeField(null=True)
    DateField2 = models.DateTimeField(null=True) 
    DateField3 = models.DateTimeField(null=True)
    DateField4 = models.DateTimeField(null=True)
    DateField5 = models.DateTimeField(null=True)
    Charfield1 = models.CharField(null=True, max_length=50)
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)
    Charfield6 = models.CharField(null=True, max_length=50)
    Charfield7 = models.CharField(null=True, max_length=50)
    Charfield8 = models.CharField(null=True, max_length=50)
    Charfield9 = models.CharField(null=True, max_length=50)
    Charfield10 = models.CharField(null=True, max_length=50)

    def __str__(self):
        return str(f"{self.loanName}  {self.Product}").title()

    # def save(self, *args, **kwargs):
    #     self.RepayFrequency = int(self.loanMode.loan_name_value) * int(self.Number_of_months)
    #     super().save(*args, **kwargs)


class state(models.Model):
    state_Name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.state_Name)


class Dist(models.Model):
    State_id = models.ForeignKey(state, on_delete=models.CASCADE)
    Dist_Name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.Dist_Name)


class Loan_Application_Details(models.Model):
    loanId = models.BigIntegerField(unique=True)
    customerId = models.BigIntegerField()
    Application_No = models.BigIntegerField()
    Aadhaar = models.BigIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.created_date is None:
            self.created_date = date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.loanId)


class DisbursementMode(models.Model):
    DisbursementModeName = models.CharField(null=True, max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return str(self.DisbursementModeName)


class customerKYC(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # Application_No = models.IntegerField(unique=True,default=None)
    status = models.ForeignKey(
        form_STATUS,
        default=40,
        related_name="customerKYC_status",
        on_delete=models.PROTECT,
    )
    loandata = models.ForeignKey(
        Loan_Application_Details, unique=True, on_delete=models.CASCADE
    )
    Aadhaar = models.BigIntegerField()
    VoterCard = models.CharField(max_length=100)
    OtherKYCIdtype = models.ForeignKey(
        OTHERKYCTYPE, related_name="OtherKYCIdtype", null=True, on_delete=models.PROTECT
    )
    OtherKYCId = models.CharField(max_length=100, null=True)
    Custimage = models.ImageField(upload_to="img")
    Member_Aadhar_Card_front = models.ImageField(upload_to="img")
    Member_Aadhar_Card_back = models.ImageField(upload_to="img")
    Member_Voter_Card_front = models.ImageField(upload_to="img")
    Member_Voter_Card_back = models.ImageField(upload_to="img")
    Co_Insurer_Aadhaar_front = models.ImageField(upload_to="img")
    Co_Insurer_Aadhaar_back = models.ImageField(upload_to="img")
    Member_Bank_Details = models.ImageField(upload_to="img")
    Member_Relationship_Proof = models.ImageField(upload_to="img", null=True)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100, null=True)
    Gender = models.ForeignKey(GENDER, on_delete=models.PROTECT)
    DateOfBirth = models.DateField()
    Age = models.IntegerField()
    MaritalStatus = models.ForeignKey(MaritalStatus, on_delete=models.PROTECT)
    FSName = models.CharField(max_length=100)
    FSType = models.ForeignKey(FSType, on_delete=models.PROTECT)
    FSDateOfBirth = models.DateField()
    FSAdhaar = models.BigIntegerField()
    MothersName = models.CharField(max_length=100)
    Caste = models.ForeignKey(CAST, on_delete=models.PROTECT)
    Religion = models.ForeignKey(Religion, on_delete=models.PROTECT)
    Qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT)
    Occupation = models.CharField(max_length=100)
    PhoneNumber = models.BigIntegerField()
    AddressLine1 = models.CharField(max_length=100)
    AddressLine2 = models.CharField(max_length=100)
    AddressLine3 = models.CharField(max_length=100)
    PreferredLanguage = models.ForeignKey(PreferredLanguage, on_delete=models.PROTECT)
    Pincode = models.PositiveIntegerField()
    Village = models.CharField(max_length=100)
    State = models.ForeignKey(state, related_name="state", on_delete=models.PROTECT)
    District = models.CharField(max_length=100)
    confirmAddressLine1 = models.CharField(max_length=100)
    confirmAddressLine2 = models.CharField(max_length=100)
    confirmAddressLine3 = models.CharField(max_length=100)
    confirmPincode = models.IntegerField()
    confirmVillage = models.CharField(max_length=100)
    confirmState = models.ForeignKey(
        state, related_name="confirm_State", on_delete=models.PROTECT
    )
    confirmDistrict = models.CharField(max_length=100)
    # FinancialDetails for customer
    HouseType = models.ForeignKey(HouseType, on_delete=models.PROTECT)
    LandInAcre = models.PositiveIntegerField()
    NumberofAnimals = models.PositiveIntegerField()
    PovertyLine = models.ForeignKey(PovertyLine, on_delete=models.PROTECT)
    BankName = models.ForeignKey(BankName, on_delete=models.PROTECT)
    BankAccountNo = models.BigIntegerField()
    ConfirmBankAccountNo = models.BigIntegerField()
    BankIFSCCode = models.CharField(max_length=100)
    ConfirmBankIFSCCode = models.CharField(max_length=100)
    # LoanDetails for customerKYC
    BranchName = models.ForeignKey(
        userWithRole, related_name="BranchName", on_delete=models.PROTECT
    )
    CenterId = models.ForeignKey(center, on_delete=models.PROTECT)
    ProductCategory = models.ForeignKey(
        LoanDetails, related_name="ProductCategory", on_delete=models.PROTECT
    )
    CategoryType = models.ForeignKey(categoryType, on_delete=models.PROTECT)
    Product = models.ForeignKey(LoanDetails, on_delete=models.PROTECT)
    PurposeId = models.ForeignKey(PurposeId, on_delete=models.PROTECT)
    LoanAmount = models.PositiveIntegerField()
    InterestRate = models.FloatField()
    RepayFrequency = models.FloatField()
    GroupName = models.ForeignKey(GroupName, on_delete=models.PROTECT)
    # CoInsurerDetails for cutomerKYC
    CoInsurerRelation = models.CharField(max_length=100)
    CoInsurerName = models.CharField(max_length=100)
    CoInsurerDOB = models.DateField()
    CoInsurerAge = models.PositiveIntegerField()
    KYCIDType = models.ForeignKey(
        OTHERKYCTYPE, related_name="KYCIDType", on_delete=models.PROTECT
    )
    KYCID = models.CharField(max_length=100)
    CoOccupation = models.CharField(max_length=100)
    RemarkComments = models.CharField(max_length=500)
    # NomineeDetails for customerKYC
    Timestamp = models.DateTimeField()
    updatedDate = models.DateTimeField(auto_now=True)
    # Extra Fields for future use
    Doc1image = models.ImageField(upload_to="img", null=True)
    Doc2image = models.ImageField(upload_to="img", null=True)
    Doc3image = models.ImageField(upload_to="img", null=True)
    Doc4image = models.ImageField(upload_to="img", null=True)
    Doc5image = models.ImageField(upload_to="img", null=True)
    intfield1 = models.IntegerField(null=True)
    intfield2 = models.IntegerField(null=True)
    intfield3 = models.IntegerField(null=True)
    intfield4 = models.IntegerField(null=True)
    intfield5 = models.IntegerField(null=True)
    DateField1 = models.DateTimeField(null=True)
    DateField2 = models.DateTimeField(null=True) 
    DateField3 = models.DateTimeField(null=True)
    DateField4 = models.DateTimeField(null=True)
    DateField5 = models.DateTimeField(null=True)
    Charfield1 = models.CharField(null=True, max_length=50)
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)
    Charfield6 = models.CharField(null=True, max_length=50)
    Charfield7 = models.CharField(null=True, max_length=50)
    Charfield8 = models.CharField(null=True, max_length=50)
    Charfield9 = models.CharField(null=True, max_length=50)
    Charfield10 = models.CharField(null=True, max_length=50)

    def save(self, *args, **kwargs):
        if self.Timestamp is None:
            self.Timestamp = date.today()
        super().save(*args, **kwargs)


class approved_customer_kyc(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.ForeignKey(form_STATUS, default=38, on_delete=models.PROTECT)
    # Application_No = models.IntegerField(unique=True, null=True)
    loandata = models.ForeignKey(
        Loan_Application_Details, unique=True, on_delete=models.CASCADE
    )
    Aadhaar = models.BigIntegerField()
    VoterCard = models.CharField(max_length=50)
    OtherKYCIdtype = models.ForeignKey(
        OTHERKYCTYPE,
        null=True,
        related_name="Other_KYC_Id_type",
        on_delete=models.PROTECT,
    )
    OtherKYCId = models.CharField(max_length=50, null=True)
    Custimage = models.ImageField(upload_to="img")
    Member_Aadhar_Card_front = models.ImageField(upload_to="img")
    Member_Aadhar_Card_back = models.ImageField(upload_to="img")
    Member_Voter_Card_front = models.ImageField(upload_to="img")
    Member_Voter_Card_back = models.ImageField(upload_to="img")
    Co_Insurer_Aadhaar_front = models.ImageField(upload_to="img")
    Co_Insurer_Aadhaar_back = models.ImageField(upload_to="img")
    Member_Bank_Details = models.ImageField(upload_to="img")
    Member_Relationship_Proof = models.ImageField(upload_to="img", null=True)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(null=True, max_length=50)
    Gender = models.ForeignKey(GENDER, on_delete=models.PROTECT)
    DateOfBirth = models.DateField()
    Age = models.IntegerField()
    MaritalStatus = models.ForeignKey(MaritalStatus, on_delete=models.PROTECT)
    FSName = models.CharField(max_length=50)
    FSType = models.ForeignKey(FSType, on_delete=models.PROTECT)
    FSDateOfBirth = models.DateField()
    FSAdhaar = models.BigIntegerField()
    MothersName = models.CharField(max_length=50)
    Caste = models.ForeignKey(CAST, on_delete=models.PROTECT)
    Religion = models.ForeignKey(Religion, on_delete=models.PROTECT)
    Qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT)
    Occupation = models.CharField(max_length=50)
    PhoneNumber = models.BigIntegerField()
    AddressLine1 = models.CharField(max_length=50)
    AddressLine2 = models.CharField(max_length=50)
    AddressLine3 = models.CharField(max_length=50)
    PreferredLanguage = models.ForeignKey(PreferredLanguage, on_delete=models.PROTECT)
    Pincode = models.PositiveIntegerField()
    Village = models.CharField(max_length=100)
    State = models.ForeignKey(
        state, related_name="Approved_state", on_delete=models.PROTECT
    )
    District = models.CharField(max_length=100)
    confirmAddressLine1 = models.CharField(max_length=50)
    confirmAddressLine2 = models.CharField(max_length=50)
    confirmAddressLine3 = models.CharField(max_length=50)
    confirmPincode = models.IntegerField(null=True)
    confirmVillage = models.CharField(max_length=100)
    confirmState = models.ForeignKey(
        state, related_name="Approved_confirm_State", on_delete=models.PROTECT
    )
    confirmDistrict = models.CharField(max_length=100)
    # FinancialDetails for customer
    HouseType = models.ForeignKey(HouseType, on_delete=models.PROTECT)
    LandInAcre = models.PositiveIntegerField()
    NumberofAnimals = models.PositiveIntegerField()
    PovertyLine = models.ForeignKey(PovertyLine, on_delete=models.PROTECT)
    BankName = models.ForeignKey(BankName, on_delete=models.PROTECT)
    BankAccountNo = models.BigIntegerField()
    # ConfirmBankAccountNo = models.BigIntegerField()
    BankIFSCCode = models.CharField(max_length=50)
    # ConfirmBankIFSCCode = models.CharField(max_length=50)
    # LoanDetails for customerKYC
    BranchName = models.ForeignKey(
        userWithRole, related_name="Approved_BranchName", on_delete=models.PROTECT
    )
    CenterId = models.ForeignKey(
        center, related_name="Approved_CenterId", on_delete=models.PROTECT
    )
    ProductCategory = models.ForeignKey(
        LoanDetails, related_name="Approved_Category_category", on_delete=models.PROTECT
    )
    CategoryType = models.ForeignKey(categoryType, on_delete=models.PROTECT)
    Product = models.ForeignKey(LoanDetails, on_delete=models.PROTECT)
    PurposeId = models.ForeignKey(PurposeId, on_delete=models.PROTECT)
    LoanAmount = models.PositiveIntegerField()
    InterestRate = models.FloatField()
    RepayFrequency = models.FloatField()
    GroupName = models.ForeignKey(GroupName, on_delete=models.PROTECT)
    # CoInsurerDetails for cutomerKYC
    CoInsurerRelation = models.CharField(max_length=50)
    CoInsurerName = models.CharField(max_length=50)
    CoInsurerDOB = models.DateField()
    CoInsurerAge = models.PositiveIntegerField()
    KYCIDType = models.ForeignKey(
        OTHERKYCTYPE, related_name="Approved_KYCID_Type", on_delete=models.PROTECT
    )
    KYCID = models.CharField(max_length=50)
    CoOccupation = models.CharField(max_length=50)
    RemarkComments = models.CharField(max_length=500)
    # NomineeDetails for customerKYC
    Disbursement_Payment_Mode = models.ForeignKey(
        DisbursementMode, on_delete=models.PROTECT
    )
    Loan_Cycle = models.IntegerField()
    Timestamp = models.DateTimeField()
    updatedDate = models.DateTimeField(auto_now=True)
    # Extra Fields for future use
    Doc1image = models.ImageField(upload_to="img", null=True)
    Doc2image = models.ImageField(upload_to="img", null=True)
    Doc3image = models.ImageField(upload_to="img", null=True)
    Doc4image = models.ImageField(upload_to="img", null=True)
    Doc5image = models.ImageField(upload_to="img", null=True)
    intfield1 = models.IntegerField(null=True)
    intfield2 = models.IntegerField(null=True)
    intfield3 = models.IntegerField(null=True)
    intfield4 = models.IntegerField(null=True)
    DateField1 = models.DateTimeField(null=True)
    DateField2 = models.DateTimeField(null=True)
    DateField3 = models.DateTimeField(null=True)
    DateField4 = models.DateTimeField(null=True)
    DateField5 = models.DateTimeField(null=True)
    Charfield1 = models.CharField(null=True, max_length=50)
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)

    def LPF(self):
        return self.LoanAmount *  self.Product.loanProcessingFee

    def LPC(self):
        return self.LoanAmount * self.Product.loanProcessingCharge

    def Total_amount(self):
        return self.LoanAmount - (self.LoanAmount * self.Product.loanProcessingCharge + self.LoanAmount * self.Product.loanProcessingFee)

    def save(self, *args, **kwargs):
        if self.Timestamp is None:
            self.Timestamp = date.today()
        super().save(*args, **kwargs)


class rejected_customer_kyc(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.ForeignKey(form_STATUS, default=39, on_delete=models.PROTECT)
    # Application_No = models.IntegerField(unique=True, null=True)
    loandata = models.ForeignKey(
        Loan_Application_Details, unique=True, on_delete=models.CASCADE
    )
    Aadhaar = models.BigIntegerField()
    VoterCard = models.CharField(max_length=50)
    OtherKYCIdtype = models.ForeignKey(
        OTHERKYCTYPE,
        null=True,
        related_name="rejected_KYC_Id_type",
        on_delete=models.PROTECT,
    )
    OtherKYCId = models.CharField(max_length=50, null=True)
    Custimage = models.ImageField(upload_to="img")
    Member_Aadhar_Card_front = models.ImageField(upload_to="img")
    Member_Aadhar_Card_back = models.ImageField(upload_to="img")
    Member_Voter_Card_front = models.ImageField(upload_to="img")
    Member_Voter_Card_back = models.ImageField(upload_to="img")
    Co_Insurer_Aadhaar_front = models.ImageField(upload_to="img")
    Co_Insurer_Aadhaar_back = models.ImageField(upload_to="img")
    Member_Bank_Details = models.ImageField(upload_to="img")
    Member_Relationship_Proof = models.ImageField(upload_to="img", null=True)
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(null=True, max_length=50)
    Gender = models.ForeignKey(GENDER, on_delete=models.PROTECT)
    DateOfBirth = models.DateField()
    Age = models.IntegerField()
    MaritalStatus = models.ForeignKey(MaritalStatus, on_delete=models.PROTECT)
    FSName = models.CharField(max_length=50)
    FSType = models.ForeignKey(FSType, on_delete=models.PROTECT)
    FSDateOfBirth = models.DateField()
    FSAdhaar = models.BigIntegerField()
    MothersName = models.CharField(max_length=50)
    Caste = models.ForeignKey(CAST, on_delete=models.PROTECT)
    Religion = models.ForeignKey(Religion, on_delete=models.PROTECT)
    Qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT)
    Occupation = models.CharField(max_length=50)
    PhoneNumber = models.BigIntegerField()
    AddressLine1 = models.CharField(max_length=50)
    AddressLine2 = models.CharField(max_length=50)
    AddressLine3 = models.CharField(max_length=50)
    PreferredLanguage = models.ForeignKey(PreferredLanguage, on_delete=models.PROTECT)
    Pincode = models.PositiveIntegerField()
    Village = models.CharField(max_length=100)
    State = models.ForeignKey(
        state, related_name="rejected_state", on_delete=models.PROTECT
    )
    District = models.CharField(max_length=100)
    confirmAddressLine1 = models.CharField(max_length=50)
    confirmAddressLine2 = models.CharField(max_length=50)
    confirmAddressLine3 = models.CharField(max_length=50)
    confirmPincode = models.IntegerField(
        null=True,
    )
    confirmVillage = models.CharField(max_length=100)
    confirmState = models.ForeignKey(
        state, related_name="rejected_confirm_State", on_delete=models.PROTECT
    )
    confirmDistrict = models.CharField(max_length=100)
    # FinancialDetails for customer
    HouseType = models.ForeignKey(HouseType, on_delete=models.PROTECT)
    LandInAcre = models.PositiveIntegerField()
    NumberofAnimals = models.PositiveIntegerField()
    PovertyLine = models.ForeignKey(PovertyLine, on_delete=models.PROTECT)
    BankName = models.ForeignKey(BankName, on_delete=models.PROTECT)
    BankAccountNo = models.BigIntegerField()
    # ConfirmBankAccountNo = models.BigIntegerField()
    BankIFSCCode = models.CharField(max_length=50)
    # ConfirmBankIFSCCode = models.CharField(max_length=50)
    # LoanDetails for customerKYC
    BranchName = models.ForeignKey(
        userWithRole, related_name="rejected_BranchName", on_delete=models.PROTECT
    )
    CenterId = models.ForeignKey(
        center, related_name="rejected_CenterId", on_delete=models.PROTECT
    )
    ProductCategory = models.ForeignKey(
        LoanDetails, related_name="rejected_Category_category", on_delete=models.PROTECT
    )
    CategoryType = models.ForeignKey(categoryType, on_delete=models.PROTECT)
    Product = models.ForeignKey(LoanDetails, on_delete=models.PROTECT)
    PurposeId = models.ForeignKey(PurposeId, on_delete=models.PROTECT)
    LoanAmount = models.PositiveIntegerField()
    InterestRate = models.FloatField()
    RepayFrequency = models.FloatField()
    GroupName = models.ForeignKey(GroupName, on_delete=models.PROTECT)
    # CoInsurerDetails for cutomerKYC
    CoInsurerRelation = models.CharField(max_length=50)
    CoInsurerName = models.CharField(max_length=50)
    CoInsurerDOB = models.DateField()
    CoInsurerAge = models.PositiveIntegerField()
    KYCIDType = models.ForeignKey(
        OTHERKYCTYPE, related_name="rejected_KYCID_Type", on_delete=models.PROTECT
    )
    KYCID = models.CharField(max_length=50)
    CoOccupation = models.CharField(max_length=50)
    RemarkComments = models.CharField(max_length=500)
    # Disbursement_Payment_Mode = models.ForeignKey(
    #     DisbursementMode,
    #     related_name="rejected_Disbursement_Payment_Mode",
    #     on_delete=models.PROTECT,
    # )
    # NomineeDetails for customerKYC
    Timestamp = models.DateTimeField()
    updatedDate = models.DateTimeField(auto_now=True)
    # Extra Fields for future use
    Doc1image = models.ImageField(upload_to="img", null=True)
    Doc2image = models.ImageField(upload_to="img", null=True)
    Doc3image = models.ImageField(upload_to="img", null=True)
    Doc4image = models.ImageField(upload_to="img", null=True)
    Doc5image = models.ImageField(upload_to="img", null=True)
    intfield1 = models.IntegerField(null=True)
    intfield2 = models.IntegerField(null=True)
    intfield3 = models.IntegerField(null=True)
    intfield4 = models.IntegerField(null=True)
    intfield5 = models.IntegerField(null=True)
    DateField1 = models.DateTimeField(null=True)
    DateField2 = models.DateTimeField(null=True)
    DateField3 = models.DateTimeField(null=True)
    DateField4 = models.DateTimeField(null=True)
    DateField5 = models.DateTimeField(null=True)
    Charfield1 = models.CharField(null=True, max_length=50)
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)

    def save(self, *args, **kwargs):
        if self.Timestamp is None:
            self.Timestamp = date.today()
        super().save(*args, **kwargs)


class preClosedLoan(models.Model):
    LoanId = models.ForeignKey(Loan_Application_Details, on_delete=models.PROTECT)
    PreclosedDate = models.DateField()
    PreclosedAmount = models.IntegerField()
    TotalPreclosedEmi = models.IntegerField()
    TotalEmi = models.IntegerField()
    createdDate = models.DateTimeField()
    updatedDate = models.DateTimeField(auto_now=True)
    intfield1 = models.IntegerField(null=True)
    intfield2 = models.IntegerField(null=True)
    intfield3 = models.IntegerField(null=True)
    intfield4 = models.IntegerField(null=True)
    intfield5 = models.IntegerField(null=True)
    DateField1 = models.DateTimeField(null=True)
    DateField2 = models.DateTimeField(null=True)
    DateField3 = models.DateTimeField(null=True)
    DateField4 = models.DateTimeField(null=True)
    DateField5 = models.DateTimeField(null=True)
    Charfield1 = models.CharField(null=True, max_length=50)
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)

    def __str__(self):
        return str(self.LoanId)


    def save(self, *args, **kwargs):
        if self.createdDate is None:
            self.createdDate = date.today()
        super().save(*args, **kwargs)




class auditTable(models.Model):
    LoanId = models.ForeignKey(Loan_Application_Details, on_delete=models.PROTECT)
    TransactionId = models.IntegerField(null=True)
    emiReverseBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    EmiReverseDate = models.DateTimeField()
    EmiInstallmentDate = models.DateTimeField()
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)

    def save(self, *args, **kwargs):
        if self.EmiReverseDate == None:
            self.EmiReverseDate = date.today()
        super().save(*args, **kwargs)


class emiStatus(models.Model):
    statusValue = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)
    updated_date = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return self.statusValue

class loanEMI(models.Model):
    center = models.ForeignKey(center, on_delete=models.PROTECT)
    preClosedId = models.ForeignKey(preClosedLoan, on_delete=models.PROTECT , null=True)
    loanId = models.ForeignKey(Loan_Application_Details, on_delete=models.CASCADE)
    emiStatus = models.ForeignKey(emiStatus, on_delete=models.PROTECT, default=2)
    loanMode = models.ForeignKey(Loan_mode_data, on_delete=models.PROTECT, default=7)
    installmentDate = models.DateTimeField()
    principleAmount = models.FloatField()
    interestAmoun = models.FloatField()
    installmentAmount = models.FloatField()
    outstandingPrincipal = models.FloatField()
    PaymentDate = models.DateTimeField(null=True)
    TransactionId = models.IntegerField(null=True)
    EmiPaymentMode = models.ForeignKey(
        DisbursementMode, on_delete=models.PROTECT, null=True
    )
    emiSubmittedBy = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    Doc3image = models.ImageField(upload_to="img", null=True)
    Doc4image = models.ImageField(upload_to="img", null=True)
    Doc5image = models.ImageField(upload_to="img", null=True)
    intfield1 = models.IntegerField(null=True)
    intfield3 = models.IntegerField(null=True)
    intfield4 = models.IntegerField(null=True)
    intfield5 = models.IntegerField(null=True)
    DateField2 = models.DateTimeField(null=True)
    DateField3 = models.DateTimeField(null=True)
    DateField4 = models.DateTimeField(null=True)
    DateField5 = models.DateTimeField(null=True)
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)

    def __str__(self):
        return str(self.loanId)

    def save(self, *args, **kwargs):
        if self.emiStatus.id == 1:
            self.PaymentDate = date.today()
        super().save(*args, **kwargs)


class disbursement_customer_kyc(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.ForeignKey(form_STATUS, default=41, on_delete=models.PROTECT)
    CustomerEMI = models.ForeignKey(loanEMI, null=True, on_delete=models.PROTECT)
    # Application_No = models.IntegerField(unique=True, null=True)
    loandata = models.ForeignKey(
        Loan_Application_Details, unique=True, on_delete=models.CASCADE
    )
    Aadhaar = models.BigIntegerField()
    OtherKYCIdtype = models.ForeignKey(
        OTHERKYCTYPE,
        null=True,
        related_name="disbursement_Other_KYC_Id_type",
        on_delete=models.PROTECT,
    )
    OtherKYCId = models.CharField(max_length=50, null=True)
    Custimage = models.ImageField(upload_to="img")
    VoterCard = models.CharField(max_length=50)
    Member_Aadhar_Card_front = models.ImageField(upload_to="img")
    Member_Aadhar_Card_back = models.ImageField(upload_to="img")
    Member_Voter_Card_front = models.ImageField(upload_to="img")
    Member_Voter_Card_back = models.ImageField(upload_to="img")
    Co_Insurer_Aadhaar_front = models.ImageField(upload_to="img")
    Co_Insurer_Aadhaar_back = models.ImageField(upload_to="img")
    Member_Bank_Details = models.ImageField(upload_to="img")
    Member_Relationship_Proof = models.ImageField(upload_to="img", null=True)
    group_Loan_Agreement = models.FileField(upload_to="pdf")
    FirstName = models.CharField(max_length=50)
    LastName = models.CharField(null=True, max_length=50)
    Gender = models.ForeignKey(GENDER, on_delete=models.PROTECT)
    DateOfBirth = models.DateField()
    Age = models.IntegerField()
    MaritalStatus = models.ForeignKey(MaritalStatus, on_delete=models.PROTECT)
    FSName = models.CharField(max_length=50)
    FSType = models.ForeignKey(FSType, on_delete=models.PROTECT)
    FSDateOfBirth = models.DateField()
    FSAdhaar = models.BigIntegerField()
    MothersName = models.CharField(max_length=50)
    Caste = models.ForeignKey(CAST, on_delete=models.PROTECT)
    Religion = models.ForeignKey(Religion, on_delete=models.PROTECT)
    Qualification = models.ForeignKey(Qualification, on_delete=models.PROTECT)
    Occupation = models.CharField(max_length=50)
    PhoneNumber = models.BigIntegerField()
    AddressLine1 = models.CharField(max_length=50)
    AddressLine2 = models.CharField(max_length=50)
    AddressLine3 = models.CharField(max_length=50)
    PreferredLanguage = models.ForeignKey(PreferredLanguage, on_delete=models.PROTECT)
    Pincode = models.PositiveIntegerField()
    Village = models.CharField(max_length=100)
    State = models.ForeignKey(
        state, related_name="disbursement_state", on_delete=models.PROTECT
    )
    District = models.CharField(max_length=100)
    confirmAddressLine1 = models.CharField(max_length=50)
    confirmAddressLine2 = models.CharField(max_length=50)
    confirmAddressLine3 = models.CharField(max_length=50)
    confirmPincode = models.IntegerField(null=True)
    confirmVillage = models.CharField(max_length=100)
    confirmState = models.ForeignKey(
        state, related_name="disbursement_confirm_State", on_delete=models.PROTECT
    )
    confirmDistrict = models.CharField(max_length=100)
    # FinancialDetails for customer
    HouseType = models.ForeignKey(HouseType, on_delete=models.PROTECT)
    LandInAcre = models.PositiveIntegerField()
    NumberofAnimals = models.PositiveIntegerField()
    PovertyLine = models.ForeignKey(PovertyLine, on_delete=models.PROTECT)
    BankName = models.ForeignKey(BankName, on_delete=models.PROTECT)
    BankAccountNo = models.BigIntegerField()
    # ConfirmBankAccountNo = models.BigIntegerField()
    BankIFSCCode = models.CharField(max_length=50)
    # ConfirmBankIFSCCode = models.CharField(max_length=50)
    # LoanDetails for customerKYC
    BranchName = models.ForeignKey(
        userWithRole, related_name="disbursement_BranchName", on_delete=models.PROTECT
    )
    CenterId = models.ForeignKey(
        center, related_name="disbursement_CenterId", on_delete=models.PROTECT
    )
    ProductCategory = models.ForeignKey(
        LoanDetails,
        related_name="disbursement_Category_category",
        on_delete=models.PROTECT,
    )
    CategoryType = models.ForeignKey(categoryType, on_delete=models.PROTECT)
    Product = models.ForeignKey(LoanDetails, on_delete=models.PROTECT)
    PurposeId = models.ForeignKey(PurposeId, on_delete=models.PROTECT)
    LoanAmount = models.PositiveIntegerField()
    InterestRate = models.FloatField()
    RepayFrequency = models.FloatField()
    GroupName = models.ForeignKey(GroupName, on_delete=models.PROTECT)
    # CoInsurerDetails for cutomerKYC
    CoInsurerRelation = models.CharField(max_length=50)
    CoInsurerName = models.CharField(max_length=50)
    CoInsurerDOB = models.DateField()
    CoInsurerAge = models.PositiveIntegerField()
    KYCIDType = models.ForeignKey(
        OTHERKYCTYPE, related_name="disbursement_KYCID_Type", on_delete=models.PROTECT
    )
    KYCID = models.CharField(max_length=50)
    CoOccupation = models.CharField(max_length=50)
    RemarkComments = models.CharField(max_length=500)
    # NomineeDetails for customerKYC
    Timestamp = models.DateTimeField()
    updatedDate = models.DateTimeField(auto_now=True)
    Disbursement_Payment_Mode = models.ForeignKey(
        DisbursementMode, related_name="Disburse_Payment_Mode", on_delete=models.PROTECT
    )
    Disbursement_Date = models.DateField(null=True)
    # Extra Fields for future use
    Doc2image = models.ImageField(upload_to="img", null=True)
    Doc3image = models.ImageField(upload_to="img", null=True)
    Doc4image = models.ImageField(upload_to="img", null=True)
    Doc5image = models.ImageField(upload_to="img", null=True)
    intfield1 = models.IntegerField(null=True)
    intfield2 = models.IntegerField(null=True)
    intfield3 = models.IntegerField(null=True)
    intfield4 = models.IntegerField(null=True)
    intfield5 = models.IntegerField(null=True)
    DateField1 = models.DateTimeField(null=True)
    DateField2 = models.DateTimeField(null=True)
    DateField3 = models.DateTimeField(null=True)
    DateField4 = models.DateTimeField(null=True)
    DateField5 = models.DateTimeField(null=True)
    Charfield1 = models.CharField(null=True, max_length=50)
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)


    def customerAddress(self):
        return self.AddressLine1 +" "+self.AddressLine2 +" "+ self.AddressLine3 +" "+ self.Village +" "+ self.District +" "+ self.State.state_Name +" "+ (str(self.Pincode))

    def LPC(self):
        return self.LoanAmount * self.Product.loanProcessingCharge

    def LPF(self):
        return self.LoanAmount * self.Product.loanProcessingFee
    
    def disbursementAmount(self):
        return self.LoanAmount - (self.LoanAmount * self.Product.loanProcessingCharge + self.LoanAmount * self.Product.loanProcessingFee)

    def Pre_Closure_Amount(self):
        totalPreClosureAmount = []
        OSPrinciple = []
        OSInterest = []
        OSInstallments = []
        principleArrear = []
        intrestArrear = []
        installmentArrear=[]
        totalEMIIntrest = []
        totalIntrest = loanEMI.objects.filter(loanId__loanId=self.loandata.loanId)
        arrearAmount = loanEMI.objects.filter(loanId__loanId=self.loandata.loanId , emiStatus__id=3)
        totalArrear = loanEMI.objects.filter(loanId__customerId=self.loandata.loanId).exclude(emiStatus__id=1)
        preClosureAmount = disbursement_customer_kyc.objects.filter(loandata__customerId=self.loandata.customerId).exclude(loandata__loanId=self.loandata.loanId)
        for arrear in arrearAmount:
            principleArrear.append(arrear.principleAmount) 
            intrestArrear.append(arrear.interestAmoun)
            installmentArrear.append(arrear.installmentAmount)
        if not preClosureAmount:
            pass
        else:
            for preCloseAmount in preClosureAmount:
                preClosureAmount = loanEMI.objects.filter(loanId__loanId=preCloseAmount.loandata.loanId).exclude(emiStatus__id=1)
                for amount in preClosureAmount:
                    totalPreClosureAmount.append(amount.principleAmount)
        for Intrest in totalIntrest:
            totalEMIIntrest.append(Intrest.interestAmoun)
        for Arrears in totalArrear:
            OSPrinciple.append(Arrears.principleAmount)
            OSInterest.append(Arrears.interestAmoun)
            OSInstallments.append(Arrears.installmentAmount)
        return {"totalPreClosureAmount":sum(totalPreClosureAmount), "OSPrinciple":sum(OSPrinciple),"OSInterest":sum(OSInterest),"OSInstallments":len(OSInstallments),"principleArrear":sum(principleArrear),"intrestArrear":sum(intrestArrear),"installmentArrear":sum(installmentArrear) ,"totalEMIIntrest":sum(totalEMIIntrest)}

    def totalEmiData(self):
        return loanEMI.objects.filter(loanId__loanId=self.loandata.loanId)

    def lastEmiData(self):
        return loanEMI.objects.filter(loanId__loanId=self.loandata.loanId).last()

    def pendingEmiData(self):
        return loanEMI.objects.filter(
            loanId__loanId=self.CustomerEMI.loanId.loanId, emiStatus__id=2
        ).first()

    def paidEMI(self):
        days = 0
        collectedEMI = (
            len(
                loanEMI.objects.filter(loanId__loanId=self.loandata.loanId).exclude(
                    emiStatus__id=2
                )
            )
            + 1
        )
        if Days := loanEMI.objects.filter(
            loanId__loanId=self.CustomerEMI.loanId.loanId, emiStatus__id=3
        ).last():
            days = (Days.installmentDate.date() - datetime.today().date()).days
        return {"collectedEMI": collectedEMI, "days": days}

    def notPaidEmiData(self):
        data = loanEMI.objects.filter(
            loanId__loanId=self.CustomerEMI.loanId.loanId, emiStatus__id=3
        )
        pAmount = 0
        iAmount = 0
        emiAmount = 0
        for Data in data:
            pAmount = pAmount + Data.principleAmount
            iAmount = iAmount + Data.interestAmoun
            emiAmount = emiAmount + Data.installmentAmount
        return {"pAmount": pAmount, "iAmount": iAmount, "emiAmount": emiAmount}

    def loanCycle(self):
        return Loan_Application_Details.objects.filter(Aadhaar=self.loandata.Aadhaar)
    
    def save(self, *args, **kwargs):
        if self.Timestamp is None:
            self.Timestamp = date.today()
        super().save(*args, **kwargs)


class TransactionsMode(models.Model):
    TransactionsValue = models.CharField(null=True, max_length=50)
    CreatedBy = models.CharField(null=True, max_length=50)
    UpdatedBy = models.CharField(null=True, max_length=50)
    CreatedDate = models.DateTimeField(null=True)
    UpadtedDate = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if self.CreatedDate is None:
            self.CreatedDate = date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.TransactionsValue


class BankTransactions(models.Model):
    TransactionsMode = models.ForeignKey(
        TransactionsMode, on_delete=models.PROTECT, null=True
    )
    BankName = models.ForeignKey(BankName, on_delete=models.PROTECT, null=True)
    branchName = models.ForeignKey(branch, on_delete=models.PROTECT, null=True)
    Center = models.ForeignKey(center, on_delete=models.PROTECT, null=True)
    AccountNumber = models.PositiveBigIntegerField(null=True)
    TransactionsAmount = models.IntegerField(null=True)
    TransactionsSlipNumber = models.CharField(max_length=50, null=True)
    Remarks = models.CharField(max_length=50, null=True)
    TransactionsDate = models.DateTimeField()
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)
    Doc3image = models.ImageField(upload_to="img", null=True)
    Doc4image = models.ImageField(upload_to="img", null=True)
    Doc5image = models.ImageField(upload_to="img", null=True)
    intfield1 = models.IntegerField(null=True)
    intfield3 = models.IntegerField(null=True)
    intfield4 = models.IntegerField(null=True)
    intfield5 = models.IntegerField(null=True)
    DateField2 = models.DateTimeField(null=True)
    DateField3 = models.DateTimeField(null=True)
    DateField4 = models.DateTimeField(null=True)
    DateField5 = models.DateTimeField(null=True)
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)

    # def save(self, *args, **kwargs):
    #     self.TransactionsDate = date.today()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class EmiCount(models.Model):
    EmiNumber = models.IntegerField()
    EmiNumberValue = models.CharField(null=True, max_length=50)
    CreatedBy = models.CharField(null=True, max_length=50)
    UpdatedBy = models.CharField(null=True, max_length=50)
    CreatedDate = models.DateTimeField()
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.EmiNumberValue

    def save(self, *args, **kwargs):
        if self.CreatedDate is None:
            self.CreatedDate = date.today()
        super().save(*args, **kwargs)


class EmiPaymentMode(models.Model):
    EmiPaymentModeName = models.CharField(null=True, max_length=50)
    CreatedBy = models.CharField(null=True, max_length=50)
    UpdatedBy = models.CharField(null=True, max_length=50)
    CreatedDate = models.DateTimeField()
    updatedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.EmiPaymentModeName

    def save(self, *args, **kwargs):
        if self.CreatedDate is None:
            self.CreatedDate = date.today()
        super().save(*args, **kwargs)


CALCULATION_TYPE = (("FLAT", "FLAT "), ("REDUCING", "REDUCING"))
LOAN_MODE = (("WEEKLY", "WEEKLY "), ("BIWEEKLY", "BIWEEKLY"), ("MONTHLY", "MONTHLY"))


class calculator(models.Model):
    calculation_type = models.CharField(choices=CALCULATION_TYPE, max_length=100)
    loanMode = models.CharField(choices=LOAN_MODE, max_length=100)
    rateOfIntrest = models.IntegerField()
    loan_amount = models.IntegerField()
    terms = models.IntegerField()


# class CurrencyNote(models.Model):
#     NoteName = models.CharField(max_length=100)
#     NoteValue = models.IntegerField()
#     CreatedBy = models.CharField(null=True, max_length=50)
#     UpdatedBy = models.CharField(null=True, max_length=50)
#     CreatedDate = models.DateTimeField()
#     updatedDate = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.NoteName

#     def save(self, *args, **kwargs):
#         if self.CreatedDate is None:
#             self.CreatedDate = date.today()
#         super().save(*args, **kwargs)


class Account_Transaction(models.Model):
    TrasID = models.CharField(max_length=10000)
    Branch = models.ForeignKey(branch, on_delete=models.PROTECT, null=True)
    Credit = models.IntegerField()
    Debit = models.IntegerField()
    AccountBalance = models.IntegerField()
    TransDate = models.DateTimeField()
    TransTimeStamp = models.DateTimeField(auto_now=True)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)
    Doc3image = models.ImageField(upload_to="img", null=True)
    Doc4image = models.ImageField(upload_to="img", null=True)
    Doc5image = models.ImageField(upload_to="img", null=True)
    intfield1 = models.IntegerField(null=True)
    intfield3 = models.IntegerField(null=True)
    intfield4 = models.IntegerField(null=True)
    intfield5 = models.IntegerField(null=True)
    DateField2 = models.DateTimeField(null=True)
    DateField3 = models.DateTimeField(null=True)
    DateField4 = models.DateTimeField(null=True)
    DateField5 = models.DateTimeField(null=True)
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)

    def __str__(self):
        return self.TrasID

    def save(self, *args, **kwargs):
        if not self.TrasID:
            self.TrasID = uuid.uuid4()
        super().save(*args, **kwargs)


class CashBookReport(models.Model):
    Branch_Name = models.ForeignKey(branch, on_delete=models.PROTECT)
    BranchManager = models.ForeignKey(User, on_delete=models.PROTECT)
    TransID = models.ForeignKey(
        Account_Transaction, on_delete=models.CASCADE, null=True
    )
    # CurrencyNote = models.ForeignKey(CurrencyNote, on_delete=models.PROTECT)
    BranchDayCloseDate = models.DateField()
    CashDate = models.DateField()
    CashBalance = models.IntegerField()
    Note2000 = models.IntegerField()
    Note500 = models.IntegerField()
    Note200 = models.IntegerField()
    Note100 = models.IntegerField()
    Note50 = models.IntegerField()
    Note20 = models.IntegerField()
    Note10 = models.IntegerField()
    Note5 = models.IntegerField()
    Note2 = models.IntegerField()
    Note1 = models.IntegerField()
    Coin20 = models.IntegerField()
    Coin10 = models.IntegerField()
    Coin5 = models.IntegerField()
    Coin2 = models.IntegerField()
    Coin1 = models.IntegerField()
    CreatedDate = models.DateTimeField()
    updatedDate = models.DateTimeField(auto_now=True)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)
    Doc3image = models.ImageField(upload_to="img", null=True)
    Doc4image = models.ImageField(upload_to="img", null=True)
    Doc5image = models.ImageField(upload_to="img", null=True)
    intfield1 = models.IntegerField(null=True)
    intfield3 = models.IntegerField(null=True)
    intfield4 = models.IntegerField(null=True)
    intfield5 = models.IntegerField(null=True)
    DateField2 = models.DateTimeField(null=True)
    DateField3 = models.DateTimeField(null=True)
    DateField4 = models.DateTimeField(null=True)
    DateField5 = models.DateTimeField(null=True)
    Charfield2 = models.CharField(null=True, max_length=50)
    Charfield3 = models.CharField(null=True, max_length=50)
    Charfield4 = models.CharField(null=True, max_length=50)
    Charfield5 = models.CharField(null=True, max_length=50)

    # def __str__(self):
    #     return self.BranchManager

    def save(self, *args, **kwargs):
        if self.CreatedDate is None:
            self.CreatedDate = date.today()
        super().save(*args, **kwargs)
