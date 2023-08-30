import string
import random
from tokenize import String
from twilio.rest import Client
from django.core import serializers
import json
import calendar
from datetime import datetime, timedelta ,date
from http.client import HTTPResponse
import numpy as np
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth, Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Q, Sum, Count , F
from .serializer import *
from rest_framework.renderers import JSONRenderer
# import qrcode as qr
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render , get_object_or_404
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from LOAN.forms import *
from LOAN.forms import customerKYCform
from LOAN.models import *
from django.contrib.auth import update_session_auth_hash

# Create your views here.


@login_required(login_url="")
def Region_field(request):
    fm = Regionform()
    user = request.user
    if request.method == "POST":
        haed_office_name = request.POST.get("haed_office_name")
        circle_name = request.POST.get("circle_name")
        zone = request.POST.get("zone")
        region = request.POST.get("region")
        obj = region(
            haed_office_name=haed_office_name,
            circle_name=circle_name,
            zone=zone,
            region=region,
            created_by=user,
        )
        obj.save()
    return render(request, "Region.html", {"form": fm})

@login_required(login_url="")
def change_password(request):
    if request.method == 'POST':
        form = MyPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password is changed successfully Please login again")
            return redirect('signin')
    else:
        form = MyPasswordChangeForm(user = request.user)
    return render(request, 'changePassword.html', {'form': form})

class MyPasswordResetView(PasswordResetView):
    template_name = '../templates/password_reset.html'
    email_template_name = '../templates/password_reset_email.html'
    success_url = reverse_lazy('myapp:password_reset_done')

@login_required(login_url="")
def region_view(request):
    regions = region.objects.all()
    messages.success(request, "Region is created successfully")
    return render(request, "region_view.html", {"regions": regions})


@login_required(login_url="")
def Zone(request):
    fm = zoneform()
    user = request.user
    if request.method == "POST":
        haed_office_name = request.POST.get("haed_office_name")
        circle_name = request.POST.get("circle_name")
        obj = zone(
            haed_office_name=haed_office_name, circle_name=circle_name, created_by=user
        )
        obj.save()
    return render(request, "zone.html", {"form": fm})

def installmentAmountButton(request):
    if request.method == "GET":
        loanAmount = request.GET.get("loanAmount")
        loanInterestRate = request.GET.get("loanInterestRate")
        loanRepayFrequency = request.GET.get("loanRepayFrequency")
        loanEmiMode = request.GET.get("loanEmiMode")
        loanEmiValue = Loan_mode_data.objects.get(id = loanEmiMode)
        p = int(loanAmount)  # get the loan amount from approved table
        R = float(loanInterestRate)  # get the loan intrestrate from approved table
        n = int(loanRepayFrequency)
        k = R / (12 * 100)  # find the intrest rate per month
        r = float(k / int(
            loanEmiValue.loan_name_value
        ))  # intrest rate divided by 2 for bi weekly loan
        loanEmi = p * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
    data = {
            "loanEmi": loanEmi,
        }
    return JsonResponse(data)

def newLoan(request):
    fm = newLoanForm()
    allLoans = LoanDetails.objects.all().order_by('-id')
    if request.method == "POST":
        loanName = request.POST.get("loanName")
        loanProductName = request.POST.get("Product")
        loanMode = request.POST.get("loanMode")
        loanAmount = request.POST.get("LoanAmount")
        interestRate = request.POST.get("InterestRate") 
        numberOfMonths = request.POST.get("Number_of_months")
        RepayFrequency = request.POST.get("RepayFrequency")
        loanProcessingCharge = request.POST.get("loanProcessingCharge")
        loanProcessingFee = request.POST.get("loanProcessingFee")
        installmentAmount = request.POST.get("installmentAmount")
        loanModeDetails = Loan_mode_data.objects.get(id = loanMode)
        createNewLoan = LoanDetails(
            loanName = loanName,
            Product = loanProductName,
            loanMode = loanModeDetails,
            LoanAmount = loanAmount,
            InterestRate = interestRate,
            RepayFrequency = RepayFrequency,
            Number_of_months = numberOfMonths,
            loanProcessingCharge = loanProcessingCharge,
            loanProcessingFee = loanProcessingFee,
        )
        createNewLoan.save()
        newLoanID =  LoanDetails.objects.aggregate(max=Max("id"))[
            "max"
        ]
        + 1
        newLoanDetails = LoanDetails.objects.get(id = newLoanID)
        messages.success(
            request, f"New loan is Created Successfully with {installmentAmount} EMI amount and {newLoanDetails.RepayFrequency} Repay Frequency for {newLoanDetails.Number_of_months} months."
            )
        # return render(request, "successRenderScreen.html")
        return redirect('successRenderScreen')
    else:
        fm = newLoanForm()
    return render(request, "newLoan.html", {"form": fm , "allLoans" : allLoans})


def successRenderScreen(request):
    return render(request, "successRenderScreen.html")



def collection_details(request):
    Region = region.objects.all()
    disbursementDate = None
    Center_Id = None
    customerEmilist = None
    customerEmiData = None
    customerEmiDataList = []
    customerList = []
    customerEmiAmount = None
    loanID = []    
    prprincipleAmount = 0
    disbursementDate =  str(date.today())
    role = Group.objects.get(name='Branch Manager')
    managerBranch = userWithRole.objects.get(userName=request.user)
    if request.method == "POST":
        Branch_Name = request.POST.get("branch")
        Center_Id = request.POST.get("centerID")
        disbursementDate = request.POST.get("disbursementDate")
        customerEmiData = loanEMI.objects.filter(
            center__id=Center_Id, PaymentDate__date = disbursementDate if disbursementDate  else str(date.today()), emiStatus__id=1
        )
        customerEmiAmount = loanEMI.objects.filter(
            center__id=Center_Id, PaymentDate__date = disbursementDate if disbursementDate  else str(date.today()), emiStatus__id=1
        ).values('loanId__loanId').annotate(principleAmountSum=Sum('principleAmount'),interestAmounSum=Sum('interestAmoun'),installmentAmountSum=Sum('installmentAmount'))
        for customerloanID in customerEmiData:
            if customerloanID.loanId.loanId not in loanID:
                customerEmiDataList.append(customerloanID)
                customer_data = disbursement_customer_kyc.objects.filter(
                loandata__loanId=customerloanID.loanId.loanId
                ).exclude(status__id = 42)
                for customer in customer_data:
                    customerList.append(customer)
            loanID.append(customerloanID.loanId.loanId)
        customerEmilist = zip(customerEmiDataList, customerList,customerEmiAmount)
    context = {
        "Region": Region,
        "customerEmiData": customerEmilist,
        "customerEmiDataList": customerEmiDataList,
        "prprincipleAmount": prprincipleAmount,
        "customerList":customerEmiDataList,
        'role':role,
        'managerBranch':managerBranch
    }
    return render(request, "collection_details.html", context)

def branchSummaryReport(request):
    agents = None
    agentCenterId = None
    agentCenterIdCount = None
    Agent = {}
    role = Group.objects.get(name='Branch Manager')
    managerBranch = userWithRole.objects.get(userName=request.user)
    branchName=branch.objects.all()
    if request.method == "POST": 
        Branch_Name = request.POST.get("branchName")
        branchSummaryDate = request.POST.get("branchSummaryDate")
        if Branch_Name:
            agents = center.objects.filter(branch_Name__id = Branch_Name)
            for agent in agents:
                agentCenterId = loanEMI.objects.filter(center__branch_Name__id = Branch_Name,center__agents_Name__id =  agent.agents_Name.id, installmentDate__date= branchSummaryDate).exclude(emiStatus__id=1)
                agentCenterIdCount = loanEMI.objects.filter(center__agents_Name__id = agent.agents_Name.id,installmentDate__date= branchSummaryDate).exclude(emiStatus__id=1).values('center__center_Id').annotate(count=Count('center__center_Id'))
                agentSubmitEmaiData = loanEMI.objects.filter(center__center_Id = agent.center_Id,center__branch_Name__id = Branch_Name , installmentDate__date= branchSummaryDate,center__agents_Name__id =  agent.agents_Name.id , emiStatus__id=1)
                LoanDisbursementData = disbursement_customer_kyc.objects.filter(CenterId__branch_Name__id = Branch_Name , Disbursement_Date = branchSummaryDate,CenterId__agents_Name__id = agent.agents_Name.id)
                Agent[agent.agents_Name.id] = [f'{agent.agents_Name.username}-{agent.agents_Name.first_name}',
                                   agentCenterIdCount.count(),agentCenterId.count(),agentCenterId.values('center__agents_Name__id').annotate(agentSubmitInstallmentSum=Sum('installmentAmount')),agentSubmitEmaiData.values('center__agents_Name__id').annotate(agentSubmitInstallmentAmountSum=Sum('installmentAmount'))
                                   ,LoanDisbursementData.values('CenterId__agents_Name__id').annotate(disburseAmountSum=Sum('LoanAmount')),LoanDisbursementData.values('CenterId__agents_Name__id').annotate(LPFAmountSum=Sum(F('LoanAmount') * F('Product__loanProcessingFee'))),LoanDisbursementData.values('CenterId__agents_Name__id').annotate(LPCAmountSum=Sum(F('LoanAmount') * F('Product__loanProcessingCharge')))]
        else:
            pass    
    context = {
        "branchName":branchName,
        "agents":agents,
        "agentCenterId":agentCenterId,
        "agentEmiData":Agent,
        "agentCenterIdCount":agentCenterIdCount,
        "role":role,
        'managerBranch':managerBranch
    }
    return render(request, "branchSummaryReport.html",context)


@login_required(login_url="")
def disburseCustomerDetails(request,id):
    disburseCustDetails = disbursement_customer_kyc.objects.filter(id = id)
    for customerDetails in disburseCustDetails:
        dist = Dist.objects.get(id=customerDetails.District)
        confirmdist = Dist.objects.get(id=customerDetails.confirmDistrict)
    return render(request, "disburseCustDetails.html",{"custoner_data":disburseCustDetails,"dist":dist,"confirmdist":confirmdist})

@login_required(login_url="")
def zone_view(request):
    zones = zone.objects.all()
    messages.success(request, "Zone is created successfully")
    return render(request, "zone_view.html", {"zones": zones})


def newUserRole(request):
    form = userProfile(request.POST)
    if request.method == "POST":
        profileRoleName = request.POST["profileRoleName"]
        agentBranch= userProfileRole(
            profileRoleName = profileRoleName,
            created_by=request.user.first_name,
            updated_by=request.user.first_name,
        )
        agentBranch.save()
        messages.success(request, "User Profile is created successfully")
        return redirect('successRenderScreen')
    else:
        form = userProfile()
        return render(request,"newUserRole.html",{"form": form,},)



@login_required(login_url="")
def Agents(request):
    form = userForm(request.POST)
    if request.method == "POST":
        User_ID = request.POST["userName"]
        user_actual_Name = request.POST["user_actual_Name"]
        branchName = request.POST.get("branchName")
        user_role = request.POST.get("user_role")
        groups = request.POST.get("group")
        agentBranch= userWithRole(
            userName=User.objects.get(id=User_ID),
            user_actual_Name=user_actual_Name,
            branchName=branch.objects.get(id=branchName),
            user_role = userProfileRole.objects.get(id = user_role),
            group = Group.objects.get(id = groups)
        )
        if user_role == 2:
            isStaffTrueUser = User.objects.get(id=User_ID)
            isStaffTrueUser.is_staff = True
            isStaffTrueUser.save()
        branchAllReadyAssign = userWithRole.objects.filter(userName = User.objects.get(id=User_ID))
        if branchAllReadyAssign:
            messages.warning(request, "Branch is Already Assigned Successfully")
        else:
            agentBranch.save()
            messages.success(request, "Branch is Assigned successfully")
        # return render(request, "successRenderScreen.html")
        return redirect('successRenderScreen')
    else:
        form = userForm()
        return render(request,"agentBranch.html",{"form": form,},)
    


@login_required(login_url="")
def center_ID(request):
    role = Group.objects.get(name='Branch Manager')
    form = centerIdform(request, request.POST,)
    if request.method == "POST":
        branchID = request.POST.get("branch_Name")
        agentID = request.POST.get("agents_Name")
        centerName = request.POST.get("center_name")
        centerMeetingTime = request.POST.get("center_meeting_time") 
        centerMeetingDay = request.POST.get("center_meeting_day")
        centerID = request.POST.get("centerID")
        centerLeaderName = request.POST.get("center_leader")
        if not centerMeetingTime and not centerMeetingDay and not centerID:
            centerDetails = branch.objects.get(id = branchID)
            agentDetails = User.objects.get(id = agentID)
            createCenterID = center(
                haed_office_name = centerDetails.haed_office_name,
                circle_name = centerDetails.circle_name,
                center_name = centerName,
                zone = centerDetails.zone,
                region = centerDetails.region,
                branch_Name = centerDetails,
                agents_Name = agentDetails,
                created_by = request.user,
                center_leader = centerLeaderName
            )
            createCenterID.save()
            maxCenterID =  center.objects.aggregate(max=Max("id"))[
                "max"
            ]
            + 1
            agentCenterID = center.objects.get(id = maxCenterID)
            messages.success(
                request, f"Center Id {agentCenterID.center_Id} is Created Successfully for {agentDetails.first_name.title()} {agentDetails.last_name.title()} Agent"
                )
            # return render(request, "successRenderScreen.html")
            return redirect('successRenderScreen')
        elif centerMeetingTime and  centerMeetingDay and centerID:
            centerIdDataUpdate = center.objects.get(center_Id=centerID)
            centerIdDataUpdate.center_meeting_time = centerMeetingTime
            centerIdDataUpdate.center_meeting_day = centerMeetingDay
            centerIdDataUpdate.center_leader = centerLeaderName
            centerIdDataUpdate.save()
            messages.success(
                request, f"Center Id is Updated Successfully"
                )
            # return render(request, "successRenderScreen.html")
            return redirect('successRenderScreen')
    else:
        pass
    return render(request, "centerID.html", {"form": form,"role":role})


