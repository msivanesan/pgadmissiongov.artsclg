from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse,Http404
from . import models
from django.views.decorators.cache import never_cache
import csv
from . decoraters import group_required
# select department in controler
@group_required(['controler'])
def deptcontrol(request):
    data=models.Department.objects.all()
    return render(request,'controler/index.html',{'department':data})
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
            'department':dpt
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
            dpt.save()
            data.save()
        elif request.POST['action']=='reject':
            data.status='rejected'
            data.rejectedBy='controler'
            data.remark=request.POST.get('remark', '') 
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
            return render(request, 'controler/student.html', context)
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
            'department':dpt
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
        
        if list=='selected' or list=='applied':    
            return render(request, 'department/student.html', context)
        elif list=='rejected' or list == 'admited':
            return render(request, 'department/studentview.html', context)
        else:
            return Http404("enter the correct url")

#principal view
@group_required(['principal'])
def principal(request,list):
    dep = request.GET.get('dep', '').lower()
    try:
        dpt = models.Department.objects.all()
        if list == 'admited': 
            data = models.PgStudentDetails.objects.filter(status='admited')
        elif list == 'rejected':
            data = models.PgStudentDetails.objects.filter(status='rejected')
        else:
            return HttpResponse("Enter the correct URL")
        
        if dep == 'all' or dep == '':
            filtered_data = data.order_by('student__username')
        else:
            filtered_data = data.filter(Department__name=dep).order_by('student__username')
        
    except Exception as e:
        return HttpResponse(e)
    
    context = {
        'data': filtered_data,
        'department': dpt
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
        else:
            return render(request, 'principal/listpage.html', context)
    else:
        return render(request, 'principal/listpage.html', context)
    
#principal view student
@group_required(['principal'])
def pplstudent(request,list, userid):
    try:
        data = models.PgStudentDetails.objects.filter(details_submited=True).get(student__username=userid)
        context = {'data': data}
        return render(request, 'principal/student.html', context)
    except models.PgStudentDetails.DoesNotExist:
        raise Http404("Student details not found.")
    except Exception as e:
        # Return a generic error message or redirect to an error page
        return HttpResponse(e)


