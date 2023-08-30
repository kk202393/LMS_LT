from django.contrib import admin
from LOAN.models import *

@admin.register(userWithRole)
class userRoleModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user_role",
        "branchName",
        "group",
        "userName"
    ]


# Register your models here.
@admin.register(haed_office)
class haed_officeModelAdmin(admin.ModelAdmin):
    list_display = ["id", "haed_office_name", "created_date", "created_by"]

# @admin.register(loanProcessingCharges)
# class loanProcessingChargesModelAdmin(admin.ModelAdmin):
#     list_display = ["id", "loanProcessingCharge", "loanProcessingFee"]


@admin.register(circle)
class circleModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "haed_office_name",
        "circle_name",
        "created_date",
        "created_by",
    ]


@admin.register(zone)
class zoneModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "haed_office_name",
        "circle_name",
        "zone",
        "created_date",
        "created_by",
    ]

@admin.register(preClosedLoan)
class preClosedLoanAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "LoanId",
        "PreclosedDate",
        "TotalPreclosedEmi",
        "TotalEmi",
    ]




@admin.register(Loan_Application_Details)
class Loan_Application_Detailsadmin(admin.ModelAdmin):
    list_display = [
        "id",
        "loanId",
        "customerId",
    ]


@admin.register(dropDownList)
class dropDownListadmin(admin.ModelAdmin):
    list_display = [
        "id",
        "hLookupId",
        "hLookupName",
        "hLookupValue",
    ]


@admin.register(region)
class zoneModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "haed_office_name",
        "circle_name",
        "zone",
        "created_date",
        "region",
        "created_by",
    ]


@admin.register(branch)
class branchModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "haed_office_name",
        "circle_name",
        "zone",
        "branch_Name",
        "created_date",
        "created_by",
    ]


@admin.register(center)
class centerModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "haed_office_name",
        "circle_name",
        "zone",
        "branch_Name",
        "center_name",
        "created_date",
        "center_meeting_day",
        "created_by",
    ]
    # prepopulated_fields = {"center_Id":("branch_Name",)}
    readonly_fields= (
        "center_Id",
    )

@admin.register(userProfileRole)
class userProfileRoleModelAdmin(admin.ModelAdmin):
    list_display = [ "id","profileRoleName", "created_by"]


@admin.register(Agent)
class Agent_dataModelAdmin(admin.ModelAdmin):
    list_display = [ "id","user_Id", "agents_Name", "branch_Name"]


@admin.register(customerKYC)
class customerKYCModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "FirstName",
        "LastName",
    ]


@admin.register(approved_customer_kyc)
class approved_customer_kycModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "FirstName",
        "LastName",
    ]


@admin.register(rejected_customer_kyc)
class rejected_customer_kycModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "Aadhaar",
        "FirstName",
        "LastName",
        "Gender",
        "DateOfBirth",
        "MaritalStatus",
    ]


@admin.register(LoanDetails)
class LoanDetailsAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "loanName",
        "Product",
        "loanMode",
        "LoanAmount",
        "InterestRate",
        "RepayFrequency",
        "activateStatus"
    ]
    readonly_fields= (
        "RepayFrequency",
    )


@admin.register(state)
class stateAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "state_Name",
    ]


@admin.register(Dist)
class DistAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "State_id",
        "Dist_Name",
    ]


@admin.register(Loan_mode_data)
class Loan_mode_dataAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "loan_name",
    ]

@admin.register(OTHERKYCTYPE)
class OTHERKYCTYPEAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(GENDER)
class GENDERAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]


@admin.register(MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]


@admin.register(FSType)
class FSTypeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(CAST)
class CASTAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(Religion)
class ReligionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(PreferredLanguage)
class PreferredLanguageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(HouseType)
class PHouseTypeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(PovertyLine)
class PovertyLineAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(PurposeId)
class PurposeIdAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(categoryType)
class categoryTypeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(GroupName)
class GroupNameAdmin(admin.ModelAdmin):
    list_display = [
        "id",
    ]

@admin.register(BankName)
class BankNameAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "BankName_value"
    ]

@admin.register(form_STATUS)
class form_STATUSAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "form_STATUS_value",
    ]                    


@admin.register(DisbursementMode)
class DisbursementModeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "DisbursementModeName",
    ]                    

@admin.register(emiStatus)
class emiStatusModeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "statusValue",
        "created_by",
    ]  
 
  





@admin.register(loanEMI)
class loanEMIModeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "center",
        "loanId",
        "emiStatus",
        "installmentDate"
    ]  
 
  
    

@admin.register(EmiPaymentMode)
class lEmiPaymentModeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "EmiPaymentModeName",
    ]  
 
@admin.register(EmiCount)
class lEmiPaymentModeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "EmiNumber",
        "EmiNumberValue"
    ]  
 

@admin.register(auditTable)
class auditTableModeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "LoanId",
        "TransactionId"
    ]  

@admin.register(TransactionsMode)
class TransactionsModeModeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "TransactionsValue",
        "CreatedBy"
    ]  


@admin.register(BankTransactions)
class BankTransactionsModeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "TransactionsMode",
        "BankName"
    ]  


@admin.register(CashBookReport)
class CashBookReportModeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "Branch_Name",
        "BranchManager",
        "CashDate"
    ]  
@admin.register(Account_Transaction)
class Account_TransectionstModeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "TrasID",
        "Branch",
        "TransDate",
        "Debit",
    ] 


@admin.register(disbursement_customer_kyc)
class disbursement_customer_kycAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "FirstName",
        "LastName",
        # "Timestamp",
        # "DateOfBirth",
        # "MaritalStatus",
        # "VoterCard",
        # "FSType",
        # "FSName",
        # "FSDateOfBirth",
        # "MothersName",
        # "FSAdhaar",
        # "AddressLine1",
        # "AddressLine2",
        # "AddressLine3",
        # "Pincode",
        # "District",
        # "State",
        # "Caste",
        # "Religion",
        # "PreferredLanguage",
        # "Qualification",
        # "Aadhaar",
        # "OtherKYCIdtype",
        # "OtherKYCId",
        # "PhoneNumber",
    ]                    
