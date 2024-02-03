from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,Http404
from . import models



def controller(request,department):
    try:
        dpt=models.Department.objects.get(name=department)
        data=models.PgStudentDetails.objects.order_by('-percentageoptained')
        context={
            'data':data,
            'department':dpt
        }
        return render(request,'controler/listpage.html',context)
    except Exception as e:
        return HttpResponse(e)

def constudent(request,department, userid):
    try:
        data = models.PgStudentDetails.objects.filter(student__username=userid).filter(details_submited=True)
        context = {'data': data}
        return render(request, 'controler/listpage.html', context)
    except models.PgStudentDetails.DoesNotExist:
        raise Http404("Student details not found.")
    except Exception as e:
        # Log the exception for debugging
        # Return a generic error message or redirect to an error page
        return HttpResponse(e)
    
def department(request,department):
    try:
        dpt=models.Department.objects.get(name=department)
        data=models.PgStudentDetails.objects.order_by('-percentageoptained')
        context={
            'data':data,
            'department':dpt
        }
        return render(request,'department/listpage.html',context)
    except Exception as e:
        return HttpResponse(e)
    
def depstudent(request,department, userid):
    try:
        data = models.PgStudentDetails.objects.filter(student__username=userid).filter(details_submited=True)
        context = {'data': data}
        return render(request, 'department/listpage.html', context)
    except models.PgStudentDetails.DoesNotExist:
        raise Http404("Student details not found.")
    except Exception as e:
        # Log the exception for debugging
        # Return a generic error message or redirect to an error page
        return HttpResponse(e)
    

def principal(request):
    try:
        dpt=models.Department.objects.all()
        data=models.PgStudentDetails.objects.order_by('-percentageoptained')
        context={
            'data':data,
            'department':dpt
        }
        return render(request,'principal/listpage.html',context)
    except Exception as e:
        return HttpResponse(e)
    
def pplstudent(request, userid):
    try:
        data = models.PgStudentDetails.objects.filter(student__username=userid).filter(details_submited=True)
        context = {'data': data}
        return render(request, 'department/listpage.html', context)
    except models.PgStudentDetails.DoesNotExist:
        raise Http404("Student details not found.")
    except Exception as e:
        # Return a generic error message or redirect to an error page
        return HttpResponse(e)


