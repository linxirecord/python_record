import paramiko,json
import pymysql
from rest_framework import exceptions
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views import View
###����Ȩ�ޣ��鿴ʵ����databases��tables

def recv_data(self,request,ret):
#    '''�������ݣ����ж��û�������Ƿ�����'''
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
    '''ͨ���û������ip��ַ����sshȻ���
        �����е�mysqld��port'''
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
    '''ͨ���������ͱ仯�����յõ�ip:port��ʽ
        �����ݣ����ҷ���ret��ǰ��'''
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
    '''ͨ��ǰ�˵����ʵ������ȡ����ʵ�������е�database'''
    def get(self,request):
        ip_port=request.path
        user='root'
        password='redhat'
        ip=ip_port.split(':')[0].lstrip('/')
        port=int(ip_port.split(':')[1].rstrip('/'))
        # user=request.Get.get['user']
        # password=request.Get.get['password']    #ǰ�˽���¼ʱ��user��password����url
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
    '''ͨ���û������database��ȡ��database�����еı�'''
    ip='192.168.5.10'
    port=3306
    user = 'root'
    password = 'redhat'
    table = 'mysql'      #�����������ǰ���ṩ
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
