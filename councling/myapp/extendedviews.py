from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,Http404
from . import models
# select department in controler
def deptcontrol(request):
    data=models.Department.objects.all()
    return render(request,'controler/index.html',{'department':data})
#controler profile
def controller(request,department,list):
    com=request.GET.get('cot','').lower()
    try:
        dpt=models.Department.objects.get(name=department)
        if list=='truned up': 
            data=models.PgStudentDetails.objects.filter(status='applied').filter(Department__name=department).order_by('-percentageoptained')
        elif list=='applied':
            data=models.PgStudentDetails.objects.all().filter(Department__name=department).order_by('-percentageoptained')
        elif list=='not turned up':
            data=models.PgStudentDetails.objects.filter(Department__name=department).order_by('-percentageoptained')
        elif list=='selected':
            data=models.PgStudentDetails.objects.filter(Department__name=department).filter(status='department').order_by('-percentageoptained')
        elif list=='rejected':
            data=models.PgStudentDetails.objects.filter(Department__name=department).filter(status='rejected').order_by('-percentageoptained')
        else:
            return Http404("enter the correct url")
        print(com)
        valid_communities = ['mbc', 'bc', 'sc', 'sca','st','bcm']
        if com in valid_communities:
            filtereddata = data.filter(community__iexact=com) 
        else:
            filtereddata = data
    except Exception as e:
        return HttpResponse(e)
    
    context={
        'data':filtereddata,
        'department':dpt
    }
    return render(request,'controler/listpage.html',context)
# controler profile for student
def constudent(request,department,list,userid):
    if request.method=='POST':
        try:
            data = models.PgStudentDetails.objects.get(student__username=userid)
        except models.PgStudentDetails.DoesNotExist:
            raise Http404("Student details not found.")
        if request.POST['action']== 'forward':
            data.status='department'
            data.remark=request.POST.get('remark', '') 
            data.save()
        elif request.POST['action']=='reject':
            data.status='rejected'
            data.remark=request.POST.get('remark', '') 
            data.save()
        return redirect('depcontroler',department=department, list=list)
    else:
        try:
            dpt=models.Department.objects.get(name=department)
            data = models.PgStudentDetails.objects.filter(student__username=userid)
            context = {'data': data,'department':dpt }
        except models.PgStudentDetails.DoesNotExist:
            raise Http404("Student details not found.")
        except Exception as e:
            return HttpResponse(e)
        
        if list=='truned up':    
            return render(request, 'controler/student.html', context)
        elif list=='applied' or list == 'not turned up':
            return render(request, 'controler/student.html', context)
        elif list=='selected' or list == 'rejected':    
            return render(request, 'controler/studentview.html', context)
        else:
            return Http404("enter the correct url")
    
    
# department views
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
# department student views 
def depstudent(request,department, userid):
    try:
        data = models.PgStudentDetails.objects.filter(student__username=userid).filter(details_submited=True)
        context = {'data': data}
        return render(request, 'department/student.html', context)
    except models.PgStudentDetails.DoesNotExist:
        raise Http404("Student details not found.")
    except Exception as e:
        # Log the exception for debugging
        # Return a generic error message or redirect to an error page
        return HttpResponse(e)
    
#principal view
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
#principal view student
def pplstudent(request, userid):
    try:
        data = models.PgStudentDetails.objects.filter(student__username=userid).filter(details_submited=True)
        context = {'data': data}
        return render(request, 'principal/student.html', context)
    except models.PgStudentDetails.DoesNotExist:
        raise Http404("Student details not found.")
    except Exception as e:
        # Return a generic error message or redirect to an error page
        return HttpResponse(e)


