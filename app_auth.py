import paramiko,json
import pymysql
from rest_framework import exceptions
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views import View
###申请权限，查看实例，databases，tables

def recv_data(self,request,ret):
#    '''接收数据，并判断用户输入的是否完整'''
    ip=request.GET.get('ip')
    user=request.GET.get('user')
    password=request.GET.get('password')
    if ip==None or user==None or password==None:
        ret['msg']='input info completely'
        ret['data']=[]
    else:
        ret['data']={
            'ip':ip,
            'user':user,
            'password':password,
        }
    return ret
def re_port_list(self,request,ret):
    '''通过用户输入的ip地址进行ssh然后得
        到所有的mysqld的port'''
    ret_data=recv_data(self,request,ret)['data']
    ip=ret_data['ip']
    user=ret_data['user']
    password=ret_data['password']
    try :
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname = ip, port = 22, username = user, password = password)
        cmd="netstat -antlp | grep mysqld |grep LISTEN| awk '{print $4}'| sed 's/::://g'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode()
        json_re = json.dumps(result)
        ssh.close()
        ret['msg']='get port successful'
        ret['data']=json_re
    except exceptions as e:
        ret['msg']='Invalid IP'
        ret['data']=[]
    return ret,ip

class GetipportViewSet(APIView):
    '''通过数据类型变化，最终得到ip:port形式
        的数据，并且返回ret给前端'''
    def get(self,request,*args,**kwargs):
        '''produce ip:port'''
        ret = {'msg': None, 'data': None}
        ip_port_list=[]
        port_list = json.loads(re_port_list(self, request, ret)[0]['data']).split('\n')
        ip=re_port_list(self,request,ret)[1]
        del port_list[-1]
        for i in port_list:
            ip_port_list.append(ip+':'+i)
        ret=re_port_list(self, request, ret)[0]
        ret['msg']='success'
        ret['data']=ip_port_list
        print(ret)
        return JsonResponse(ret)

class list_database(View):
    '''通过前端点击的实例，获取到该实例下所有的database'''
    def get(self,request):
        ip_port=request.path
        user='root'
        password='redhat'
        ip=ip_port.split(':')[0].lstrip('/')
        port=int(ip_port.split(':')[1].rstrip('/'))
        # user=request.Get.get['user']
        # password=request.Get.get['password']    #前端将登录时的user，password传给url
        conn = pymysql.connect(host=ip, port=port, user=user, password=password,
                               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        cursor.execute("show databases;")
        data_list=cursor.fetchall()
        print(data_list)
        length=len(data_list)
        database_list=[]
        sys_database_list=['information_schema','mysql','sys','performance_schema']
        for i in range(length):
            database_list.append(data_list[i]['Database'])
        for j in sys_database_list:
            database_list.remove(j)
        conn.commit()
        cursor.close()
        conn.close()
        return JsonResponse(database_list, safe=False)

def list_table(request):
    '''通过用户点击的database获取该database下所有的表'''
    ip='192.168.5.10'
    port=3306
    user = 'root'
    password = 'redhat'
    table = 'mysql'      #这五个参数由前端提供
    conn = pymysql.connect(host=ip, port=port, user=user, password=password, db=table,
                                charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    cursor.execute("show tables;")
    tb_list_in_dic = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    tb_list = []
    for i in tb_list_in_dic:
        tb_list.append(i['Tables_in_mysql'])
    print(tb_list)
    return JsonResponse(tb_list, safe=False)
