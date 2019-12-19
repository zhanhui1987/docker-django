1，概述

    使用docker，进行django后端服务的快速部署。


2，设计思路

    （1）核心思路：用docker image封装使用的各种软件，同时将django项目使用到的所有python包进行统一管理。

    （2）将django后端服务，划分为三个部分：代理（nginx）、数据库（mysql）、web服务（python+django+uwsgi）。

        按照这个思路，生成相应的三个docker image： z1987_nginx、z1987_mysql、z1987_web。

![](http://qiniu.z1987.com/20.overall_framework.png)

    （3）容器之间使用 docker network 进行内部通讯，仅将nginx容器的某个端口（示例中是30080）暴露出来，用于接受外部访问。

    （4）将代码、配置文件、数据库数据文件等，挂载到容器中，方便进行代码的更新、数据的保存。


3，开发环境

    （1）开发服务信息
    云服务商：     腾讯云
    宿主机系统：   ubuntu16.04

    （2）涉及到软件的信息
    反向代理：   nginx   （v1.14.0）
    数据库：     mysql   （v5.7.28）
    后端语言：   python  （v3.6.9）
    框架：       django  （v2.0.8）
    web服务器：  uwsgi   （v2.0.18）

    （3）docker基础镜像信息

    REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
    ubuntu              16.04               56bab49eef2e        3 weeks ago         123MB
    mysql               5.7                 1e4405fe1ea9        3 weeks ago         437MB
![](http://qiniu.z1987.com/1.base_image.png)


4，操作流程

    （1）使用git，将本仓库clone到root目录下：

        git clone git@github.com:zhanhui1987/docker-django.git /root/docker-django/

![](http://qiniu.z1987.com/0.git_clone.png)

    （2）拉取基础镜像（ubuntu:16.04和mysql:5.7）：

        docker pull ubuntu:16.04
        docker pull mysql:5.7

![](http://qiniu.z1987.com/2.pull_base_image.png)

        注：需确保这两个基础镜像的 IMAGE ID 和3中相应的IMAGE ID相同。

    （3）创建项目三个镜像：

        按照 /root/docker-django/docker/makefile/README 中的操作步骤，创建三个docker 镜像：

        root@bbb70:~# docker images
        REPOSITORY   TAG     IMAGE ID        CREATED          SIZE
        z1987        web     fd8ed2ef0be3    9 minutes ago    651MB
        z1987        mysql   ec99611492c9    3 hours ago      437MB
        z1987        nginx   ed8a71920403    4 hours ago      255MB

![](http://qiniu.z1987.com/3.generate_customer_image.png)

    （4）创建项目的三个容器：

        按照 /root/docker-django/docker/container/README 中的操作步骤，创建 docker network 和三个docerk 容器：

        root@bbb70:~# docker network ls
        NETWORK ID          NAME                DRIVER              SCOPE
        958e3efd8635        z1987-net           bridge              local

![](http://qiniu.z1987.com/4.ls_docker_network.png)

        root@bbb70:~# docker ps -a

![](http://qiniu.z1987.com/5.running_docker_container.png)

    （5）通过服务器的30080端口，对web页面进行访问（示例中，项目部署在z1987.com服务器上，因此使用该域名进行访问）：

        web页面：  z1987.com:30080

![](http://qiniu.z1987.com/6.web.png)

        管理员页面：  z1987.com:30080/admin， 使用默认的超级管理员：  admin / admin 登录：

![](http://qiniu.z1987.com/7.admin_login.png)

        可以通过管理员页面 用户 二级页面，对管理账号进行编辑

![](http://qiniu.z1987.com/8.admin.png)

        通过 博客 二级页面，添加新的博客。

![](http://qiniu.z1987.com/9.blog.png)
![](http://qiniu.z1987.com/10.add_blog.png)


5， 数据初始化

    在镜像中，对数据库database、后端管理员账号等进行了初始化操作。

    （1）mysql的表（table）、管理员账号

        在后端服务器镜像（z1987_web）中，对mysql的表、管理员账号（admin账号）进行了初始化。

        当 新建容器/重启容器 时，会执行。

        代码位置： /root/docker-django/docker/makefile/web/init/docker-entrypoint.sh

![](http://qiniu.z1987.com/18.init_mysql_table.png)

    （2）mysql的库（database）、用户（user）

        在数据库镜像（z1987_mysql）中，对mysql数据库的登陆用户、库进行了初始化。

        当 新建容器 时，会执行。

        代码位置：  /root/docker-django/docker/makefile/mysql5.7/init/init.sql

![](http://qiniu.z1987.com/19.init_mysql_database.png)

    （3）初始化的各账号信息

        账户类型：     mysql root账户
        账户名/密码：  root/root
        初始化时间：   创建mysql容器时
        初始化位置：   /root/docker-django/docker/container/README 中的： -e MYSQL_ROOT_PASSWORD="root"

        账户类型：     后端服务使用的mysql账户
        账户名/密码：  z1987_user/z1987_pw
        初始化时间：   创建mysql容器时
        初始化位置：   /root/docker-django/docker/makefile/mysql5.7/init/init.sql

        账户类型：     后端超级管理员
        账户名/密码：  admin/admin
        初始化时间：   创建web容器时
        初始化位置：   /root/docker-django/docker/makefile/web/init/docker-entrypoint.sh


        注：当需要更改后端服务使用的mysql账户时，不仅需要更改上面提到的代码文件，还需要更改后端服务的配置文件：

            /root/docker-django/z1987_web/z1987_web/settings.py


6，FAQ

    （1）项目目录解析：

        root@bbb70:~# ls -lrt docker-django
        total 28
        drwxr-xr-x 7 root root 4096 Dec 16 19:58 z1987_web
        drwxr-xr-x 4 root root 4096 Dec 16 20:17 docker
        drwxr-xr-x 6 root root 4096 Dec 17 17:54 project_files
        drwxr-xr-x 4 root root 4096 Dec 18 00:19 packages
        -rw-r--r-- 1 root root 8392 Dec 18 14:06 README.md

![](http://qiniu.z1987.com/11.code_structure.png)

        仓库根目录下有一个说明文件（README.md）、四个文件夹：

        z1987_web：     django项目代码
![](http://qiniu.z1987.com/12.web_code_folder.png)

        docker：        保存镜像和容器创建相关的内容，例如 Dockerfile、容器创建命令等
![](http://qiniu.z1987.com/13.docker_folder.png)

        project_files:  保存项目相关的文件，例如容器中的日志文件（logs文件夹：nginx日志、uwsgi日志等）、
                        mysql数据库文件（mysql_data文件夹）、配置文件（conf文件夹：mysql、nginx等）。
                        在运行docker容器时，会将这些文件挂载到相应容器的对应路径。
![](http://qiniu.z1987.com/15.project_files_folder.png)

        packages：      保存django项目涉及到的python包，在创建 z1987_web 容器时，会将这些包的路径挂载到
                        容器对应的python路径下，确保django项目涉及到的python包均能正确加载。
![](http://qiniu.z1987.com/14.packages_folder.png)

    （2）项目涉及到的文件，均保存在宿主机、挂载到docker容器。因此只需要在宿主机对文件进行更改，重启相应docker容器即可
        使其生效：

        docker restart 容器名/容器ID
![](http://qiniu.z1987.com/16.restart_container.png)

    （3）进入docker容器的方法：

        推荐使用 docker exec 的命令，来进入docker容器：

        命令：  docker exec -it 容器名/容器ID bash

        示例：  docker exece -it z1987_web bash
![](http://qiniu.z1987.com/17.exec_container.png)

        注：命令最后的bash（或 /bin/bash ）不可缺少，意思是进入容器并执行 bash 命令。


7，项目缺陷：

    （1）仅在腾讯云、ubuntu16.04环境上进行了测试，在其他环境下使用时可能会出现异常情况。

    （2）python包的收集、管理，目前未找到好的方法。在web镜像中，安装好uwsgi之后将pip删除，是为了确保镜像最小化。

    （3）开发/测试过程中，出现了基础镜像 ubuntu:16.04 发生变更的情况。导致初始采用的python3.5无法正常安装。

        后续也可能会出现这种情况，因此需要确认基础镜像的版本，或对使用的python版本、python包进行调整。
