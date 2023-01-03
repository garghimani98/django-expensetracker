from django.shortcuts import render,redirect
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime
# Create your views here.

def index(request):
    
    if request.method=="POST":
        expense=ExpenseForm(data=request.POST)
        if expense.is_valid():
             expense.save()
        
             
    expense_form=ExpenseForm()
    expenses=Expense.objects.all()
    
    #to find the sum of all the expenses we have used below line
    total_expenses=expenses.aggregate(Sum('amount'))
    
    
    #logic to find expenses of  last 1 year etc
    
    last_year=datetime.date.today()-datetime.timedelta(365)
    data=Expense.objects.filter(date__gt=last_year)
    yearly_expense=data.aggregate(Sum('amount'))
    
    #logic to find expenses of  last 1 month etc
    
    last_month=datetime.date.today()-datetime.timedelta(30)
    data=Expense.objects.filter(date__gt=last_month)
    monthly_expense=data.aggregate(Sum('amount'))
    
    
    #logic to find expenses of last 1 week 
    
    last_week=datetime.date.today()-datetime.timedelta(7)
    data=Expense.objects.filter(date__gt=last_week)
    weekly_expense=data.aggregate(Sum('amount'))
    
    
    #logic to calculate total expense on a particular day, we will use annotate function here
    
    daily_sums=Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    
    #logic to calculate total expense on a particular day, we will use annotate function here
    
    categorical_sums=Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    
    
    return render(request,'myapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses,'yearly_expense':yearly_expense,'monthly_expense':monthly_expense,'weekly_expense':weekly_expense,'daily_sums':daily_sums,'categorical_sums':categorical_sums})


def edit(request,id):
    expense=Expense.objects.get(id=id)
    expense_form=ExpenseForm(instance=expense)
    if request.method=="POST":
        expense=Expense.objects.get(id=id)
        expense=ExpenseForm(request.POST,instance=expense)
        if expense.is_valid():
             expense.save()
             return redirect('index')
    return render(request,'myapp/edit.html',{'expense_form':expense_form})



def delete(request,id):
    if request.method=="POST" and 'delete' in request.POST:
        expense=Expense.objects.get(id=id)
        expense.delete()
    return redirect('index')
    