def centerIdDetail(request):
    if request.method == "GET":
        centerID = request.GET.get("centerID")
        loandata = center.objects.get(center_Id=centerID)
        data = {
            "LoanAmount": loandata.center_Id,
            "centerName": loandata.center_name,
            "branchName": loandata.branch_Name.branch_Name,
            "agentID": loandata.agents_Name.username,
            "agentName": loandata.agents_Name.first_name,
            "centerLeader": loandata.center_leader,
        }
    return JsonResponse(data)



@login_required(login_url="")
def Agent_user(request):
    userID = (1001 if User.objects.count() == 0 else User.objects.aggregate(max=Max("id"))["max"] + 10000)
    if request.method == "POST":
        form = customerRegistraionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
            request, "User is Created Successfully"
            )
            # return render(request, "successRenderScreen.html")
            return redirect('successRenderScreen')
    else:
        form = customerRegistraionForm(initial={
            'username': userID
        })
    return render(request,"useragent.html",{"form": form})

# managerBranch     user_role
@login_required(login_url="")
def desbord(request):
    user = request.user
    managerBranch = userWithRole.objects.get(userName = user)
    role = Group.objects.get(name='Branch Manager')
    if request.user.is_superuser == True:
        return render(request, "home.html", {"user": user, "role": role})
    elif managerBranch.user_role.id == 2:
        return render(request, "home.html", {"user": user, "role": role})
    else:
        return render(request, "home.html", {"user": user})


@login_required(login_url="")
def center_meeting(request):
    role = Group.objects.get(name='Branch Manager')
    return render(request, "center_meeting.html", {"role": role})


@login_required(login_url="")
def addCenterMeeting(request):
    return render(request, "addCenterMeeting.html")


@login_required(login_url="")
def reverseEMI(request, TransactionId, loanId):
    reverse_emi = loanEMI.objects.filter(
        TransactionId=TransactionId, loanId__loanId=loanId
    )
    for emi in reverse_emi:
        if str(emi.PaymentDate.date() + timedelta(days=1)) == str(
            datetime.now().date()
        ):
            auditData = auditTable(
                TransactionId=emi.TransactionId,
                LoanId=Loan_Application_Details.objects.get(loanId=emi.loanId.loanId),
                emiReverseBy=request.user,
                EmiInstallmentDate=emi.installmentDate,
            )
            auditData.save()
            emi.emiStatus = emiStatus.objects.get(id=2)
            emi.TransactionId = None
            emi.save()
            message = "EMI Reversed successfully"
        else:
            message = "You can not Reverse this EMI"
            break
    context = {"message": message}
    return render(request, "submit_reverse_collection.html", context)


@login_required(login_url="")
def collection_reverse(request):
    role = Group.objects.get(name='Branch Manager')
    reverseEMI1 = None
    loanReverseEmi = None
    reverseEMI = None
    message = None
    max = None
    TransactionId = None
    Amount_Collected_Date = None
    emiAmountCount = 0
    if request.method == "POST":
        loanID = request.POST.get("loanId")
        try:
            if loanID:
                loanReverseEmi = disbursement_customer_kyc.objects.get(
                    loandata__loanId=loanID
                )
                paidEmi = loanEMI.objects.filter(
                    loanId__loanId=loanReverseEmi.loandata.loanId, emiStatus__id=1
                )
                max = paidEmi.aggregate(Max("TransactionId"))
                if max.get("TransactionId__max") != None:
                    reverseEMI = loanEMI.objects.filter(
                        TransactionId=max.get("TransactionId__max"),
                        loanId__loanId=loanReverseEmi.loandata.loanId,emiStatus__id=1
                    )
                    reverseEMI1 = loanEMI.objects.filter(
                        TransactionId=max.get("TransactionId__max"),
                        loanId__loanId=loanReverseEmi.loandata.loanId,emiStatus__id=1
                    ).last()
                    Amount_Collected_Date = reverseEMI1.PaymentDate.date() + timedelta(days=int(1))
                    for emi_ID in reverseEMI:
                        TransactionId = emi_ID.TransactionId
                        emiAmountCount = emiAmountCount + emi_ID.installmentAmount
                        # break
                else:
                    message = "No EMI Paid"
        except Exception:
            loanReverseEmi = None
            message = "No Record Found"
            reverseEMI = None
            max = None
            TransactionId = None
    else:
        loanReverseEmi = None
        message = None
        reverseEMI = None
        max = None
        TransactionId = None
    context = {
        "loanReverseEmi": loanReverseEmi,
        "Amount_Collected_Date":Amount_Collected_Date,
        "emi": reverseEMI1,
        "message": message,
        "max": max,
        "TransactionId": TransactionId,
        "emiAmountCount": emiAmountCount,
        "role":role
    }
    return render(request, "collection_reverse.html", context)


@login_required(login_url="")
def cross_sell_cash_sell(request):
    role = Group.objects.get(name='Branch Manager')
    return render(request, "cross_sell_cash_sell.html", {"role": role})


@login_required(login_url="")
def add_cross_sell_cash_sell(request):
    return render(request, "add_cross_sell_cash_sell.html")


@login_required(login_url="")
def Credit_Bureau_Check(request):
    role = Group.objects.get(name='Branch Manager')
    return render(request, "Credit_Bureau_Check.html", {"role": role})


@login_required(login_url="")
def branchDayClose(request):
    [EmiData,ProcessCharge,Branch_Name,error,branchCashBook,Branches,role,managerBranch,closingBalancePendingMessage] = [None,None ,None,None,None,None,None,None,None]
    PriAmount = 0
    IntAmount = 0
    AmountLPC = 0
    AmountLPF = 0
    LoanAmount = 0
    ClosingBalance = 0
    openingBalance = 0
    bankWithdrawalAmount = 0
    bankDeposite = 0
    preCloseIntrestAmount = 0
    preclosureEmiAmount = 0
    preClosedLoanIdList = []
    preClosedOutstandingPrincipleAmount = []
    Date = date.today()
    try:
        managerBranch = userWithRole.objects.get(userName = request.user)
        role = Group.objects.get(name='Branch Manager')
    except userWithRole.DoesNotExist:
        Branches = branch.objects.all()
    try:
        closingBalancePending = Account_Transaction.objects.get(TransDate__date = (date.today() - timedelta(days=int(1))))
    except Account_Transaction.DoesNotExist:
        closingBalancePendingMessage = "Please enter last day closing Amount"
    if request.method == "POST":
        closingBalancePendingMessage = None
        Date = request.POST.get("dateRange")
        closingDate = request.POST.get("closing_date")
        Branch = request.POST.get("branch")    #  CalculatedBalance  branchDayCloseDate
        closingBranch = request.POST.get("closing_branch")
        CalculatedBalance = request.POST.get("CalculatedBalance")
        branchDayCloseDate = request.POST.get("branchDayCloseDate")
        try:
            depositeAmounts = BankTransactions.objects.filter(
                TransactionsDate=Date,
                branchName__id=Branch,
                TransactionsMode__id=1,  
            )
            withdrawalAmounts = BankTransactions.objects.filter(
                TransactionsDate=Date,
                branchName__id=Branch,
                TransactionsMode__id=2,  
            )
            datetime_object = datetime.strptime(Date, '%Y-%m-%d').date()
            openingBalanceAmount = Account_Transaction.objects.filter(TransDate__date = (datetime_object - timedelta(days=int(1))))
            if openingBalanceAmount:
                for openingBalances in openingBalanceAmount:
                    openingBalance = openingBalances.AccountBalance
            else:
                Account_TransactionID =  Account_Transaction.objects.aggregate(max=Max("id"))["max"] - 1
                openingBalances = Account_Transaction.objects.get(id = Account_TransactionID)
                openingBalance = openingBalances.AccountBalance
        except:
            ClosingBalance = 0
        if Date and Branch:
            max_Trans_ID = Account_Transaction.objects.all().aggregate(Max("id"))
            dayCloseRecord1 = Account_Transaction.objects.get(id=max_Trans_ID["id__max"]).TransDate.date() + timedelta(days=int(2))
            dayCloseRecord2 = date.today() - timedelta(days=int(1))
            if str(dayCloseRecord1) != str(Date):
                lastDayCloseDate = Account_Transaction.objects.aggregate(max=Max("TransDate"))["max"].date() + timedelta(days=int(2))
                start = datetime.strptime(str(lastDayCloseDate), "%Y-%m-%d")
                end = datetime.strptime(str(datetime.today().date()), "%Y-%m-%d")
                date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]
                messages.success(
                request, f"First submit day close for existing dates"
                )
                return render(request, "successRenderScreen.html",{"lastDayCloseDate":date_generated})
            else:
                Branch_Name = branch.objects.get(id=Branch)
                EmiData = loanEMI.objects.filter(
                    PaymentDate=Date, center__branch_Name__id=Branch, emiStatus__id=1
                )
                ProcessCharge = disbursement_customer_kyc.objects.filter(
                    BranchName__branchName__branch_Name=Branch_Name,
                    Disbursement_Date=Date,
                    Disbursement_Payment_Mode__id=2,
                )
                preclosureEmi = loanEMI.objects.filter(
                    PaymentDate=Date,
                    center__branch_Name__branch_Name=Branch_Name,
                    emiStatus__id = 4
                    )
                for preClosedLoanId in preclosureEmi:
                    if preClosedLoanId.loanId.loanId not in preClosedLoanIdList:
                        preClosedLoanIdList.append(preClosedLoanId.loanId.loanId)
                    preClosedEmiData = loanEMI.objects.filter(
                        loanId__loanId__in = preClosedLoanIdList,
                        emiStatus__id= 1
                        ).order_by('-id')
                    if preClosedEmiData:
                        for preClosedOutstandingPrinciple in preClosedEmiData:
                            if preClosedOutstandingPrinciple.loanId.loanId not in preClosedOutstandingPrincipleAmount:
                                preClosedOutstandingPrincipleAmount.append(preClosedOutstandingPrinciple.loanId.loanId)
                                preclosureEmiAmount = preclosureEmiAmount + preClosedOutstandingPrinciple.outstandingPrincipal
                                preCloseIntrestRate = disbursement_customer_kyc.objects.get(loandata__loanId = preClosedOutstandingPrinciple.loanId.loanId)
                                daysForIntrest = abs(int((preClosedOutstandingPrinciple.PaymentDate.date() - datetime.today().date()).days)  / 365)
                                preCloseIntrestAmount = preCloseIntrestAmount + (preClosedOutstandingPrinciple.outstandingPrincipal * daysForIntrest * preCloseIntrestRate.Product.InterestRate) / 100
                    else:
                        pass # if there is not paied emi 

                for depositAmount in depositeAmounts:
                    bankDeposite += depositAmount.TransactionsAmount
                for withdrawalAmount in withdrawalAmounts:
                    bankWithdrawalAmount += withdrawalAmount.TransactionsAmount
                for amount in EmiData:
                    PriAmount = PriAmount + amount.principleAmount
                    IntAmount = IntAmount + amount.interestAmoun
                PriAmount = PriAmount + preclosureEmiAmount
                IntAmount = IntAmount + preCloseIntrestAmount
                for Charge in ProcessCharge:
                    AmountLPC = AmountLPC + int(Charge.LPC())
                    AmountLPF = AmountLPF + int(Charge.LPF())
                    LoanAmount = Charge.LoanAmount
                ClosingBalance = (PriAmount + IntAmount + AmountLPC + AmountLPF + openingBalance + bankWithdrawalAmount) - (
                    LoanAmount + bankDeposite
                )
        else:
            ClosingBalance = 0
        if closingDate and closingBranch:
            try:
                branchCashBook = CashBookReport.objects.filter(
                    Branch_Name__id=closingBranch, CashDate=closingDate
                )
            except:
                branchCashBook = None
                error = "NO RECORD FOUND"
        if CalculatedBalance and branchDayCloseDate:
            messages.success(
                request, f"Day close amount submitted succefully"
                )
            return render(request, "successRenderScreen.html")
    context = {
        "closingBalancePendingMessage":closingBalancePendingMessage,
        "Branches": Branches,
        "Branch": Branch_Name,
        "ClosingBalance": ClosingBalance,
        "branchDayCloseDate":Date,
        "branch_CashBook": branchCashBook,
        "error": error,
        "managerBranch":managerBranch,
        "role":role
    }
    return render(request, "branchDayClose.html", context)


@login_required(login_url="")
def loan(request):
    return render(request, "loan.html")


