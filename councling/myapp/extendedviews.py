from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,Http404
from . import models
from django.db.models import Q
from . import forms
from django.views.decorators.cache import never_cache
import csv
from . decoraters import group_required
from .utils import sendstatus
# select department in controler
@group_required(['controler'])
def setchange(request,department):
    try:
        data = models.Department.objects.get(name=department)
    except models.Department.DoesNotExist:
        return HttpResponse("You have no data. Please contact the administrator.")
    if request.method == 'POST':
        form = forms.pgsetform(request.POST,  instance=data)
        if form.is_valid():
            form.save()
            return redirect('depcontroler',department=department, list='selected')
    else:
        form = forms.pgsetform(instance=data)
    return render(request, 'controler/seatcontrol.html', {'forms': form})
    
#controler profile
@group_required(['controler'])
def controller(request,department,list):
    com=request.GET.get('cot','').lower()
    try:
        dpt=models.Department.objects.get(name=department)
        if list=='truned up': 
            data=models.PgStudentDetails.objects.filter(status='controler').filter(Department__name=department).filter(details_submited=True).order_by('-percentageoptained')
        elif list=='applied':
            data=models.PgStudentDetails.objects.filter(Department__name=department).order_by('-percentageoptained')
        elif list=='not turned up':
            data=models.PgStudentDetails.objects.filter(Department__name=department).filter(status='applied').order_by('-percentageoptained')
        elif list=='selected':
            data=models.PgStudentDetails.objects.filter(Department__name=department).filter(details_submited=True).filter(status='department').order_by('-percentageoptained')
        elif list=='rejected':
            data=models.PgStudentDetails.objects.filter(Department__name=department).filter(status='rejected').filter(details_submited=True).order_by('-percentageoptained')
        else:
            return HttpResponse("enter the correct url")
        valid_communities = ['mbc', 'bc', 'sc', 'sca','st','bcm']
        if com in valid_communities:
            filtereddata = data.filter(community__iexact=com) 
        else:
            filtereddata = data
    except Exception as e:
        return HttpResponse(e)
    context={
            'data':filtereddata,
            'department':dpt,
            'count':filtereddata.count()
        }
    if request.method=='POST':
        if request.POST['action']=='download':
            response = HttpResponse(content_type='text/csv',headers={'Content-Disposition': 'attachment; filename="report.csv"'},)
            writer = csv.writer(response)
            writer.writerow([list])
            writer.writerow(['application id','name','gender','percentage','community','department'])
            for item in filtereddata:
                writer.writerow([item.student.username, item.name, item.gender,item.percentageoptained,item.community,item.Department.name]) 
            return response
        else:
            return render(request,'controler/listpage.html',context)
    else:
        return render(request,'controler/listpage.html',context)
# controler profile for student
@group_required(['controler'])
def constudent(request,department,list,userid):
    if request.method=='POST':
        try:
            dpt=models.Department.objects.get(name=department)
            data = models.PgStudentDetails.objects.get(student__username=userid)
        except models.PgStudentDetails.DoesNotExist:
            raise Http404("Student details not found.")
        if request.POST['action']== 'forward':
            data.status='department'
            data.remark=request.POST.get('remark', '') 
            if data.community=='bc':
                if dpt.pg_oc >1:
                    data.resevation='oc'
                    dpt.pg_oc-=1
                elif dpt.pg_bc>0:
                    data.resevation='bc'
                    dpt.pg_bc-=1
                else:
                    return HttpResponse('no avalable sets for bc community !')
            elif data.community=='bcm':
                if dpt.pg_oc >1:
                    data.resevation='oc'
                    dpt.pg_oc-=1
                elif dpt.pg_bcm>0:
                    data.resevation='bcm'
                    dpt.pg_bcm-=1
                else:
                    return HttpResponse('no avalable sets for bcm community !')
            elif data.community=='mbc':
                if dpt.pg_oc >1:
                    data.resevation='oc'
                    dpt.pg_oc-=1
                elif dpt.pg_mbc>0:
                    data.resevation='mbc'
                    dpt.pg_mbc-=1
                else:
                    return HttpResponse('no avalable sets for mbc community !')
            elif data.community=='sc':
                if dpt.pg_oc >1:
                    data.resevation='oc'
                    dpt.pg_oc-=1
                elif dpt.pg_sc>0:
                    data.resevation='sc'
                    dpt.pg_sc-=1
                else:
                    return HttpResponse('no avalable sets for sc community !')
            elif data.community=='sca':
                if dpt.pg_oc >1:
                    data.resevation='oc'
                    dpt.pg_oc-=1
                elif dpt.pg_sca>0:
                    data.resevation='sca'
                    dpt.pg_sca-=1
                else:
                    return HttpResponse('no avalable sets for sca community !')
            elif data.community=='st':
                if dpt.pg_oc >1:
                    data.resevation='oc'
                    dpt.pg_oc-=1
                elif dpt.pg_st>0:
                    data.resevation='st'
                    dpt.pg_st-=1
                else:
                    return HttpResponse('no avalable sets for st community !')
            elif dpt.pg_oc==1 and (data.sports=='yes' or data.pysically_chalanged=='yes'):
                data.resevation='ph'
                dpt.pg_oc-=1
            else:
                return HttpResponse('some thing went worng')
            sendstatus(data.student.email,f'your application {data.student.username} has been aproved by controler and forworded to department')
            dpt.save()
            data.save()
        elif request.POST['action']=='reject':
            data.status='rejected'
            data.rejectedBy='controler'
            data.remark=request.POST.get('remark', '') 
            sendstatus(data.student.email,f'your application {data.student.username} has been rejected by controler')
            data.save()
        return redirect('depcontroler',department=department, list=list)
    else:
        try:
            dpt=models.Department.objects.get(name=department)
            data = models.PgStudentDetails.objects.get(student__username=userid)
            context = {'data': data,'department':dpt }
        except models.PgStudentDetails.DoesNotExist:
            raise Http404("Student details not found.")
        except Exception as e:
            return HttpResponse(e)
        
        if list=='truned up':    
            return render(request, 'controler/student.html', context)
        elif list=='applied' or list == 'not turned up':
            return render(request, 'controler/studentview_not_turnedup.html', context)
        elif list=='selected' or list == 'rejected':    
            return render(request, 'controler/studentview.html', context)
        else:
            return Http404("enter the correct url")
    
