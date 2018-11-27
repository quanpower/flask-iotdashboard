1、路径说明：

　　路径：/usr/local/src

2、下载nginx-rtmp-module (我这里的目录是在/usr/local/src/下面)

       cd /usr/local/src

        nginx-rtmp-module的官方github地址：https://github.com/arut/nginx-rtmp-module

        git clone https://github.com/arut/nginx-rtmp-module.git 

       （ 如果没有git进行安装，yum install git）

       

       sudo apt install libpcre3 libpcre3-dev
		sudo apt install openssl libssl-dev


3、nginx版本及安装

       下载 nginx-1.14.1.tar.gz 解压并安装

　　wget http://nginx.org/download/nginx-1.14.1.tar.gz   （如果下载不到请自行查找）
        
        tar -zxvf nginx-1.14.1.tar.gz   （解压）
        
        cd nginx-1.14.1  （进入目录）
        
        ./configure --prefix=/usr/local/src/nginx  --add-module=../nginx-rtmp-module  --with-http_ssl_module    
        
        make && make install 

4.****配置nginx****
在nginx的配置文件nginx.conf最后添加如下信息

# RMTP的服务器配置信息
rtmp {
        server {
                listen  2016; #推流的监听端口
                publish_time_fix on;
                # 推流其一
                application live {
                        live on; #stream on live allow
                        allow publish all; # control access privilege
                        allow play all; # control access privilege
                }
               #推流其二
        application hls_alic {
                        live on;
                        hls on;
                        hls_path /home/alic/www/hls;
                        hls_fragment 5s;
                }
        }
}
重新加载nginx的配置

$ /usr/local/nginx/sbin/nginx -s reload
****简单的测试demo****
安装ffmpag

$ add-apt-repository ppa:kirillshkrogalev/ffmpeg-next
$ apt-get update
$  apt-get install ffmpeg
使用ffmpeg向服务器推送一个视频

ffmpeg -re -i /home/alic/Desktop/demo/film.mp4 -c copy -f flv rtmp://localhost:2016/live/film
or
# 推荐 可用于浏览器播放
ffmpeg -re -i /home/alic/Desktop/demo/film.mp4 -c copy -f flv rtmp://localhost:2016/hls_alic/film
Alic_推流
视频播放器获取视频流


Alic_客户端获取流
对于浏览器呢,html的整理代码如下

<html>
<head>
    <link rel="stylesheet" href="http://vjs.zencdn.net/5.10/video-js.css">
</head>
    <video id=example-video width=960 height=540 class="video-js vjs-default-skin" controls>
        <source
            src="film.m3u8"
            type="application/x-mpegURL">
    </video>
    <script src="http://vjs.zencdn.net/5.10/video.js"></script>
    <script src="https://npmcdn.com/videojs-contrib-hls@^3.0.0/dist/videojs-contrib-hls.js"></script>
    <script>
        var player = videojs('example-video');
        player.play();
    </script>
</html>
注意，在hls_path的路径添加一个站点来访问即可！
推流还是用ffmpeg的命令来, 推流一段时间后, 你会发现在"/home/alic/www/hls"目录里, 有很多ts文件,
还有一个后缀".m3u8"文件上面配置中的 server:8081 块, 就是为了能在外部能访问这些ts文件和m3u8文件。

Alic_浏览器

搭建推流服务器Nginx+rtmp就成功了！
即将总结ffmpeg推流的命令~~~

# RMTP的服务器配置信息
rtmp {
        server {
                listen  1935; #推流的监听端口
                chunk_size 4096;
                publish_time_fix on;
                # 推流其一
                application live {
                        live on; #stream on live allow
                        allow publish all; # control access privilege
                        allow play all; # control access privilege
                }
               #推流其二
        application hls_alic {
                        live on;
                        hls on;
                        hls_path /home/alic/www/hls;
                        hls_fragment 5s;
                }    
        }
}


第一步：添加源。

sudo add-apt-repository ppa:djcj/hybrid
第二步：更新源。
sudo apt-get update
第三步：下载安装。
sudo apt-get install ffmpeg


sudo add-apt-repository ppa:kirillshkrogalev/ffmpeg-next

sudo apt-get update

sudo apt-get install ffmpeg


sudo ./sbin/nginx -c conf/nginx.conf

ffmpeg -re -i /home/quanpower/Downloads/xvideos.com_40178813ef6381d45823e48b63f5153d.mp4 -c copy -f flv rtmp://localhost:1935/live/film

ffmpeg -re -i /home/quanpower/Downloads/xvideos.com_40178813ef6381d45823e48b63f5153d.mp4 -c copy -f flv rtmp://localhost:1935/hls/film 


ffmpeg -re -i rtsp:// -c copy -f flv rtmp://localhost:1935/live/film

ffmpeg -i "rtsp://admin:shuhang2018@192.168.1.64:554/h265/ch1/main/av_stream" -f flv -r 25 -s 640x360 -an rtmp://localhost:1935/live/room
