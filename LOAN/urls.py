from django.contrib import admin
from django.urls import path
from LOAN import views
from LOAN.views import MyPasswordResetView
from django.contrib.auth import views as auth_views
from LOAN.forms import LoginForm 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)


urlpatterns = [
    path(
        "BANK_Transaction_Withdrawal/",
        views.BANK_Transaction_Withdrawal,
        name="BANK_Transaction_Withdrawal",
    ),
    path(
        "Bank_Transaction_Deposit/",
        views.Bank_Transaction_Deposit,
        name="Bank_Transaction_Deposit",
    ),
    path("desbord/", views.desbord, name="desbord"),
    path("dataUpdate/", views.dataUpdate),
    path("collection_details/", views.collection_details, name="collection_details"),
    # path("agentformsubmit/", views.agentformsubmit, name="agentformsubmit"),
    path("center_meeting/", views.center_meeting, name="center_meeting"),
    path("addCenterMeeting/", views.addCenterMeeting, name="addCenterMeeting"),
    path("collection_reverse/", views.collection_reverse, name="collection_reverse"),
    path("reverseEMI/<TransactionId>/<loanId>/", views.reverseEMI, name="reverseEMI"),
    path("addCollectionForm/<loanID>/", views.addCollectionForm, name="addCollectionForm"),
    path("editLoanData/", views.editLoanData),
    path(
        "cross_sell_cash_sell/", views.cross_sell_cash_sell, name="cross_sell_cash_sell"
    ),
    path(
        "add_cross_sell_cash_sell/",
        views.add_cross_sell_cash_sell,
        name="add_cross_sell_cash_sell",
    ),
    path("Credit_Bureau_Check/", views.Credit_Bureau_Check, name="Credit_Bureau_Check"),
    path("branchDayClose/", views.branchDayClose, name="branchDayClose"),
    path("disburseCustomerDetails/<id>/", views.disburseCustomerDetails, name="disburseCustomerDetails"),
    path("customerAccountStatement/<id>/", views.customerAccountStatement, name="customerAccountStatement"),
    path("region_view/", views.region_view, name="region_view"),
    path("loan/", views.loan, name="loan"),
    path("updateLoanData/", views.updateLoanData),
    path("loanApplication/", views.loanApplication, name="loanApplication"),
    path("branchSummaryReport/", views.branchSummaryReport, name="branchSummaryReport"),
    # path('', views.home, name='login'),
    path(
        "update_customer_kyc/<id>/",
        views.update_customer_kyc,
        name="update_customer_kyc",
    ),
    path("region/", views.Region_field, name="region"),
    path("newUserRole/", views.newUserRole, name="newUserRole"),
    path("zone_view/", views.zone_view, name="zone_view"),
    path("zone/", views.Zone, name="zone"),
    path("center_ID/", views.center_ID, name="center_ID"),
    path("newLoan/", views.newLoan, name="newLoan"),
    path("Agent/", views.Agents, name="Agent"),
    path("Agent_user/", views.Agent_user, name="Agent_user"),
    path("customerKYC/", views.CustomerKYC, name="customerKYC"),
    path("loanCalculator/", views.loanCalculator, name="loanCalculator"),
    path("generate_pdf/", views.generate_pdf, name="generate_pdf"),
    path("loanDetailsAmount/", views.loanDetailsAmount),
    path("installmentAmountButton/", views.installmentAmountButton),
    path("Branch_values/", views.Branch_values),
    path("csoName/", views.csoName),
    path("emiAmount/", views.emiAmount), 
    path("centerIdDetail/", views.centerIdDetail), 
    path("Region_values/", views.Region_values),
    path("agentDetails/", views.agentDetails),
    path("Preclosure_Amount/", views.Preclosure_Amount),
    path("TotalAmount/", views.TotalAmount),
    path("cashNumber/", views.cashNumber), 
    path("Customer_data/", views.Customer_data),
    path("clear-session/", views.clear_session),
    path("sendOTP/", views.sendOTP),
    path("dist_data/", views.dist_data),
    path("update_dist_data/", views.update_dist_data),
    path("confirm_dist_data/", views.confirm_dist_data),
    path("Approved_Customer_data/", views.Approved_Customer_data),
    path("Collection_demand/", views.Collection_demand, name="Collection_demand"),
    path("data_input/", views.data_update),
    path("AgentCustomer/", views.AgentCustomerKYC, name="AgentCustomerKYC"),
    path(
        "GroupLoanApplicationReport/",
        views.GroupLoanApplicationReport,
        name="Group_Loan_Application_Report",
    ),
    path("Loan_Details/", views.Loan_Details, name="Loan_Details"),
    path("cutomer_data/<id>/", views.cutomer_data),
    path(
        "group_Loan_Application_Report_card/<center_Id>/<groupName>/",
        views.Goup_loan_applications,
        name="Goup_loan_applications",
    ),
    path("customer_Loan_card/<id>/", views.customer_Loan_card),
    path("addCollections/<id>/", views.addCollections),
    path("deleteCassBookRecord/", views.deleteCassBookRecord),
    path("member_document/<id>/<num>/", views.member_document, name="member_document"),
    path("loan_disbursement/<loanId>/", views.loan_disbursement),
    path(
        "",
        auth_views.LoginView.as_view(
            next_page="desbord",
            template_name="../templates/index.html",
            authentication_form=LoginForm,
        ),
        name="signin",
    ),
    path('changePassword/', views.change_password, name='changePassword'),
    path('password-reset/', MyPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('successRenderScreen/', views.successRenderScreen, name='successRenderScreen'),
   
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