@login_required(login_url="")
def loanCalculator(request):
    fm = calculatorForm()
    emi = 0
    if request.method == "POST":
        calculationType = request.POST.get("calculation_type")
        loanMode = request.POST.get("loanMode")
        R = float(request.POST.get("rateOfIntrest"))
        p = int(request.POST.get("loan_amount"))
        n = int(request.POST.get("terms"))
        if (calculationType == "REDUCING") & (loanMode == "WEEKLY"):
            Rate = R / 4
            r = Rate / (12 * 100)
            emi = p * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
        elif (calculationType == "REDUCING") & (loanMode == "BIWEEKLY"):
            Rate = R / 2
            r = Rate / (12 * 100)
            emi = p * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
        elif (calculationType == "REDUCING") & (loanMode == "MONTHLY"):
            Rate = R / 1
            r = Rate / (12 * 100)
            emi = p * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
    else:
        fm = calculatorForm()
    return render(request, "loanCalculator.html", {"form": fm, "finalAmount": emi})


@login_required(login_url="")
def CustomerKYC(request):
    try:
        if request.user.is_superuser != True:
            return redirect("/AgentCustomer")
        AppID = commonfield.objects.all()
        return render(request, "customerKYC.html", {"AppID": AppID})
    except Exception:
        return render(request, "customerKYC.html", {"AppID": AppID})


@login_required(login_url="signin")
def AgentCustomerKYC(request):
    # try:
    user = request.user
    regno = (
        1001
        if Loan_Application_Details.objects.count() == 0
        else Loan_Application_Details.objects.aggregate(max=Max("Application_No"))[
            "max"
        ]
        + 1
    )
    if request.method == "POST":
        fm = customerKYCform(request, request.POST, request.FILES)
        if fm.is_valid():
            AadhaarNumber = fm.cleaned_data["Aadhaar"]
            # Application_No = fm.cleaned_data["Application_No"]
            VoterCard = fm.cleaned_data["VoterCard"]
            KycIdType = fm.cleaned_data["OtherKYCIdtype"]
            kycId = fm.cleaned_data["OtherKYCId"]
            custimg = fm.cleaned_data["Custimage"]
            Member_Aadhar_Card_front = fm.cleaned_data["Member_Aadhar_Card_front"]
            Member_Aadhar_Card_back = fm.cleaned_data["Member_Aadhar_Card_back"]
            Member_Voter_Card_front = fm.cleaned_data["Member_Voter_Card_front"]
            Member_Voter_Card_back = fm.cleaned_data["Member_Voter_Card_back"]
            Co_Insurer_Aadhaar_front = fm.cleaned_data["Co_Insurer_Aadhaar_front"]
            Co_Insurer_Aadhaar_back = fm.cleaned_data["Co_Insurer_Aadhaar_back"]
            Member_Bank_Details = fm.cleaned_data["Member_Bank_Details"]
            Member_Relationship_Proof = fm.cleaned_data["Member_Relationship_Proof"]
            FirstName = fm.cleaned_data["FirstName"]
            LastName = fm.cleaned_data["LastName"]
            Gender = fm.cleaned_data["Gender"]
            DateOfBirth = fm.cleaned_data["DateOfBirth"]
            Age = fm.cleaned_data["Age"]
            MaritalStatus = fm.cleaned_data["MaritalStatus"]
            FsName = fm.cleaned_data["FSName"]
            FsType = fm.cleaned_data["FSType"]
            FsDOB = fm.cleaned_data["FSDateOfBirth"]
            FsAdhaar = fm.cleaned_data["FSAdhaar"]
            MotherName = fm.cleaned_data["MothersName"]
            Caste = fm.cleaned_data["Caste"]
            Religion = fm.cleaned_data["Religion"]
            Qualification = fm.cleaned_data["Qualification"]
            Occupation = fm.cleaned_data["Occupation"]
            PhoneNumber = fm.cleaned_data["PhoneNumber"]
            AddLine1 = fm.cleaned_data["AddressLine1"]
            AddLine2 = fm.cleaned_data["AddressLine2"]
            AddLine3 = fm.cleaned_data["AddressLine3"]
            Language = fm.cleaned_data["PreferredLanguage"]
            Village = fm.cleaned_data["Village"]
            District = fm.cleaned_data["District"]
            State = fm.cleaned_data["State"]
            PinCode = fm.cleaned_data["Pincode"]
            confirmAddressLine1 = fm.cleaned_data["confirmAddressLine1"]
            confirmAddressLine2 = fm.cleaned_data["confirmAddressLine2"]
            confirmAddressLine3 = fm.cleaned_data["confirmAddressLine3"]
            confirmVillage = fm.cleaned_data["confirmVillage"]
            confirmDistrict = fm.cleaned_data["confirmDistrict"]
            confirmState = fm.cleaned_data["confirmState"]
            confirmPincode = fm.cleaned_data["confirmPincode"]
            HouseType = fm.cleaned_data["HouseType"]
            LandInAcre = fm.cleaned_data["LandInAcre"]
            PovertyLine = fm.cleaned_data["PovertyLine"]
            NoOfAnimals = fm.cleaned_data["NumberofAnimals"]
            BankName = fm.cleaned_data["BankName"]
            BankAccountNo = fm.cleaned_data["BankAccountNo"]
            ConfirmbankAccountNo = fm.cleaned_data["ConfirmBankAccountNo"]
            BankIFSCcode = fm.cleaned_data["BankIFSCCode"]
            ConfirmbankIFSCcode = fm.cleaned_data["ConfirmBankIFSCCode"]
            Branch = fm.cleaned_data["BranchName"]
            CenterId = fm.cleaned_data["CenterId"]
            CategoryType = fm.cleaned_data["CategoryType"]
            productCategory = fm.cleaned_data["ProductCategory"]
            Product = fm.cleaned_data["Product"]
            PurposeId = fm.cleaned_data["PurposeId"]
            LoanAmount = fm.cleaned_data["LoanAmount"]
            IntRate = fm.cleaned_data["InterestRate"]
            RepayFreq = fm.cleaned_data["RepayFrequency"]
            GroupName = fm.cleaned_data["GroupName"]
            CoInsurerRelation = fm.cleaned_data["CoInsurerRelation"]
            CoInsurerName = fm.cleaned_data["CoInsurerName"]
            CoOccupation = fm.cleaned_data["CoOccupation"]
            CoInsurerdob = fm.cleaned_data["CoInsurerDOB"]
            CoInsurerage = fm.cleaned_data["CoInsurerAge"]
            CokycIdType = fm.cleaned_data["KYCIDType"]
            KycId = fm.cleaned_data["KYCID"]
            RemarkComments = fm.cleaned_data["RemarkComments"]
            Cust_Id = Loan_Application_Details.objects.filter(
                Aadhaar=AadhaarNumber
            ).first()
            try:
                Customer_Id = Cust_Id.customerId
            except:
                Customer_Id = (
                    1001
                    if Loan_Application_Details.objects.count() == 0
                    else Loan_Application_Details.objects.aggregate(
                        max=Max("Application_No")
                    )["max"]
                    + 1
                )
            data1 = Loan_Application_Details(
                Aadhaar=AadhaarNumber,
                Application_No=regno,
                customerId=Customer_Id,
                loanId=regno,
            )
            data1.save()
            # request.session["session_id"] = AadhaarNumber
            data = Loan_Application_Details.objects.get(loanId=regno)
            data2 = customerKYC(
                user=user,
                # Application_No=regno,
                loandata=data,
                Aadhaar=AadhaarNumber,
                VoterCard=VoterCard,
                OtherKYCIdtype=KycIdType,
                OtherKYCId=kycId,
                Custimage=custimg,
                Member_Aadhar_Card_front=Member_Aadhar_Card_front,
                Member_Aadhar_Card_back=Member_Aadhar_Card_back,
                Member_Voter_Card_front=Member_Voter_Card_front,
                Member_Voter_Card_back=Member_Voter_Card_back,
                Co_Insurer_Aadhaar_front=Co_Insurer_Aadhaar_front,
                Co_Insurer_Aadhaar_back=Co_Insurer_Aadhaar_back,
                Member_Bank_Details=Member_Bank_Details,
                Member_Relationship_Proof=Member_Relationship_Proof,
                FirstName=FirstName,
                LastName=LastName,
                Gender=Gender,
                DateOfBirth=DateOfBirth,
                Age=Age,
                MaritalStatus=MaritalStatus,
                FSName=FsName,
                FSType=FsType,
                FSDateOfBirth=FsDOB,
                MothersName=MotherName,
                FSAdhaar=FsAdhaar,
                Caste=Caste,
                Religion=Religion,
                Qualification=Qualification,
                Occupation=Occupation,
                PhoneNumber=PhoneNumber,
                AddressLine1=AddLine1,
                AddressLine2=AddLine2,
                AddressLine3=AddLine3,
                PreferredLanguage=Language,
                Village=Village,
                District=District,
                State=State,
                Pincode=PinCode,
                confirmAddressLine1=confirmAddressLine1,
                confirmAddressLine2=confirmAddressLine2,
                confirmAddressLine3=confirmAddressLine3,
                confirmPincode=confirmPincode,
                confirmVillage=confirmVillage,
                confirmState=confirmState,
                confirmDistrict=confirmDistrict,
                HouseType=HouseType,
                LandInAcre=LandInAcre,
                NumberofAnimals=NoOfAnimals,
                PovertyLine=PovertyLine,
                BankName=BankName,
                BankAccountNo=BankAccountNo,
                ConfirmBankAccountNo=ConfirmbankAccountNo,
                BankIFSCCode=BankIFSCcode,
                ConfirmBankIFSCCode=ConfirmbankIFSCcode,
                BranchName= Branch,
                CenterId=CenterId,
                CategoryType=CategoryType,
                ProductCategory=productCategory,
                Product=Product,
                PurposeId=PurposeId,
                LoanAmount=LoanAmount,
                InterestRate=IntRate,
                RepayFrequency=RepayFreq,
                GroupName=GroupName,
                CoInsurerRelation=CoInsurerRelation,
                CoInsurerName=CoInsurerName,
                CoOccupation=CoOccupation,
                CoInsurerDOB=CoInsurerdob,
                CoInsurerAge=CoInsurerage,
                KYCIDType=CokycIdType,
                KYCID=KycId,
                RemarkComments=RemarkComments,
            )
            data2.save()
            customerKYCData = Loan_Application_Details.objects.filter(Aadhaar=AadhaarNumber).last()
            messages.success(request, "Customer KYC is submitted successfully")
            return render(request, "successAgentRenderScreen.html", {"customerKYCData": customerKYCData})
    else:
        fm = customerKYCform(request)  # render empty form
    return render(
        request,
        "AgentcustomerKYC.html",
        {
            "form": fm,
            "regno": regno,
        },
    )
    # except Exception:
    #     return render(
    #     request,
    #     "404.html")


# def agentformsubmit(request):
#     loandata = request.session.get("session_id")
#     data = Loan_Application_Details.objects.filter(Aadhaar=loandata)
#     return render(request, "agentformsubmit.html", {"data": data})


def loanDetailsAmount(request):
    if request.method == "GET":
        product = request.GET.get("Product_name")
        loandata = LoanDetails.objects.get(id=product)
        data = {
            "LoanAmount": loandata.LoanAmount,
            "InterestRate": loandata.InterestRate,
            "RepayFrequency": loandata.RepayFrequency,
        }
    return JsonResponse(data)


def TotalAmount(request):
    if request.method == "GET":
        TotalAmount = request.GET.get("TotalAmount")
        data = {"TotalAmount": TotalAmount}
    return JsonResponse(data)


def cashNumber(request):
    if request.method == "GET":
        Amount = request.GET.get("Amount")
        Note = json.loads(Amount)
        try:
            alreadyDayClose = Account_Transaction.objects.get(TransDate__date = Note["branchDayCloseDate"])
            data = {"msg": "Day close already submitted"}
            return JsonResponse(data)
        except Account_Transaction.DoesNotExist:
            Account_Transaction(
                Branch=branch.objects.get(branch_Name=Note["Branch_name"]),
                Credit=Note["Count"],
                Debit=Note["Count"],
                AccountBalance=Note["Count"],
                TransDate = Note["branchDayCloseDate"]
            ).save()
            Trans_ID = Account_Transaction.objects.all().aggregate(Max("id"))
            CashBookReport(
                BranchDayCloseDate = Note["branchDayCloseDate"],
                CashDate = Note["branchDayCloseDate"],
                Branch_Name=branch.objects.get(branch_Name=Note["Branch_name"]),
                TransID=Account_Transaction.objects.get(id=Trans_ID["id__max"]),
                CashBalance=Note["Count"],
                BranchManager=request.user,
                Note2000=Note["Note2000"],
                Note500=Note["Note500"],
                Note200=Note["Note200"],
                Note100=Note["Note100"],
                Note50=Note["Note50"],
                Note20=Note["Note20"],
                Note10=Note["Note10"],
                Note5=Note["Note5"],
                Note2=Note["Note2"],
                Note1=Note["Note1"],
                Coin20=Note["coin20"],
                Coin10=Note["coin10"],
                Coin5=Note["Coin5"],
                Coin2=Note["Coin2"],
                Coin1=Note["Coin1"],
            ).save()
            data = {"Amount": Trans_ID["id__max"]}
        return JsonResponse(data)


