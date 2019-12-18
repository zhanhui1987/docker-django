1，概述

    尝试使用docker，来进行django后端服务的快速部署。


2，设计思路

    （1）核心思路：用docker image封装使用的各种软件，同时将django项目使用到的所有python包进行统一管理，这样能够确保部署新的服务器时，软件和python包都是一致的。

    （2）将django后端服务，划分为三个部分：代理（nginx）、数据库（mysql）、web服务（python+django+uwsgi）。

        按照这个思路，生成相应的三个docker image： z1987_nginx、z1987_mysql、z1987_web。
        ![]()

    （3）三个容器之间，使用 docker network 进行相互间的通讯，仅将 z1987_nginx 容器的某个端口（示例中是 30080）暴露出来。

    （4）使用docker容器挂载文件夹/文件的方法，把代码、配置文件、数据库文件等均挂载到容器里，方便进行代码的更新、数据的保存。


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
    ![](https://raw.githubusercontent.com/zhanhui1987/docker-django/master/project_files/.dd-img/1.base_image.png)

4，操作流程

    （1）使用git，将本仓库clone到root目录下：

        git clone git@github.com:zhanhui1987/docker-django.git /root/docker-django/

        ![拉取基础镜像](https://raw.githubusercontent.com/zhanhui1987/docker-django/master/project_files/.dd-img/4.%20%E6%8B%89%E5%8F%96%E5%9F%BA%E7%A1%80%E9%95%9C%E5%83%8F.png)

    （2）拉取基础镜像（ubuntu:16.04和mysql:5.7）：

        docker pull ubuntu:16.04
        docker pull mysql:5.7

        ![]()

        注：需确保这两个基础镜像的 IMAGE ID 和3中相应的IMAGE ID相同。

    （3）创建项目三个镜像：

        按照 /root/docker-django/docker/makefile/README 中的操作步骤，创建三个docker 镜像：

        root@bbb70:~# docker images
        REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
        z1987               web                 fd8ed2ef0be3        9 minutes ago       651MB
        z1987               mysql               ec99611492c9        3 hours ago         437MB
        z1987               nginx               ed8a71920403        4 hours ago         255MB

        ![]()

    （4）创建项目的三个容器：

        按照 /root/docker-django/docker/container/README 中的操作步骤，创建 docker network 和三个docerk 容器：

        root@bbb70:~# docker network ls
        NETWORK ID          NAME                DRIVER              SCOPE
        958e3efd8635        z1987-net           bridge              local

        ![]()

        root@bbb70:~# docker ps -a
        CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                              NAMES
        a2b90122c70a        z1987:nginx         "/bin/sh -c /usr/sbi…"   12 minutes ago      Up 12 minutes       443/tcp, 0.0.0.0:30080->80/tcp     z1987_nginx
        b69188c154c9        z1987:web           "docker-entrypoint.sh"   12 minutes ago      Up 12 minutes                                          z1987_web
        6c0ad04f72e8        z1987:mysql         "docker-entrypoint.s…"   12 minutes ago      Up 12 minutes       3306/tcp, 33060/tcp                z1987_mysql

        ![]()

    （5）通过服务器的30080端口，对web页面进行访问（示例中，项目部署在 z1987.com 对应的服务器上。测试时可以将该域名更换为实际IP）：

        web页面：  z1987.com:30080

        ![]()

        管理员页面：  z1987.com:30080/admin， 使用默认的超级管理员：  admin / admin 登录：

        ![]()

        可以通过管理员页面 用户 二级页面，对管理账号进行编辑

        ![]()

        通过 博客 二级页面，添加新的博客。

        ![]()
        ![]()

5，FAQ

    （1）项目目录解析：

        root@bbb70:~# ls -lrt docker-django
        total 28
        drwxr-xr-x 7 root root 4096 Dec 16 19:58 z1987_web
        drwxr-xr-x 4 root root 4096 Dec 16 20:17 docker
        drwxr-xr-x 6 root root 4096 Dec 17 17:54 project_files
        drwxr-xr-x 4 root root 4096 Dec 18 00:19 packages
        -rw-r--r-- 1 root root 8392 Dec 18 14:06 README.md

        ![]()


        仓库根目录下有一个说明文件（README.md）、四个文件夹：

        z1987_web：     django项目代码
        ![]()

        docker：        保存镜像和容器创建相关的内容，例如 Dockerfile、容器创建命令等
        ![]()

        project_files:  保存项目相关的文件，例如容器中的日志文件（logs文件夹：nginx日志、uwsgi日志等）、mysql数据库文件（mysql_data文件夹）、配置文件（conf文件夹：mysql、nginx等）。
                        在运行docker容器时，会将这些文件挂载到相应容器的对应路径。
        ![]()

        packages：      保存django项目涉及到的python包，在创建 z1987_web 容器时，会将这些包的路径挂载到容器对应的python路径下，确保django项目涉及到的python包均能正确加载。
        ![]()

    （2）因项目涉及到的文件，均保存在宿主机、挂载到docker容器，因此当需要对某个文件进行更改时，只需要在宿主机对其进行更改，并重启对应的docker容器即可使其生效：

        docker restart 容器名/容器ID
        ![]()

    （3）进入docker容器的方法：

        推荐使用 docker exec 的命令，来进入docker容器：

        docker exec -it 容器名/容器ID bash

        docker exece -it z1987_web bash
        ![]()

        注：命令最后的bash（或 /bin/bash ）不可缺少，意思是进入容器并执行 bash 命令。

    （4）后端服务镜像（z1987_web）中，集成了同步数据库、创建超级管理员（admin）的功能。当 新建容器/容器重启 时，均会执行。

        代码位置：  /root/docker-django/docker/makefile/web/init/docker-entrypoint.sh
        ![]()

    （5）数据库镜像（z1987_mysql）中，集成了初始化user、database的功能。当 新建容器 时，会执行：

        代码位置：  /root/docker-django/docker/makefile/mysql5.7/init/init.sql
        ![]()

        django项目中使用到的mysql用户和库，均在这个文件中进行初始化。

    （6）各账号、密码的初始值及初始位置：

        账户类型                 账户名/密码            初始化时间            初始化代码文件
        mysql root账户          root/root             创建mysql容器时       /root/docker-django/docker/container/README 中的： -e MYSQL_ROOT_PASSWORD="root"
        后端服务使用的mysql账户   z1987_user/z1987_pw   创建mysql容器时       /root/docker-django/docker/makefile/mysql5.7/init/init.sql
        后端超级管理员           admin/admin           创建web容器时          /root/docker-django/docker/makefile/web/init/docker-entrypoint.sh

        注：当需要更改后端服务使用的mysql账户时，不仅需要更改上面提到的代码文件，还需要更改后端服务的配置文件（否则会因账户/密码不正确，导致无法连接数据库）：

            /root/docker-django/z1987_web/z1987_web/settings.py

    （7）项目中存在较多的 .gitignore 文件，用于过滤次要文件（.pyc文件等），或用于保存空文件夹（日志文件夹等）。


6，项目缺陷：

    （1）仅在腾讯云、ubuntu16.04环境上进行了测试，在其他环境下测试时可能会出现异常情况。这里主要是为了阐述快速部署django后端服务的一种思路。

    （2）python包的收集、管理，目前未找到好的方法。在web镜像中，安装好uwsgi之后将pip删除，是为了确保镜像最小化、确保不存在多余的功能/文件。也导致了后续新增python包时难度较大。

    （3）开发/测试过程中，出现了基础镜像： ubuntu:16.04 发生变更的情况。导致之前采用的python3.5无法正常安装，因此调整为python3.6。

        后续也可能会出现这种情况，因此需要确认基础镜像的image id，或者对使用的python版本进行调整、python包进行调整。
