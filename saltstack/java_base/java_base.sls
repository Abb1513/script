Install Java Base environment:
  file.managed:
    - name: /tmp/jdk-8u202-linux-x64.tar.gz
    - source: salt://file/jdk-8u202-linux-x64.tar.gz
    - user: root
    - group: root
    - mode: 755
  cmd.run:
    - name: mkdir -p /application/ &&  cd /tmp/ && tar -zxf jdk-8u202-linux-x64.tar.gz -C /application/ && mv /application/jdk1.8.0_202   /application/java   && echo 'export JAVA=/application/java/bin/'>> /etc/profile && echo 'export PATH=$PATH:$JAVA' >>/etc/profile && source /etc/profile