def Region_values(request):
    if request.method == "GET":
        Region = request.GET.get("Region")
        Branch = branch.objects.filter(region=Region)
    return render(request, "dropdown_list.html", {"Branch_name": Branch})

def agentDetails(request):
    if request.method == "GET":
        agentID = request.GET.get("agent_ID")
        agentDetail = User.objects.filter(id=agentID)
        serialized_data = UserModelSerializer(agentDetail, many=True).data
    return JsonResponse(serialized_data, safe=False)
      
    


def Preclosure_Amount(request):
    amount = 0
    pre_closure_Amount = 0
    if request.method == "GET":
        cust_Id = request.GET.get("cust_Id")
        LoanIDs = customerKYC.objects.filter(
            loandata__customerId=cust_Id, status__id=41
        )
        totalLoanAmount = customerKYC.objects.get(
            loandata__customerId=cust_Id, status__id=40
        )
        for LoanID in LoanIDs:
            amount = amount + LoanID.LoanAmount
            no_EMI_Pay = loanEMI.objects.filter(
                loanId__loanId=LoanID.loandata.loanId, emiStatus__id=1
            )
            preclosureAmounts = loanEMI.objects.filter(
                loanId__loanId=LoanID.loandata.loanId, emiStatus__id=2
            ).first()
            if not no_EMI_Pay:
                pre_closure_Amount = pre_closure_Amount + LoanID.LoanAmount

            else:
                pre_closure_Amount = (
                    pre_closure_Amount + preclosureAmounts.outstandingPrincipal
                )
        data = {
            "preclosureAmount": pre_closure_Amount,
            "amount": totalLoanAmount.LoanAmount,
        }

        return JsonResponse(data)

        #     data = serializers.serialize('json', [preclosureAmount], many=True)
        #     struct = json.loads(data)
        #     data = json.dumps(struct)
        # return HttpResponse(data, content_type ='application/json')


def Branch_values(request):
    if request.method == "GET":
        Loan = request.GET.get("loan_data")
        Center = center.objects.filter(branch_Name=Loan).order_by("center_Id")
    return render(request, "dropdown_list.html", {"center_ids": Center})


def csoName(request):
    if request.method == "GET":
        branch = request.GET.get("branchID")
        cso_Name = userWithRole.objects.filter(branchName__id=branch,user_role__id = 1)
    return render(request, "dropdown_list.html", {"cso_Name": cso_Name})


def Customer_data(request):
    if request.method == "GET":
        cust_data = request.GET.get("customer_data")
        try:
            Customer_data = customerKYC.objects.filter(Aadhaar=cust_data).first()
            data = {
                "Customer_data": Customer_data.Aadhaar,
                "VoterCard": Customer_data.VoterCard,
                "FirstName": Customer_data.FirstName,
                "LastName": Customer_data.LastName,
                "Age": Customer_data.Age,
                "MaritalStatus": Customer_data.MaritalStatus.id,
                "Gender": Customer_data.Gender.id,
                "DateOfBirth": Customer_data.DateOfBirth,
            }
            # return render(request,'Aadhar_customer_record.html',{"Customer_data": Customer_data})
        except:
            data = {"Customer_data": -1}
        return JsonResponse(data)


def loanApplication(request):
    """
    This function is for getting the data from customer kyc table . only pending and Approved status customers.
    """
    Region = region.objects.all()
    role = Group.objects.get(name='Branch Manager')
    Branch = userWithRole.objects.get(userName=request.user)
    # CenterID = Center_ID.objects.all()
    Center_Id = None
    ApplicationNo = None
    Branch_Name = None
    if request.method == "POST":
        role = Group.objects.get(name='Branch Manager')
        Branch = userWithRole.objects.get(userName=request.user)
        Branch_Name = request.POST.get("branch")
        Center_Id = request.POST.get("centerID")
        fromDate = request.POST.get("fromDate")
        toDate = request.POST.get("toDate")
        ApplicationNo = request.POST.get("applicationNumber")
        try:
            if Branch_Name and fromDate and toDate:
                customer_data = customerKYC.objects.filter(
                    BranchName__branchName__id=Branch_Name,
                    Timestamp__date__range=[fromDate, toDate],
                ).exclude(Q(status=39) | Q(status=41))
            elif Branch_Name and Center_Id and fromDate and toDate:
                customer_data = customerKYC.objects.filter(
                    BranchName__branchName__id=Branch_Name,
                    CenterId__id=Center_Id,Timestamp__date__range=(fromDate, toDate),
                ).exclude(Q(status=39) | Q(status=41))
            elif Branch_Name and Center_Id or ApplicationNo:
                customer_data = customerKYC.objects.filter(
                    Q(BranchName__branchName__id=Branch_Name, CenterId__id=Center_Id)
                    ^ Q(loandata__Application_No=ApplicationNo)
                ).exclude(Q(status=39) | Q(status=41))
        except:
            customer_data = None
        context = {
            "Region": Region,
            "customer_data": customer_data,
            "Branch": Branch,
            "role":role
        }
    else:
        context = {
            "Region": Region,
            "Branch": Branch,
            # "CenterID": CenterID,
            "role":role
        }

    return render(request, "loanApplication.html", context)


def cutomer_data(request, id):  # customer data for branch manager
    """
    this function for approved or rejected kyc and save the customer data to according tables.
    """
    custoner_data = customerKYC.objects.filter(id=id)
    # cust_data = customerKYC.objects.get(id=id)
    # preclosureAmount = loanEMI.objects.filter(
    #     loanId__loanId=cust_data.loandata.customerId, emiStatus__id=2
    # ).first()
    Disbursement_Mode = DisbursementMode.objects.all()
    role = Group.objects.get(name='Branch Manager')
    group_data = GroupName.objects.all().order_by("GroupName_value")
    status_data = (
        form_STATUS.objects.all()
        .order_by("form_STATUS_value")
        .exclude(Q(id=40) | Q(id=41))
    )
    user = request.user
    pre_closure_Amount = 0
    for data in custoner_data:
        LoanIDs = customerKYC.objects.filter(
            loandata__customerId=data.loandata.customerId, status__id=41
        )
        for LoanID in LoanIDs:
            # amount = amount +  LoanID.LoanAmount
            no_EMI_Pay = loanEMI.objects.filter(
                loanId__loanId=LoanID.loandata.loanId, emiStatus__id=1
            )
            preclosureAmounts = loanEMI.objects.filter(
                loanId__loanId=LoanID.loandata.loanId, emiStatus__id=2
            ).first()
            if not no_EMI_Pay:
                pre_closure_Amount = pre_closure_Amount + LoanID.LoanAmount

            else:
                pre_closure_Amount = (
                    pre_closure_Amount + preclosureAmounts.outstandingPrincipal
                )
        LPF = int(data.LoanAmount) * (data.Product.loanProcessingFee)
        LPC = int(data.LoanAmount) * (data.Product.loanProcessingCharge)
        payment_amount = int(data.LoanAmount) - (LPF + LPC)
        dist = Dist.objects.get(id=data.District)
        conf_dist = Dist.objects.get(id=data.confirmDistrict)
    if request.method == "POST":
        AadhaarNumber = request.POST.get("Aadhaar")
        Status = int(request.POST.get("Status"))
        # Application_No = request.POST.get("Application_No")
        VoterCard = request.POST.get("VoterCard")
        custimg = request.POST.get("Custimage")
        Member_Aadhar_Card_front = data.Member_Aadhar_Card_front
        Member_Aadhar_Card_back = data.Member_Aadhar_Card_back
        Member_Voter_Card_front = data.Member_Voter_Card_front
        Member_Voter_Card_back = data.Member_Voter_Card_back
        Co_Insurer_Aadhaar_front = data.Co_Insurer_Aadhaar_front
        Co_Insurer_Aadhaar_back = data.Co_Insurer_Aadhaar_back
        Member_Bank_Details = data.Member_Bank_Details
        Member_Relationship_Proof = data.Member_Relationship_Proof
        FirstName = request.POST.get("FirstName")
        LastName = request.POST.get("LastName")
        DateOfBirth = request.POST.get("DateOfBirth")
        Age = request.POST.get("Age")
        FsName = request.POST.get("FSName")
        FsDOB = request.POST.get("FSDateOfBirth")
        FsAdhaar = request.POST.get("FSAdhaar")
        MotherName = request.POST.get("MothersName")
        Occupation = request.POST.get("Occupation")
        PhoneNumber = request.POST.get("PhoneNumber")
        AddLine1 = request.POST.get("AddressLine1")
        AddLine2 = request.POST.get("AddressLine2")
        AddLine3 = request.POST.get("AddressLine3")
        Village = request.POST.get("Village")
        District = request.POST.get("District")
        PinCode = request.POST.get("Pincode")
        confirmAddressLine1 = request.POST.get("confirmAddressLine1")
        confirmAddressLine2 = request.POST.get("confirmAddressLine2")
        confirmAddressLine3 = request.POST.get("confirmAddressLine3")
        confirmVillage = request.POST.get("confirmVillage")
        confirmDistrict = request.POST.get("confirmDistrict")
        confirmPincode = request.POST.get("confirmPincode")
        LandInAcre = request.POST.get("LandInAcre")
        NoOfAnimals = request.POST.get("NumberofAnimals")
        BankAccountNo = request.POST.get("BankAccountNo")
        BankIFSCcode = request.POST.get("BankIFSCCode")
        LoanAmount = request.POST.get("LoanAmount")
        branch_Name = request.POST.get("BranchName")
        IntRate = request.POST.get("InterestRate")
        RepayFreq = request.POST.get("RepayFrequency")
        CoInsurerRelation = request.POST.get("CoInsurerRelation")
        CoInsurerName = request.POST.get("CoInsurerName")
        CoOccupation = request.POST.get("CoOccupation")
        CoInsurerdob = request.POST.get("CoInsurerDOB")
        CoInsurerage = request.POST.get("CoInsurerAge")
        KycId = request.POST.get("KYCID")
        RemarkComments = request.POST.get("RemarkComments")
        loan_data = Loan_Application_Details.objects.filter(
            Aadhaar=AadhaarNumber
        ).last()
        Payment_Mode = request.POST.get("Disbursement_Payment_Mode")
        if Status == 38:
            approved_appilaction_data = approved_customer_kyc(
                user=user,
                # status = status,
                loandata=loan_data,
                Aadhaar=AadhaarNumber,
                VoterCard=VoterCard,
                OtherKYCIdtype=data.OtherKYCIdtype,
                OtherKYCId=data.OtherKYCId,
                Custimage=custimg,
                Member_Aadhar_Card_front=Member_Aadhar_Card_front,
                Member_Aadhar_Card_back=Member_Aadhar_Card_back,
                Member_Voter_Card_front=Member_Voter_Card_front,
                Member_Voter_Card_back=Member_Voter_Card_back,
                Co_Insurer_Aadhaar_front=Co_Insurer_Aadhaar_front,
                Co_Insurer_Aadhaar_back=Co_Insurer_Aadhaar_back,
                Member_Bank_Details=Member_Bank_Details,
                Member_Relationship_Proof=Member_Relationship_Proof,
                FirstName=FirstName,
                LastName=LastName,
                Gender=data.Gender,
                DateOfBirth=DateOfBirth,
                Age=Age,
                MaritalStatus=data.MaritalStatus,
                FSName=FsName,
                FSType=data.FSType,
                FSDateOfBirth=FsDOB,
                MothersName=MotherName,
                FSAdhaar=FsAdhaar,
                Caste=data.Caste,
                Religion=data.Religion,
                Qualification=data.Qualification,
                Occupation=Occupation,
                PhoneNumber=PhoneNumber,
                AddressLine1=AddLine1,
                AddressLine2=AddLine2,
                AddressLine3=AddLine3,
                PreferredLanguage=data.PreferredLanguage,
                Village=Village,
                District=District,
                State=data.State,
                Pincode=PinCode,
                confirmAddressLine1=confirmAddressLine1,
                confirmAddressLine2=confirmAddressLine2,
                confirmAddressLine3=confirmAddressLine3,
                confirmPincode=confirmPincode,
                confirmVillage=confirmVillage,
                confirmState=data.confirmState,
                confirmDistrict=confirmDistrict,
                HouseType=data.HouseType,
                LandInAcre=LandInAcre,
                NumberofAnimals=NoOfAnimals,
                PovertyLine=data.PovertyLine,
                BankName=data.BankName,
                BankAccountNo=BankAccountNo,
                # ConfirmBankAccountNo=ConfirmbankAccountNo,
                BankIFSCCode=BankIFSCcode,
                # ConfirmBankIFSCCode=ConfirmbankIFSCcode,
                BranchName=userWithRole.objects.get(branchName=branch_Name,userName =data.BranchName.userName),
                CenterId=center.objects.get(center_Id=data.CenterId.center_Id),
                CategoryType=data.CategoryType,
                ProductCategory=data.ProductCategory,
                Product=data.Product,
                PurposeId=data.PurposeId,
                LoanAmount=LoanAmount,
                InterestRate=IntRate,
                RepayFrequency=RepayFreq,
                GroupName=data.GroupName,
                CoInsurerRelation=CoInsurerRelation,
                CoInsurerName=CoInsurerName,
                CoOccupation=CoOccupation,
                CoInsurerDOB=CoInsurerdob,
                CoInsurerAge=CoInsurerage,
                KYCIDType=data.KYCIDType,
                KYCID=KycId,
                RemarkComments=RemarkComments,
                Disbursement_Payment_Mode=DisbursementMode.objects.get(id=Payment_Mode),
                Loan_Cycle=len(
                    Loan_Application_Details.objects.filter(Aadhaar=AadhaarNumber)
                ),
            )
            try:
                rejected_appilaction = rejected_customer_kyc.objects.get(
                    loandata__loanId=loan_data.loanId
                )
                rejected_appilaction.status.id == 39
                messages.success(request, "This form is rejected please apply another Loan")
                # return render(request, "successRenderScreen.html")
                return redirect('successRenderScreen')
            except rejected_customer_kyc.DoesNotExist:
                inst = customerKYC.objects.get(loandata__loanId=loan_data.loanId)
                inst.status = form_STATUS.objects.get(id=Status)
                inst.save()
            try:
                already_approved_customer_kyc = approved_customer_kyc.objects.get(
                    Aadhaar=AadhaarNumber
                )
                messages.success(request, "This Form Already Approved")
                return redirect('successRenderScreen')
                # return render(
                #     request, "successRenderScreen.html"
                # )
            except approved_customer_kyc.DoesNotExist:
                approved_appilaction_data.save()
                messages.success(request, "Loan is Approved is successfully")
                # return render(request, "successRenderScreen.html")
                return redirect('successRenderScreen')
        elif Status == 39:
            rejected_appilaction_data = rejected_customer_kyc(
                user=user,
                # Application_No=Application_No,
                loandata=loan_data,
                Aadhaar=AadhaarNumber,
                VoterCard=VoterCard,
                OtherKYCIdtype=data.OtherKYCIdtype,
                OtherKYCId=data.OtherKYCId,
                Custimage=custimg,
                Member_Aadhar_Card_front=Member_Aadhar_Card_front,
                Member_Aadhar_Card_back=Member_Aadhar_Card_back,
                Member_Voter_Card_front=Member_Voter_Card_front,
                Member_Voter_Card_back=Member_Voter_Card_back,
                Co_Insurer_Aadhaar_front=Co_Insurer_Aadhaar_front,
                Co_Insurer_Aadhaar_back=Co_Insurer_Aadhaar_back,
                Member_Bank_Details=Member_Bank_Details,
                Member_Relationship_Proof=Member_Relationship_Proof,
                FirstName=FirstName,
                LastName=LastName,
                Gender=data.Gender,
                DateOfBirth=DateOfBirth,
                Age=Age,
                MaritalStatus=data.MaritalStatus,
                FSName=FsName,
                FSType=data.FSType,
                FSDateOfBirth=FsDOB,
                MothersName=MotherName,
                FSAdhaar=FsAdhaar,
                Caste=data.Caste,
                Religion=data.Religion,
                Qualification=data.Qualification,
                Occupation=Occupation,
                PhoneNumber=PhoneNumber,
                AddressLine1=AddLine1,
                AddressLine2=AddLine2,
                AddressLine3=AddLine3,
                PreferredLanguage=data.PreferredLanguage,
                Village=Village,
                District=District,
                State=data.State,
                Pincode=PinCode,
                confirmAddressLine1=confirmAddressLine1,
                confirmAddressLine2=confirmAddressLine2,
                confirmAddressLine3=confirmAddressLine3,
                confirmPincode=confirmPincode,
                confirmVillage=confirmVillage,
                confirmState=data.confirmState,
                confirmDistrict=confirmDistrict,
                HouseType=data.HouseType,
                LandInAcre=LandInAcre,
                NumberofAnimals=NoOfAnimals,
                PovertyLine=data.PovertyLine,
                BankName=data.BankName,
                BankAccountNo=BankAccountNo,
                # ConfirmBankAccountNo=ConfirmbankAccountNo,
                BankIFSCCode=BankIFSCcode,
                # ConfirmBankIFSCCode=ConfirmbankIFSCcode,
                BranchName=userWithRole.objects.get(branchName=branch_Name,userName =data.BranchName.userName),
                CenterId=center.objects.get(center_Id=data.CenterId.center_Id),
                CategoryType=data.CategoryType,
                ProductCategory=data.ProductCategory,
                Product=data.Product,
                PurposeId=data.PurposeId,
                LoanAmount=LoanAmount,
                InterestRate=IntRate,
                RepayFrequency=RepayFreq,
                GroupName=data.GroupName,
                CoInsurerRelation=CoInsurerRelation,
                CoInsurerName=CoInsurerName,
                CoOccupation=CoOccupation,
                CoInsurerDOB=CoInsurerdob,
                CoInsurerAge=CoInsurerage,
                KYCIDType=data.KYCIDType,
                KYCID=KycId,
                RemarkComments=RemarkComments,
                # Disbursement_Payment_Mode=DisbursementMode.objects.get(id=Payment_Mode),
            )
            try:
                Approved_form = approved_customer_kyc.objects.get(
                loandata__loanId=loan_data.loanId
                )
                Approved_form.delete() # need some dicussion on this function
            except approved_customer_kyc.DoesNotExist:
                rejected_appilaction_data.save()
                inst = customerKYC.objects.get(loandata__loanId=loan_data.loanId)
                inst.status = form_STATUS.objects.get(id=Status)
                inst.save()
                messages.error(request, "Loan Application Form is successfully Rejected")
                return redirect('successRenderScreen')
                # return render(request, "successRenderScreen.html")
    context = {
        "LPF": LPF,
        "LPC": LPC,
        "preclosureAmount": pre_closure_Amount,
        "payment_amount": payment_amount,
        "custoner_data": custoner_data,
        "group_data": group_data,
        "conf_dist": conf_dist,
        "dist": dist,
        "status_data": status_data,
        "Disbursement_Mode": Disbursement_Mode,
        "role":role
    }
    return render(request, "loanapplicationform.html", context)


