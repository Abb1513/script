# coding=utf-8
import os, re,time
#  自动创建Jenkins Job
#  2019年7月24日
# Url  服务名
jenkins_home = '/root/.jenkins/jobs/'
jenkins_user = 'root'
# jenkins_passwd = '116365fd86d63bf507aba962606a5c8956'  Pre token
jenkins_passwd = '11811f784531053132519844d047186074'   # Dev Token
jenkins_url = 'http://10.1.188.121'
#jenkins_conf = '/etc/jenkins.conf'
jenkins_conf = r'./jenkins.conf'
# "${JAVA_CMD}" -jar "${JAR_FILE}" -s "${JENKINS_URL}" copy-job "${SRC_BUILD}" "${DST_BUILD}" --username "${USER_NAME}" --password "${PASSWORD}"
with open(jenkins_conf,'r') as f:
    for line in f.readlines():
        try:
            t = line.split(',')
            git_url = t[0]
            server_name = t[1]
            port = t[2].strip('\n')
            name='Dev_' + server_name
            if os.path.exists(jenkins_home+name):
                print '%s Job Is Exist'%name
                print
                continue
            # java -jar jenkins-cli.jar -s http://10.1.188.121 copy-job SRC DST
            # Copies a job.
            #  SRC : Name of the job to copy
            #  DST : Name of the new job to be created.
            new_job = jenkins_home + name
            print "GiT:", git_url, "服务名:", server_name, "端口号:", port, "新Job:", new_job
            print
            result = os.system('/application/java/bin/java -jar /data/deploy/jenkins-cli.jar -s http://192.168.1.62:7000 -auth %s:%s  copy-job template %s'%(jenkins_user,jenkins_passwd,name) )
           # if os.path.exists(new_job):
            if result == 0:
                os.chdir(new_job)
                os.system("sed -ie 's#PORT#%s#g;s#SERVERNAME#%s#g;s#GITURL#%s#g' config.xml"%(port,server_name,git_url))
          #      print "sed -ie 's#PORT#%s#g;s#SERVERNAME#%s#g;s#URL#%s#g' config.xml"%(port,server_name,git_url)
                print "Create \033[1;35m Success \033[0m!"
            else:
                print "\033[1;31m Create Faild! Please Check Config  \033[0m"
        except Exception as e:
            print e
#print "\033[1;33m Will Resrart Reload\033[0m"
print
print "\033[1;32m  Will Resrart Reload\033[0m"
os.system('/application/java/bin/java -jar /data/deploy/jenkins-cli.jar   -s http://192.168.1.62:7000 -auth %s:%s restart'%(jenkins_user,jenkins_passwd))