# department views
@group_required(['department'])
def department(request,department,list):
    com=request.GET.get('cot','').lower()
    try:
        dpt=models.Department.objects.get(name=department)
        if list=='selected': 
            data=models.PgStudentDetails.objects.filter(status='department').filter(Department__name=department).filter(details_submited=True).order_by('-percentageoptained')
        elif list=='admited':
            data=models.PgStudentDetails.objects.filter(status='admited').filter(Department__name=department).filter(details_submited=True).order_by('-percentageoptained')
        elif list=='applied':
            data=models.PgStudentDetails.objects.filter(Department__name=department).order_by('-percentageoptained')
        elif list=='rejected':
            data=models.PgStudentDetails.objects.filter(status='rejected').filter(Department__name=department).filter(details_submited=True).order_by('-percentageoptained')
        else:
            return HttpResponse("enter the correct url")
        
        valid_communities = ['mbc', 'bc', 'sc', 'sca','st','bcm','oc']
        if com in valid_communities:
            if com=='oc':
                filtereddata = data.filter(resevation=(com or 'ph')) 
            else:
                filtereddata = data.filter(resevation=com) 
        else:
            filtereddata = data
    except Exception as e:
        return HttpResponse(e)
    
    context={
            'data':filtereddata,
            'department':dpt,
            'count':filtereddata.count()
        }
    if request.method=='POST':
        if request.POST['action']=='download':
            response = HttpResponse(content_type='text/csv',headers={'Content-Disposition': 'attachment; filename="report.csv"'},)
            writer = csv.writer(response)
            writer.writerow([list])
            writer.writerow(['application id','name','gender','percentage','community','department'])
            for item in filtereddata:
                writer.writerow([item.student.username, item.name, item.gender,item.percentageoptained,item.community,item.Department.name]) 
            return response
        else:
            return render(request,'department/listpage.html',context)
    else:
        return render(request,'department/listpage.html',context)