def Goup_loan_applications(request, center_Id, groupName):
    """
    This function is for creating grup loan agreement
    """
    customer_data = approved_customer_kyc.objects.filter(
        CenterId__center_Id=center_Id, GroupName__GroupName_value=groupName
    )
    loan_amount = []
    LPC_amount = []
    for cust_data in customer_data:
        loan_amount.append(int(cust_data.LoanAmount))
        LPC_amount.append((cust_data.LPC()))
        center_meeting_day = calendar.day_name[
            (
                cust_data.Timestamp.date()
                + timedelta(days=cust_data.Product.loanMode.loan_days)
            ).weekday()
        ]
        Region = cust_data.BranchName.branchName.region.region
        datetime = cust_data.Timestamp
        repay = cust_data.Product.loanMode.loan_days
        centerid = cust_data.CenterId.center_Id
        center = cust_data.CenterId.center_name
        group = cust_data.GroupName.GroupName_value
        branch = cust_data.BranchName.branchName.branch_Name
    Total_loan_amount = sum(loan_amount)
    Total_LPC_amount = sum(LPC_amount)
    template_path = "groupLoanApplications.html"
    tmpJson = customerDataSerializer(customer_data, many=True)
    # json_data = JSONRenderer().render(tmpJson.data)
    # json_data = json.dumps(tmpJson.data)
    # tmpObj = json.loads(tmpJson.data)
    # tmpJson=json.dumps(tmpJson)

    context = {
        "center_meeting_day": center_meeting_day,
        "Total_LPC_amount": Total_LPC_amount,
        "Total_loan_amount": Total_loan_amount,
        "Region": Region,
        "customer_data": customer_data,
        "group": group,
        "centerid": centerid,
        "center": center,
        "branch": branch,
        "datetime": datetime,
        "repay": repay,
        "data": tmpJson.data,
    }
    return render(request, "groupLoanApplications.html", context)
    # # Create a Django response object, and specify content_type as pdf
    # response = HttpResponse(content_type="application/pdf")
    # response["Content-Disposition"] = 'filename="Order.pdf"'
    # # find the template and render it.
    # template = get_template(template_path)
    # html = template.render(context)
    # # create a pdf
    # pisa_status = pisa.pisaDocument(html.encode("ISO-8859-1"), dest=response)
    # # if error then show some funny view
    # if pisa_status.err:
    #     return HttpResponse(f"We had some errors <pre>{html}</pre>")
    # return response


def GroupLoanApplicationReport(request):
    Region = region.objects.all()
    Groupname = GroupName.objects.all().order_by("GroupName_value")
    role = Group.objects.get(name='Branch Manager')
    managerBranch = userWithRole.objects.get(userName=request.user)
    customer_data = None
    if request.method == "POST":
        Branch_Name = request.POST.get("branch")
        Center_Id = request.POST.get("centerID")
        Group_Name = request.POST.get("Group_Name")
        applicationDate = request.POST.get("applicationDate")
        try:
            if Branch_Name and Center_Id and applicationDate:
                customer_data = approved_customer_kyc.objects.filter(
                    BranchName__branchName__id=Branch_Name,
                    CenterId__id=Center_Id,
                    Timestamp__date=applicationDate,
                )
            elif Branch_Name and Center_Id and Group_Name:
                customer_data = approved_customer_kyc.objects.filter(
                    BranchName__branchName__id=Branch_Name,
                    CenterId__id=Center_Id,
                    GroupName__id=Group_Name,
                )
            elif Branch_Name and Center_Id:
                customer_data = approved_customer_kyc.objects.filter(
                    BranchName__branchName__id=Branch_Name, CenterId__id=Center_Id
                )
        except:
            customer_data = None
        context = {
            "Region": Region,
            "customer_data": customer_data,
            'role':role,
            'managerBranch':managerBranch
        }
    else:
        context = {
            "Region": Region,
            "GroupName": Groupname,
            'role':role,
            'managerBranch':managerBranch
        }

    return render(request, "Group_Loan_Application_Report.html", context)


def Collection_demand(request):
    Region = region.objects.all()
    Groupname = GroupName.objects.all().order_by("GroupName_value")
    role = Group.objects.get(name='Branch Manager')
    managerBranch = userWithRole.objects.get(userName=request.user)
    [loanIds , customer_data , grouped_queryset]= [None , None , None]
    userLoanIdList = []
    if request.method == "POST":
        role = Group.objects.get(name='Branch Manager')
        managerBranch = userWithRole.objects.get(userName=request.user)
        Branch_Name = request.POST.get("branch")
        Center_Id = request.POST.get("centerID")
        CSO_Name = request.POST.get("CSO_Name")
        Demand_Date = request.POST.get("Demand_Date")
        try:
            if Branch_Name and not Center_Id  and not CSO_Name:
                loanIds = loanEMI.objects.filter(center__branch_Name__id = Branch_Name,installmentDate__date = Demand_Date).exclude(emiStatus__id = 1)
                for id in loanIds:
                    userLoanIdList.append(id.loanId.loanId)
                customer_data = disbursement_customer_kyc.objects.filter(
                    loandata__loanId__in = userLoanIdList
                ).exclude(status__id = 42)
                grouped_queryset = customer_data.values('CenterId__center_Id').annotate(count=models.Count('CenterId__center_Id')).annotate(totalSumInstallment=Sum('CustomerEMI__installmentAmount'))
            elif Branch_Name and Center_Id  and not CSO_Name:
                loanIds = loanEMI.objects.filter(center__branch_Name__id = Branch_Name,center__id = Center_Id,installmentDate__date = Demand_Date).exclude(emiStatus__id = 1)
                for id in loanIds:
                    userLoanIdList.append(id.loanId.loanId)
                customer_data = disbursement_customer_kyc.objects.filter(
                    loandata__loanId__in = userLoanIdList
                ).exclude(status__id = 42)
                grouped_queryset = customer_data.values('CenterId__center_Id').annotate(count=models.Count('CenterId__center_Id')).annotate(totalSumInstallment=Sum('CustomerEMI__installmentAmount'))
            elif Branch_Name and CSO_Name and not Center_Id:
                loanIds = loanEMI.objects.filter(center__branch_Name__id = Branch_Name,center__agents_Name__id = CSO_Name,installmentDate__date = Demand_Date).exclude(emiStatus__id = 1)
                for id in loanIds:
                    userLoanIdList.append(id.loanId.loanId)
                customer_data = disbursement_customer_kyc.objects.filter(
                    loandata__loanId__in = userLoanIdList
                ).exclude(status__id = 42)
                grouped_queryset = customer_data.values('CenterId__center_Id').annotate(count=models.Count('CenterId__center_Id')).annotate(totalSumInstallment=Sum('CustomerEMI__installmentAmount'))
        except:
            customer_data = None
        context = {"Region": Region, "customer_data": customer_data,
            'role':role,
            "grouped_queryset":grouped_queryset,
            "Demand_Date":Demand_Date,
            'managerBranch':managerBranch}
    else:
        context = {
            "Region": Region,
            "GroupName": Groupname,
            'role':role,
            'managerBranch':managerBranch
        }

    return render(request, "Collection_demand.html", context)

def editLoanData(request):
    if request.method == "GET":
        loanID = request.GET.get("loanID")
        if loanID:
            loanData = LoanDetails.objects.get(id = loanID)
            serialized_data = editLoanSerializer(loanData).data
    return JsonResponse(serialized_data, safe=False)
      
