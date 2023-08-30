from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class loandataSerializer(serializers.ModelSerializer):  
    class Meta:
      model = Loan_Application_Details
      fields = '__all__'

class loanTypeSerializer(serializers.ModelSerializer): 
    class Meta:
      model = LoanDetails
      fields = '__all__'

class PurposeIdSerializer(serializers.ModelSerializer): 
    class Meta:
      model = PurposeId
      fields = '__all__'

class BankNameSerializer(serializers.ModelSerializer): 
    class Meta:
      model = BankName
      fields = '__all__'

class Disbursement_Payment_ModeSerializer(serializers.ModelSerializer): 
    class Meta:
      model = DisbursementMode
      fields = '__all__'

class GroupNameModeSerializer(serializers.ModelSerializer): 
    class Meta:
      model = GroupName
      fields = '__all__'


class customerDataSerializer(serializers.ModelSerializer):
    loandata = loandataSerializer()
    Product = loanTypeSerializer() 
    PurposeId = PurposeIdSerializer()
    BankName = BankNameSerializer()
    GroupName = GroupNameModeSerializer()
    Disbursement_Payment_Mode = Disbursement_Payment_ModeSerializer()
    class Meta:
      model = approved_customer_kyc
      fields =  ["id","PhoneNumber","GroupName","CoInsurerRelation","CoInsurerName","loandata","Product","PurposeId","Custimage","Disbursement_Payment_Mode","BankName","Timestamp","FirstName","LastName","LoanAmount","Loan_Cycle","RepayFrequency","BankAccountNo","BankIFSCCode","InterestRate"]


class Loan_mode_dataSerializer(serializers.ModelSerializer): 
    class Meta:
      model = Loan_mode_data
      fields = '__all__'

class editLoanSerializer(serializers.ModelSerializer):
    loanMode = Loan_mode_dataSerializer() 
    class Meta:
      model = LoanDetails
      fields = ["id","loanName","Product","loanMode","LoanAmount","InterestRate","Number_of_months","RepayFrequency","loanProcessingCharge","loanProcessingFee"]