# department student views 
# @group_required(['department'])
def depstudent(request,department,list,userid):
    if request.method=='POST':
        try:
            dpt=models.Department.objects.get(name=department)
            data = models.PgStudentDetails.objects.get(student__username=userid)
        except models.PgStudentDetails.DoesNotExist:
            raise Http404("Student details not found.")
        if request.POST['action']== 'admit':
            data.status='admited'
            data.remark=request.POST.get('remark', '')   
            sendstatus(data.student.email,f'your application {data.student.username} has been aproved by department you are admited to your collage')
            data.save()
        elif request.POST['action']=='reject':
            data.status='rejected'
            data.rejectedBy='department'
            data.remark=request.POST.get('remark', '') 
            if data.resevation=='oc':
                dpt.pg_oc+=1
            elif data.resevation=='bc':
                dpt.pg_bc+=1
            elif data.resevation=='bcm':
                dpt.pg_bcm+=1
            elif data.resevation=='mbc':
                dpt.pg_mbc+=1
            elif data.resevation=='sc':
                dpt.pg_sc+=1
            elif data.resevation=='sca':
                dpt.pg_sca+=1
            elif data.resevation=='st':
                dpt.pg_st+=1
            sendstatus(data.student.email,f'your application {data.student.username} has been rejected department')
            dpt.save()
            data.save()
        return redirect('department',department=department, list=list)
    else:
        try:
            dpt=models.Department.objects.get(name=department)
            data = models.PgStudentDetails.objects.get(student__username=userid)
            context = {'data': data,'department':dpt }
        except models.PgStudentDetails.DoesNotExist:
            raise HttpResponse("Student details not found.")
        except Exception as e:
            return HttpResponse(e)
        
        if list=='selected':    
            return render(request, 'department/student.html', context)
        elif list=='applied':
            return render(request, 'controler/studentview_not_turnedup.html', context)
        elif list=='rejected' or list == 'admited':
            return render(request, 'department/studentview.html', context)
        else:
            return Http404("enter the correct url")

#principal view
@group_required(['principal'])
def principal(request,list):
    dep = request.GET.get('dep','').lower()
    try:
        dpt = models.Department.objects.all()
        if list == 'admited': 
            data = models.PgStudentDetails.objects.filter(status='admited')
        elif list == 'rejected':
            data = models.PgStudentDetails.objects.filter(status='rejected')
        elif list=='applied':
            data=models.PgStudentDetails.objects.all()
        else:
            return HttpResponse("Enter the correct URL")
        
        if dep == 'all' or dep == '':
            filtered_data = data.order_by('-community')
        else:
            filtered_data = data.filter(Department__name=dep).order_by('-community')
        
    except Exception as e:
        return HttpResponse(e)
    
    context = {
        'data': filtered_data,
        'department': dpt,
        'count':filtered_data.count()
    }
    if request.method=='POST':
        if request.POST['action']=='download':
            response = HttpResponse(content_type='text/csv',headers={'Content-Disposition': 'attachment; filename="report.csv"'},)
            writer = csv.writer(response)
            writer.writerow([list])
            writer.writerow(['application id','name','gender','percentage','community','department'])
            for item in filtered_data:
                writer.writerow([item.student.username, item.name, item.gender,item.percentageoptained,item.community,item.Department.name]) 
            return response
        elif request.POST['action']=='approve'and list=='admited':
            filtered_data.update(aproved=True)
        elif request.POST['action']=='approve'and list!='admited':
            HttpResponse(" wrong reqest")
    return render(request, 'principal/listpage.html', context)
#principal view student
@group_required(['principal'])
def pplstudent(request,list, userid):
    try:
        data = models.PgStudentDetails.objects.filter(details_submited=True).get(student__username=userid)
    except models.PgStudentDetails.DoesNotExist:
        raise Http404("Student details not found.")
    except Exception as e:
        # Return a generic error message or redirect to an error page
        return HttpResponse(e)
    context = {'data': data}
    if list=='applied':
        return render(request, 'controler/studentview_not_turnedup.html', context)
    else:
        return render(request, 'principal/student.html', context)


# office view
    
# def deptselect(request):
#     dpt=models.Department.objects.all()
#     return render(request,'office/index.html',{'department':dpt})
@group_required(['office'])
def office(request):
    dep = request.GET.get('dep', '').lower()
    search=request.GET.get('data', '').lower()
    try:
        dpt = models.Department.objects.all()
        data=models.PgStudentDetails.objects.filter(status='admited').filter(aproved=True).filter(Q(student__username__icontains=search)|Q(name__icontains=search))

    except Exception as e:
        return HttpResponse(e)
    if dep == 'all' or dep == '':
        filtered_data = data.order_by('-community')
    else:
        filtered_data = data.filter(Department__name=dep).order_by('-community')
    context = {
        'data': filtered_data,
        'department': dpt,
        'count':filtered_data.count()
    }
    return render(request, 'office/listpage.html', context)

@group_required(['office'])
def stdoffice(request,userid):
    
    try:
        data = models.PgStudentDetails.objects.filter(details_submited=True).filter(aproved=True).get(student__username=userid)
    except models.PgStudentDetails.DoesNotExist:
        raise Http404("Student details not found.")
    except Exception as e:
        return HttpResponse(e)
    if request.method=='POST':
        data.fees=True
        data.save()
        redirect('office')
    context = {'data': data}
    return render(request, 'office/student.html', context)