def updateLoanData(request):
    if request.method == "GET":
        loanID = request.GET.get("loanID")
        loanData = LoanDetails.objects.get(id = loanID)
        if loanData.activateStatus == True:
            loanData.activateStatus = False
        else:
            loanData.activateStatus = True
        loanData.save()
        data = {
            "Success" : True,
            "loanActivateStatus" : loanData.activateStatus,
        }
    return JsonResponse(data)

            

def Approved_Customer_data(request):
    if request.method == "GET":
        customer_data = request.GET.get("customer_data")
        cust_data = customerKYC.objects.get(loandata__loanId=customer_data)
        data = {"kycIdType": cust_data.OtherKYCIdtype, "Gender": str(cust_data.Gender)}
    return JsonResponse(data)


def dist_data(request):
    if request.method == "GET":
        dist_data = request.GET.get("dist_data")
        Dist_list = Dist.objects.filter(State_id=dist_data)
    return render(request, "dist_list.html", {"Dist_list": Dist_list})


def update_dist_data(request):
    if request.method == "GET":
        dist_data = request.GET.get("dist_data")
        Dist_list = Dist.objects.filter(State_id__state_Name=dist_data)
    return render(request, "dist_list.html", {"Dist_list": Dist_list})


def confirm_dist_data(request):
    if request.method == "GET":
        dist_data = request.GET.get("dist_data")
        Dist_list = Dist.objects.get(id=dist_data)
        data = {"Dist_list": Dist_list.Dist_Name, "Dist_id": Dist_list.id}
    return JsonResponse(data)

def clear_session(request):
    # request.session.clear()
    del request.session['branchID']
    del request.session['centerID']
    return JsonResponse({'status': 'success'})

def Loan_Details(request):
    Region = region.objects.all()
    role = Group.objects.get(name='Branch Manager')
    managerBranch = userWithRole.objects.get(userName=request.user)
    Branch = branch.objects.all()
    customer_data = None
    if request.method == "POST":
        role = Group.objects.get(name='Branch Manager')
        managerBranch = userWithRole.objects.get(userName=request.user)
        Branch_Name = request.POST.get("branch")
        Center_Id = request.POST.get("centerID")
        ApplicationNo = request.POST.get("applicationNumber")
        applicationFromDate = request.POST.get("applicationFromDate")
        applicationToDate = request.POST.get("applicationToDate")
        request.session["branchID"] = Branch_Name
        request.session["centerID"] = Center_Id
        try:
            if Branch_Name and applicationFromDate and applicationToDate:
                customer_data = disbursement_customer_kyc.objects.filter(
                    BranchName__branchName__id=Branch_Name,
                    Timestamp__date__range=[applicationFromDate, applicationToDate],
                ).exclude(status__id = 42)
            elif Branch_Name and Center_Id or ApplicationNo:
                customer_data = disbursement_customer_kyc.objects.filter(
                    Q(BranchName__branchName__id=Branch_Name, CenterId__id=Center_Id)
                    ^ Q(loandata__Application_No=ApplicationNo)
                ).exclude(status__id = 42)
        except:
            customer_data = None
        context = {
            "Region": Region,
            "Branch": Branch,
            "customer_data": customer_data
             ,'managerBranch':managerBranch
             ,'role':role ,'managerBranch':managerBranch
        }
    else:
        branchID = request.session.get('branchID', '')
        centerID = request.session.get('centerID', '')
        if branchID and centerID:
            customer_data = disbursement_customer_kyc.objects.filter(
                    BranchName__branchName__id = branchID, CenterId__id = centerID
                )
            
        context = {"Region": Region, "Branch": Branch ,"customer_data": customer_data,'role':role ,'managerBranch':managerBranch}
    return render(request, "Loan_Details.html", context)

def customerAccountStatement(request, id):
    customer_data = disbursement_customer_kyc.objects.get(
        id=id
        )
    allPaidEmi = loanEMI.objects.filter(loanId__loanId = customer_data.loandata.loanId,emiStatus__id__in = [1,4])
    allEmi = loanEMI.objects.filter(loanId__loanId = customer_data.loandata.loanId)
    lastPaidEmai = loanEMI.objects.filter(loanId__loanId = customer_data.loandata.loanId,emiStatus__id = 1).first()

    context = {
        "customer_data" : customer_data,
        "lastPaidEmai" : lastPaidEmai,
        "allPaidEmi" : allPaidEmi,
        "allEmi":allEmi,
    }
    return render(request, "accountStatement.html", context)
    # template_path = "accountStatement.html"
    # # Create a Django response object, and specify content_type as pdf
    # response = HttpResponse(content_type="application/pdf")
    # response["Content-Disposition"] = 'filename="Order.pdf"'
    # # find the template and render it.
    # template = get_template(template_path)
    # html = template.render(context)
    # # create a pdf
    # pisa_status = pisa.CreatePDF(html, dest=response)
    # # if error then show some funny view
    # if pisa_status.err:
    #     return HttpResponse(f"We had some errors <pre>{html}</pre>")
    # return response 


def customer_Loan_card(request, id):
    customer_data = disbursement_customer_kyc.objects.get(
        id=id
    )  # this filter must be apply in approved table
    days = 0
    # emi starting date calculator
    customer_emi_starting_date = (
        disbursement_customer_kyc.objects.filter(
            CenterId__center_Id=customer_data.CenterId.center_Id
        )
        .order_by("Timestamp")
        .first()
    )
    if customer_emi_starting_date.CenterId.center_meeting_day < customer_data.Disbursement_Date:
        emi_dates = loanEMI.objects.filter(
            loanId__loanId=customer_emi_starting_date.loandata.loanId
        ).order_by("id")
        for emi_date in emi_dates:
            if emi_date.installmentDate.date() >= customer_data.Disbursement_Date:
                starting_date = emi_date.installmentDate.date() + timedelta(days=int(1))
                data = starting_date
                days = int((starting_date - customer_data.Disbursement_Date).days) / 365
                break
    elif customer_emi_starting_date.CenterId.center_meeting_day > customer_data.Disbursement_Date:
        starting_date = (
            customer_data.CenterId.center_meeting_day 
        )
        days = int((starting_date - customer_data.Disbursement_Date).days) / 365
    else:
        days = int((customer_data.CenterId.center_meeting_day - customer_data.Disbursement_Date).days) / 365
        starting_date = (
            customer_data.CenterId.center_meeting_day
        )  # get loan approved data for loan installments
    first_emi_mode = customer_data.Product.loanMode.loan_days  # loan EMI days
    T = first_emi_mode / 365  # find the terms for emi calculations
    # for cust_data in customer_data:
    # cust_id = customer_data.loandata   # get the customer id
    P = customer_data.Product.LoanAmount  # get the loan amount from appFroved table
    R = customer_data.Product.InterestRate  # get the loan intrestrate from approved table
    # get the loan repay frequency from approved table
    n = customer_data.Product.RepayFrequency
    d = int(customer_data.Product.RepayFrequency)  # convert in to int
    LPF = int(customer_data.Product.LoanAmount ) * float(customer_data.Product.loanProcessingFee)
    LPC = int(customer_data.Product.LoanAmount ) * float(customer_data.Product.loanProcessingCharge)
    payment_amount = int(customer_data.Product.LoanAmount ) - (LPF + LPC)
    # Calculating interest rate per month
    k = R / (12 * 100)  # find the intrest rate per month
    r = k / int(
        customer_data.Product.loanMode.loan_name_value
    )  # intrest rate divided by 2 for bi weekly loan
    # Calculating Equated Monthly Installment (EMI)
    # calculate the final emi of loan
    emi = P * r * ((1 + r) ** n) / ((1 + r) ** n - 1)
    data_list = []  # create empty list for data of loan amount
    intrest_list = []  # create empty list for total intrest calculation
    # P = customer_data.Product.LoanAmount   # get the loan amount from approved table
    # R = customer_data.Product.InterestRate  # get the loan intrestrate from approved table
    extraIntrest = (P * days * R) / 100
    delta = timedelta(
        days=int(customer_data.Product.loanMode.loan_days)
    )  # date delay for biweekly(14 days) , monthly(28 days) , weekly(7 days)
    while P >= 5:
        dataes = starting_date.strftime("%d-%m-%Y")  # date for installments
        starting_date += delta  # add 14 days for biweekly loan installments dates
        data_list.append(starting_date)  # add the date in empty list
        intrest_rate = (
            P * r
        )  # final calculations for intrest rate for loan installments
        data_list.append(intrest_rate)  # add intrest amount  in empty list
        intrest_list.append(intrest_rate)  # add intrest amount  in empty list
        dedect_amount = emi - float(
            intrest_rate
        )  # dedect the intrest rate from emi for principle amount
        # and add above amount in same empty list
        data_list.append(dedect_amount)
        # second principle amount after dedection
        amount = P - float(dedect_amount)
        P = amount
        data_list.extend((P, emi))
    array_data = (np.array(data_list)).reshape(
        d, 5 
    )  # convert list into emprty array and reshape it into (no. of insatllment and 5)
    array_data.flat[-2] = 0
    array_data.flat[4] = array_data.flat[4] + extraIntrest 
    array_data.flat[1] = array_data.flat[1] + extraIntrest
    array_data.flat[-3] = float(array_data.flat[-7])
    array_data.flat[-1] = float(array_data.flat[-4]) + float(array_data.flat[-7])
    # save all emi to loan emi table only first time
    if not loanEMI.objects.filter(loanId=customer_data.loandata):
        for v, x, y, z, a in array_data:
            obj = loanEMI(
                center=customer_data.CenterId,
                loanId=customer_data.loandata,
                installmentDate=v,
                principleAmount=y,
                interestAmoun=x,
                outstandingPrincipal=z,
                installmentAmount=a,
            )
            obj.save()
    inst = disbursement_customer_kyc.objects.get(
        loandata__loanId=customer_data.loandata.loanId
    )
    inst.CustomerEMI = loanEMI.objects.filter(
        loanId__loanId=customer_data.loandata.loanId
    ).first()
    inst.save()
    Total_intrest = sum(intrest_list) + extraIntrest
    context = {
        "cust_data": customer_data,
        "array_data": array_data,
        "dataes": dataes,
        # "days" : f'{extraIntrest}  , {day}',
        "LPF": LPF,
        "LPC": LPC,
        "payment_amount": payment_amount,
        "Total_intrest": Total_intrest,
    }
    return render(request, "Loan_Report_card.html", context)


def member_document(request, id, num):
    try:
        customer_data = customerKYC.objects.get(
            id=id
        )  # this filter must be apply in approved table
    except:
        customer_data = disbursement_customer_kyc.objects.get(
            id=id
        )
    if num == "100":
        template_path = "member_document.html"
        file_name = customer_data.FirstName
    elif num == "101":
        template_path = "member_document.html"
        file_name = f"{customer_data.FirstName}_AadharCard"
    elif num == "102":
        template_path = "member_document.html"
        file_name = f"{customer_data.FirstName}_VoterCard"
    elif num == "103":
        template_path = "member_document.html"
        file_name = f"{customer_data.FirstName}_Co_Insurer_AadhaarCard"
    elif num == "104":
        template_path = "member_document.html"
        file_name = f"{customer_data.FirstName}_memberBankDetails"
    elif num == "105":
        template_path = "member_document.html"
        file_name = f"{customer_data.FirstName}_memberRelationProof"
    elif num == "106":
        customer_group_Loan_Agreement= disbursement_customer_kyc.objects.get(
            id=id
        ).group_Loan_Agreement
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{customer_data.FirstName}__group_Loan_Agreement.pdf"'
        # Write the file content to the response
        response.write(customer_group_Loan_Agreement.read())
        return response
    context = {"customer_data": customer_data,"num" : num}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"filename = {file_name}.pdf"
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return response


def loan_disbursement(request, loanId):
    try:
        customer_data = approved_customer_kyc.objects.get(
            loandata__loanId=loanId
        )  # this filter must be apply in approved table
        if request.method == "POST":
            group_Loan_Agreement = request.FILES.get("inputFile10")
            Disbursement_Date = request.POST.get("Disbursement_Date")
            cust_data = disbursement_customer_kyc(
                user=customer_data.user,
                loandata=customer_data.loandata,
                Aadhaar=customer_data.Aadhaar,
                VoterCard=customer_data.VoterCard,
                OtherKYCIdtype=customer_data.OtherKYCIdtype,
                OtherKYCId=customer_data.OtherKYCId,
                Custimage=customer_data.Custimage,
                Member_Aadhar_Card_front=customer_data.Member_Aadhar_Card_front,
                Member_Aadhar_Card_back=customer_data.Member_Aadhar_Card_back,
                Member_Voter_Card_front=customer_data.Member_Voter_Card_front,
                Member_Voter_Card_back=customer_data.Member_Voter_Card_back,
                Co_Insurer_Aadhaar_front=customer_data.Co_Insurer_Aadhaar_front,
                Co_Insurer_Aadhaar_back=customer_data.Co_Insurer_Aadhaar_back,
                Member_Bank_Details=customer_data.Member_Bank_Details,
                Member_Relationship_Proof=customer_data.Member_Relationship_Proof,
                group_Loan_Agreement=group_Loan_Agreement,
                FirstName=customer_data.FirstName,
                LastName=customer_data.LastName,
                Gender=customer_data.Gender,
                DateOfBirth=customer_data.DateOfBirth,
                Age=customer_data.Age,
                MaritalStatus=customer_data.MaritalStatus,
                FSName=customer_data.FSName,
                FSType=customer_data.FSType,
                FSDateOfBirth=customer_data.FSDateOfBirth,
                MothersName=customer_data.MothersName,
                FSAdhaar=customer_data.FSAdhaar,
                Caste=customer_data.Caste,
                Religion=customer_data.Religion,
                Qualification=customer_data.Qualification,
                Occupation=customer_data.Occupation,
                PhoneNumber=customer_data.PhoneNumber,
                AddressLine1=customer_data.AddressLine1,
                AddressLine2=customer_data.AddressLine2,
                AddressLine3=customer_data.AddressLine3,
                PreferredLanguage=customer_data.PreferredLanguage,
                Village=customer_data.Village,
                District=customer_data.District,
                State=customer_data.State,
                Pincode=customer_data.Pincode,
                confirmAddressLine1=customer_data.confirmAddressLine1,
                confirmAddressLine2=customer_data.confirmAddressLine2,
                confirmAddressLine3=customer_data.confirmAddressLine3,
                confirmPincode=customer_data.confirmPincode,
                confirmVillage=customer_data.confirmVillage,
                confirmState=customer_data.confirmState,
                confirmDistrict=customer_data.confirmDistrict,
                HouseType=customer_data.HouseType,
                LandInAcre=customer_data.LandInAcre,
                NumberofAnimals=customer_data.NumberofAnimals,
                PovertyLine=customer_data.PovertyLine,
                BankName=customer_data.BankName,
                BankAccountNo=customer_data.BankAccountNo,
                # ConfirmBankAccountNo=ConfirmbankAccountNo,
                BankIFSCCode=customer_data.BankIFSCCode, 
                # ConfirmBankIFSCCode=ConfirmbankIFSCcode,   
                BranchName=userWithRole.objects.get(branchName=customer_data.BranchName.branchName,userName =customer_data.BranchName.userName),
                CenterId=center.objects.get(id=customer_data.CenterId.id),
                CategoryType=customer_data.CategoryType,
                ProductCategory=customer_data.ProductCategory,
                Product=customer_data.Product,
                PurposeId=customer_data.PurposeId,
                LoanAmount=customer_data.LoanAmount,
                InterestRate=customer_data.InterestRate,
                RepayFrequency=customer_data.RepayFrequency,
                GroupName=customer_data.GroupName,
                CoInsurerRelation=customer_data.CoInsurerRelation,
                CoInsurerName=customer_data.CoInsurerName,
                CoOccupation=customer_data.CoOccupation,
                CoInsurerDOB=customer_data.CoInsurerDOB,
                CoInsurerAge=customer_data.CoInsurerAge,
                KYCIDType=customer_data.KYCIDType,
                KYCID=customer_data.KYCID,
                RemarkComments=customer_data.RemarkComments,
                Disbursement_Payment_Mode=customer_data.Disbursement_Payment_Mode,
                Disbursement_Date=Disbursement_Date,
            )
            try:
                alreadyDisburseKyc = loanEMI.objects.filter(center__center_Id = customer_data.CenterId.center_Id).first()
            except loanEMI.DoesNotExist:
                if Disbursement_Date > customer_data.CenterId.center_meeting_day:
                    messages.success(request, "Disbursement date must be less than center meeting date")
                    # return render(request, "successRenderScreen.html")
                    return redirect('successRenderScreen')
            approvedKYC = approved_customer_kyc.objects.get(
                loandata__loanId=customer_data.loandata.loanId
            )
            approvedKYC.delete()
            inst = customerKYC.objects.get(
                loandata__loanId=customer_data.loandata.loanId
            )
            inst.status = form_STATUS.objects.get(id=41)
            inst.save()
            cust_data.save()
            messages.success(request, "Loan is disbursed successfully")
            # return render(request, "successRenderScreen.html")
            return redirect('successRenderScreen')
    except:
        messages.error(request, " First approved the Loan after try Loan Disbursed")
        # return render(request, "successRenderScreen.html")
        return redirect('successRenderScreen')

def update_customer_kyc(request, id):
    custoner_data = get_object_or_404(customerKYC, id=id)
    # for dist in custoner_data:
    dist = Dist.objects.get(id = custoner_data.District)
    bankName = BankName.objects.all()
    loanDetails = LoanDetails.objects.filter(activateStatus = True)
    # fm = customerKYCform(request,request.POST, request.FILES , instance=custoner_data)
    if request.method == "POST":
        VoterCard = request.POST.get("VoterCard")
        KycIdType = request.POST.get("OtherKYCIdtype")
        kycId = request.POST.get("OtherKYCId")
        custimg = request.FILES['Custimage']
        # Member_Aadhar_Card_front = request.FILES["Member_Aadhar_Card_front"]
        # Member_Aadhar_Card_back = request.FILES["Member_Aadhar_Card_back"]
        # Member_Voter_Card_front = request.FILES["Member_Voter_Card_front"]
        # Member_Voter_Card_back = request.FILES["Member_Voter_Card_back"]
        # Co_Insurer_Aadhaar_front = request.FILES["Co_Insurer_Aadhaar_front"]
        # Co_Insurer_Aadhaar_back = request.FILES["Co_Insurer_Aadhaar_back"]
        # Member_Bank_Details = request.FILES["Member_Bank_Details"]
        # Member_Relationship_Proof = request.FILE["Member_Relationship_Proof"]
        DateOfBirth = request.POST.get("DateOfBirth")
        Age = request.POST.get("Age")
        FsDOB = request.POST.get("FSDateOfBirth") 
        Bank_Name = request.POST.get("BankName")
        BankAccountNo = request.POST.get("BankAccountNo")
        confirmbankAccountNo = request.POST.get("confirmbankAccountNo")
        BankIFSCcode = request.POST.get("BankIFSCCode")
        confirmbankIFSCcode = request.POST.get("confirmbankIFSCcode")  
        CategoryType = request.POST.get("CategoryType")
        ProductCategory = request.POST.get("ProductCategory")
        Product = request.POST.get("Product")
        custoner_data.VoterCard = VoterCard   
        custoner_data.Custimage = custimg
        # custoner_data.Member_Aadhar_Card_front = Member_Aadhar_Card_front
        # custoner_data.Member_Aadhar_Card_back = Member_Aadhar_Card_back
        # custoner_data.Member_Voter_Card_front = Member_Voter_Card_front
        # custoner_data.Member_Voter_Card_back = Member_Voter_Card_back
        # custoner_data.Co_Insurer_Aadhaar_front = Co_Insurer_Aadhaar_front
        # custoner_data.Co_Insurer_Aadhaar_back = Co_Insurer_Aadhaar_back
        # custoner_data.Member_Bank_Details = Member_Bank_Details
        # custoner_data.Member_Relationship_Proof = Member_Relationship_Proof
        custoner_data.OtherKYCId = kycId
        custoner_data.ConfirmBankIFSCCode = confirmbankIFSCcode
        custoner_data.FSDateOfBirth = FsDOB
        custoner_data.ProductCategory = LoanDetails.objects.get(id = ProductCategory)    
        custoner_data.Product = LoanDetails.objects.get(id = Product)  
        custoner_data.DateOfBirth = DateOfBirth
        custoner_data.Age = Age
        custoner_data.BankName = BankName.objects.get(id = Bank_Name)
        custoner_data.BankAccountNo = BankAccountNo
        custoner_data.ConfirmBankAccountNo = confirmbankAccountNo
        custoner_data.BankIFSCCode = BankIFSCcode
        custoner_data.ConfirmBankIFSCCode = Age
        custoner_data.CategoryType = categoryType.objects.get(id = CategoryType)
        custoner_data.save()
    context = {
        "customer": custoner_data,
        "bankName": bankName,
        "dist":dist,
        "loanDetails" : loanDetails,
        # "form" : fm
    }
    return render(request, "update_customer_kyc.html", context)



def deleteCassBookRecord(request):
    if request.method == "GET":
        accountTransactionId = request.GET.get("accountTransactionId")
        # my_model = get_object_or_404(Account_Transaction,TrasID = Transaction)
        my_model = Account_Transaction.objects.get(TrasID = str(accountTransactionId))
        my_model.delete()
    return JsonResponse({'success': True})

def addCollections(request, id):
    principalArrear = None
    days = None
    emiForUpdate = None
    emiPayMode = None
    nextEmi = None
    preclosureAmount = None
    collectionSequanceNo = 0
    intrest_rate = 0
    precloseLoanAmount = 0
    referer = request.META.get('HTTP_REFERER')
    todayDate = datetime.today().date()
    emiPayMode = EmiPaymentMode.objects.all().order_by("EmiPaymentModeName")
    disbursementMode = DisbursementMode.objects.all().order_by("DisbursementModeName")
    emiCustomerData = disbursement_customer_kyc.objects.get(id=id)
    request.session["loan_id"] = emiCustomerData.loandata.loanId
    emiList = loanEMI.objects.filter(
        loanId__loanId=emiCustomerData.loandata.loanId
    ).exclude(emiStatus__id=2)
    exclude_paid_emi = loanEMI.objects.filter(
        loanId__loanId=emiCustomerData.loandata.loanId
    ).exclude(emiStatus__id=1)
    preclosureAmount = loanEMI.objects.filter(
        loanId__loanId=emiCustomerData.loandata.loanId, emiStatus__id=1
    ).last()
    if preclosureAmount is None:
        preclosureAmount = loanEMI.objects.filter(
        loanId__loanId=emiCustomerData.loandata.loanId, emiStatus__id=2
        ).first()
        precloseLoanAmount = emiCustomerData.LoanAmount
        daysForIntrest = int((datetime.today().date() - emiCustomerData.Disbursement_Date).days) / 365
        intrest_rate = (precloseLoanAmount * daysForIntrest * emiCustomerData.Product.InterestRate) / 100
    else:
        daysForIntrest = int((datetime.today().date() - preclosureAmount.installmentDate.date()).days)
        if daysForIntrest != 0:
            R = emiCustomerData.Product.InterestRate
            k = R / (12 * 100)  # find the intrest rate per month
            r = k / int(
            daysForIntrest
            )
            intrest_rate = (
                (preclosureAmount.outstandingPrincipal) * r
                )
    if preclosureAmount:
        nextEmi = loanEMI.objects.get(id=((preclosureAmount.id) + 1))
        collectionSequanceNo = len(emiList) + 1
    for notPaidEmi in emiList:
        if notPaidEmi.emiStatus.id == 3:
            principalArrear = notPaidEmi
            days = (notPaidEmi.installmentDate.date() - datetime.today().date()).days
    
    context = {
        "emiCustomerData": emiCustomerData,
        "collectionSequanceNo": collectionSequanceNo,
        "preclosureAmount": preclosureAmount,
        "principalArrear": principalArrear,
        "intrest_rate":intrest_rate,
        "loanAmount":precloseLoanAmount,
        "daysForIntrest": daysForIntrest,
        "nextEmi": nextEmi,
        "days": days,
        "data": exclude_paid_emi,
        "emiForUpdate": emiForUpdate,
        "emiPayMode": emiPayMode,
        "disbursementMode": disbursementMode,
        "todayDate":todayDate,
        'referer': referer
    }
    return render(request, "addCollections.html", context)


def addCollectionForm(request, loanID):
    i = 0
    emiList = loanEMI.objects.filter(loanId__loanId=loanID).exclude(emiStatus__id=2)
    exclude_paid_emi = loanEMI.objects.filter(loanId__loanId=loanID).exclude(
        emiStatus__id=1
    )
    maxTransactionId = emiList.aggregate(Max("TransactionId"))
    paidEMI = loanEMI.objects.filter(
        loanId__loanId=loanID,
        TransactionId=maxTransactionId.get("TransactionId__max"),
    ).last()
    if request.method == "POST":
        emiForUpdate = request.POST.get("numberOfEMI")
        Emiamount = request.POST.get("collectedAmount")
        CollectedBy = request.POST.get("collectedBy")
        collection_Pay_Mode = request.POST.get("collectionPayMode")
        number_of_emi = request.POST.get("numberOfEMI")
        CollectionPayType = request.POST.get("CollectionPayType") 
        preclosureAmount = request.POST.get("preclosureAmount")
        Transaction_Id = (
            1001
            if loanEMI.objects.filter(loanId__loanId=loanID, emiStatus__id=1).count()
            == 0
            else loanEMI.objects.filter(
                loanId__loanId=loanID, emiStatus__id=1
            ).aggregate(max=Max("TransactionId"))["max"]
            + 1
        )
        if (
            emiForUpdate
            and Emiamount
            and CollectedBy
            and collection_Pay_Mode
            and number_of_emi
            and Transaction_Id
            and int(CollectionPayType) != 3 
            and preclosureAmount
        ):
            if (
                emiList
                and str(paidEMI.PaymentDate.date() + timedelta(days=1))
                == str(datetime.now().date())
                and paidEMI.emiStatus.id != 3
            ):
                message = "You can submit only one installment on same day"
            else:
                for update_emi_installment in exclude_paid_emi:
                    update_emi_installment.emiStatus = emiStatus.objects.get(id=1)
                    update_emi_installment.TransactionId = Transaction_Id
                    update_emi_installment.emiSubmittedBy = User.objects.get(id=CollectedBy)
                    update_emi_installment.EmiPaymentMode = DisbursementMode.objects.get(
                        id=int(collection_Pay_Mode)
                    )
                    message = "EMI submitted successfully"
                    update_emi_installment.save()
                    i += 1
                    if i == int(number_of_emi):
                        break
        elif(int(CollectionPayType) == 3 ):
            preclosedDisburseLoan = disbursement_customer_kyc.objects.get(loandata__loanId = loanID)
            preclosedDisburseLoan.status = form_STATUS.objects.get(id=42)
            preclosedDisburseLoan.save()
            preClosedLoanDetails = preClosedLoan(
                LoanId = Loan_Application_Details.objects.get(loanId = loanID),
                PreclosedDate = date.today(),
                PreclosedAmount =  int(preclosureAmount),
                TotalPreclosedEmi = exclude_paid_emi.count(),
                TotalEmi = int(exclude_paid_emi.count()) + int(emiList.count()),
            )
            preClosedLoanDetails.save()
            for update_emi_installment in exclude_paid_emi:
                update_emi_installment.emiStatus = emiStatus.objects.get(id=4)
                update_emi_installment.TransactionId = Transaction_Id
                update_emi_installment.PaymentDate = date.today()
                update_emi_installment.emiSubmittedBy = User.objects.get(id=CollectedBy)  
                update_emi_installment.EmiPaymentMode = DisbursementMode.objects.get(
                    id=int(collection_Pay_Mode)
                )
                update_emi_installment.save()
            message = "Loan is Preclosed successfully"
    return render(request, "submit_add_collection.html", {"message": message})


def emiAmount(request):
    if request.method == "GET":
        i = 0
        amount = 0
        no_of_emi = int(request.GET.get("no_of_emi"))
        loanid = request.session.get("loan_id")
        Center = loanEMI.objects.filter(loanId__loanId=loanid).exclude(emiStatus__id=1)
        for emiAmount in Center:
            amount = amount + emiAmount.installmentAmount
            i += 1
            if i == no_of_emi:
                break
    return render(request, "no_of_emi.html", {"amount": amount})


def Bank_Transaction_Deposit(request):
    Branch = branch.objects.all()
    Bank = BankName.objects.get(id =22)
    if request.method == "POST":
        branchName = request.POST.get("branchName")
        accountNumber = request.POST.get("AccountNo")
        transactionsDate = request.POST.get("transactionsDate")
        depositAmount = request.POST.get("depositAmount")
        bankName = request.POST.get("BankName")
        remarks = request.POST.get("remarks")
        BankTransactions(
            TransactionsMode = TransactionsMode.objects.get(id = 1),
            branchName =  branch.objects.get(id = branchName) ,
            BankName =  BankName.objects.get(id = bankName) ,
            AccountNumber = accountNumber,
            TransactionsDate = transactionsDate,
            TransactionsAmount = depositAmount,
            Remarks = remarks
        ).save()
        messages.success(
            request, f"New record is submitted successfully"
            )
        # return render(request, "successRenderScreen.html")
        return redirect('successRenderScreen')
    context = {"Branch": Branch, "Bank": Bank}
    return render(request, "Bank_Transaction_Deposit.html", context)


def BANK_Transaction_Withdrawal(request):
    Branch = branch.objects.all()
    Bank = BankName.objects.get(id =22)
    if request.method == "POST":
        branchName = request.POST.get("branchName")
        accountNumber = request.POST.get("AccountNo")
        transactionsDate = request.POST.get("transactionsDate")
        depositAmount = request.POST.get("depositAmount")
        transactionsSlipNumber = request.POST.get("transactionsSlipNumber")
        bankName = request.POST.get("BankName")
        remarks = request.POST.get("remarks")
        BankTransactions(
            TransactionsMode = TransactionsMode.objects.get(id = 2),
            branchName =  branch.objects.get(id = branchName) ,
            BankName =  BankName.objects.get(id = bankName) ,
            AccountNumber = accountNumber,
            TransactionsDate = transactionsDate,
            TransactionsAmount = depositAmount,
            TransactionsSlipNumber = transactionsSlipNumber,
            Remarks = remarks
        ).save()
        messages.success(
            request, f"New record is submitted successfully"
            )
        # return render(request, "successRenderScreen.html")
        return redirect('successRenderScreen')
    context = {"Branch": Branch, "Bank": Bank}
    return render(request, "Bank_Transaction_Withdrawal.html", context)


def data_update(request):
    Data = customerKYC.objects.get(id=114)
    Data.status = form_STATUS.objects.get(id=40)
    # for data in Data:
    #     data.status= form_STATUS.objects.get(id = 40)
    Data.save()
    return HttpResponse("greate job")


# account_sid = "AC977a3ea1f36d34966b529ab32a582a49"
# auth_token = "6c3016381ded8a0a86ec4f38e6eda180"
# client = Client(account_sid, auth_token)


def sendOTP(request):
    # try:
    if request.method == "GET":
        PhoneNumber = int(request.GET.get("Phone_Number"))
        Otp_Count = int(request.GET.get("Otp_Count"))
        otp = "".join(random.choices(string.digits, k=Otp_Count))
        # message = client.messages.create(
        #     to=f"+918851202312",  # user's phone number
        #     from_="+15135063207",  # your Twilio phone number
        #     body=f"Your OTP is for Demo Purpose in LMS : {otp}",
        # )
        data = {
            "LoanAmount": str(PhoneNumber),
            "OTP": otp,
        }
    return JsonResponse(data)


# except:
#     print()
# return JsonResponse(PhoneNumber)


def generate_pdf(request):
    [PriAmount , bankDeposite ,bankWithdrawalAmount,dayTotal , openingBalance] = [0,0,0,0,0]
    IntAmount = 0
    AmountLPC = 0
    AmountLPF = 0
    LoanAmount = 0
    ClosingBalance = 0
    totalNoteCount = 0
    preclosureEmiAmount = 0
    preCloseIntrestAmount = 0 
    From_Date = None
    BranchName = None
    To_Date = None
    preClosedLoanIdList = []
    preClosedOutstandingPrincipleAmount = []
    userName = request.user
    createdDate = datetime.now().date()
    [
        Note2000,
        Note500,
        Note200,
        Note100,
        Note50,
        Note20,
        Note10,
        Note5,
        Note2,
        Note1,
        Coin20,
        Coin10,
        Coin5,
        Coin2,
        Coin1,
        totalAmount,
    ] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    noteCount = []
    if request.method == "POST":
        Branch_Name = request.POST.get("branch")
        From_Date = request.POST.get("fromDateRange")
        To_Date = request.POST.get("toDateRange")
        datetime_object = datetime.strptime(To_Date, '%Y-%m-%d').date()
        openingBalanceAmount = Account_Transaction.objects.filter(TransDate__date = (datetime_object - timedelta(days=int(1))))
        if openingBalanceAmount:
            for openingBalances in openingBalanceAmount:
                openingBalance = openingBalances.AccountBalance
        else:
            Account_TransactionID =  Account_Transaction.objects.aggregate(max=Max("id"))["max"] - 1
            openingBalances = Account_Transaction.objects.get(id = Account_TransactionID)
            openingBalance = openingBalances.AccountBalance
        EmiData = loanEMI.objects.filter(
            PaymentDate__date__range=(From_Date, To_Date),
            center__branch_Name__id=int(Branch_Name),
            emiStatus__id= 1
        )
        preclosureEmi = loanEMI.objects.filter(
            PaymentDate__date__range=(From_Date, To_Date),
            center__branch_Name__id=int(Branch_Name),
            emiStatus__id = 4
        )
        for preClosedLoanId in preclosureEmi:
            if preClosedLoanId.loanId.loanId not in preClosedLoanIdList:
                preClosedLoanIdList.append(preClosedLoanId.loanId.loanId)
        preClosedEmiData = loanEMI.objects.filter(
            loanId__loanId__in = preClosedLoanIdList,
            emiStatus__id= 1
        ).order_by('-id')
        if preClosedEmiData:
            for preClosedOutstandingPrinciple in preClosedEmiData:
                if preClosedOutstandingPrinciple.loanId.loanId not in preClosedOutstandingPrincipleAmount:
                    preClosedOutstandingPrincipleAmount.append(preClosedOutstandingPrinciple.loanId.loanId)
                    preclosureEmiAmount = preclosureEmiAmount + preClosedOutstandingPrinciple.outstandingPrincipal
                    preCloseIntrestRate = disbursement_customer_kyc.objects.get(loandata__loanId = preClosedOutstandingPrinciple.loanId.loanId)
                    daysForIntrest = abs(int((preClosedOutstandingPrinciple.PaymentDate.date() - datetime.today().date()).days)  / 365)
                    preCloseIntrestAmount = preCloseIntrestAmount + (preClosedOutstandingPrinciple.outstandingPrincipal * daysForIntrest * preCloseIntrestRate.Product.InterestRate) / 100
        else:
            pass # if there is not paied emi 

        loanDisburseAmount = disbursement_customer_kyc.objects.filter(
            Disbursement_Date__range=(From_Date, To_Date),
            BranchName__branchName__id=int(Branch_Name),
            Disbursement_Payment_Mode__id=2,
        )
        depositeAmounts = BankTransactions.objects.filter(
            TransactionsDate__range=(From_Date, To_Date),
            branchName__id=int(Branch_Name),
            TransactionsMode__id=1,  
        )
        withdrawalAmounts = BankTransactions.objects.filter(
            TransactionsDate__range=(From_Date, To_Date),
            branchName__id=int(Branch_Name),
            TransactionsMode__id=2,  
        )
        cashDenomination = CashBookReport.objects.filter(
            BranchDayCloseDate__range=(From_Date, To_Date),
            Branch_Name__id=int(Branch_Name),
        )
        # if EmiData or userData or cashDenomination or withdrawalAmounts or depositeAmounts:
        BranchName = branch.objects.get(id = Branch_Name)
        for cash in cashDenomination:
            Note2000 += cash.Note2000
            Note500 += cash.Note500
            Note200 += cash.Note200
            Note100 += cash.Note100
            Note50 += cash.Note50
            Note20 += cash.Note20
            Note10 += cash.Note10
            Note5 += cash.Note5
            Note2 += cash.Note2
            Note1 += cash.Note1
            Coin20 += cash.Coin20
            Coin10 += cash.Coin10
            Coin5 += cash.Coin5
            Coin2 += cash.Coin2
            Coin1 += cash.Coin1
            totalAmount += cash.CashBalance
        for amount in EmiData:
            PriAmount += amount.principleAmount
            IntAmount += amount.interestAmoun
        PriAmount = PriAmount + preclosureEmiAmount
        IntAmount = IntAmount + preCloseIntrestAmount
        for depositAmount in depositeAmounts:
            bankDeposite += depositAmount.TransactionsAmount
        for withdrawalAmount in withdrawalAmounts:
            bankWithdrawalAmount += withdrawalAmount.TransactionsAmount
        for Charge in loanDisburseAmount:
            AmountLPC += int(Charge.LPC())
            AmountLPF += int(Charge.LPF())
            LoanAmount = Charge.LoanAmount
        ClosingBalance = (PriAmount + IntAmount +  AmountLPC + AmountLPF + bankWithdrawalAmount ) - (
            LoanAmount + bankDeposite
        )
        noteCount.extend(
            (
                Note2000,
                Note500,
                Note200,
                Note100,
                Note50,
                Note20,
                Note10,
                Note5,
                Note2,
                Note1,
                Coin20,
                Coin10,
                Coin5,
                Coin2,
                Coin1,
            )
        )
        for note in range(0, len(noteCount)):
            totalNoteCount = totalNoteCount + noteCount[note]
        dayTotal = PriAmount + IntAmount + AmountLPC + AmountLPF + bankWithdrawalAmount
        ClosingBalance = (PriAmount + IntAmount  + AmountLPC + AmountLPF + bankWithdrawalAmount + openingBalance) - (
        LoanAmount + bankDeposite
        )
        # else:
        #     ClosingBalance = 0
    template_path = "cashBook.html"
    context = {
        "dayTotal":dayTotal,
        "ClosingBalance": ClosingBalance,
        "PriAmount": PriAmount,
        "IntAmount": IntAmount,
        "AmountLPC": AmountLPC,
        "AmountLPF": AmountLPF,
        "LoanAmount": LoanAmount,
        "From_Date": From_Date,
        "To_Date": To_Date,
        "BranchName": BranchName,
        "userName": userName,
        "createdDate": createdDate,
        "noteCount": noteCount,
        "totalNoteCount": totalNoteCount,
        "totalAmount": totalAmount,
        "bankDeposite":bankDeposite,
        "bankWithdrawalAmount":bankWithdrawalAmount,
        "openingBalance":openingBalance
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="Order.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse(f"We had some errors <pre>{html}</pre>")
    return response


def dataUpdate(request):
    data = loanEMI.objects.get(id = 1433)
    data.emiStatus = emiStatus.objects.get(id=2)
    data.save()
    messages.success(
            request, f"First submit day close for existing dates"
            )
    return render(request, "successRenderScreen.html")