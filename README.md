<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email
-->

# EasyDangerzone
[EasyDangerzone Demo 접속하기](http://ec2-52-78-218-146.ap-northeast-2.compute.amazonaws.com:5000/)

# update 09.02  
* 파일 업로드 시, 첫번째로 2page 파일, 두번째로 1page 파일을 업로드 하면 첫번째 파일의 두번째 페이지가 같이 merge되서 나오는 오류를 발견함 --> dangerzone-pixel 내부의 width, height, rgb를 매번 변환 시 지우고 새로 업데이트하도록 변경  
* 지원 불가능한 확장자를 업로드하여 실행하면 내부에서 에러를 발생시켜 페이지 자체에 에러가 보여지는 오류 --> 확장자에 대한 조건을 걸어 지원 불가능한 확장자 파일을 선택 시 불가능하다는 alert를 띄우도록 변경

# todo
* 방문자 수 및 다운로드 수 db에 연동하여 동적으로 업데이트 되도록 변경해야함. 현재는 기록을 바탕으로 하드 코딩 되어있음.  
* contact를 통해 전송 시 특정 메일로 보내진다던지, 대상을 결정해야함. 슬랙을 연동한다면 어떤 식으로 연동할 것인지. 

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project
사용한 오픈소스 프로젝트: [dangerzone](https://github.com/firstlookmedia/dangerzone)  
OS 및 여러가지에 의존성이 높은 dangerzone 프로그램을 쉽게 사용할 수 있도록 하자는 취지로 고안된 프로젝트입니다.  
웹에 파일을 업로드 하면, 서버에서 dangerzone을 거쳐 안전한 파일을 전달하고, 이 파일을 다시 사용자가 받을 수 있도록 하는 형태로 구현하였습니다.
또한 Dashboard를 통해 파일 변환 추이 및 사용자 추이를 확인할 수 있으며, Feedback 및 문의사항을 Contact에 남길 수 있습니다.

현재 지원 가능한 파일 타입 목록:  
* PDF(`.pdf`)
* WORD(`.docx`,`.doc`)
* EXCEL(`.xlsx`,`.xls`)
* PPT(`.pptx`,`.ppt`)
* ODF(`.odt`,`.ods`,`.odp`,`.ods`)
* JPEG(`.jpg`,`.jpeg`)
* GIF(`.gif`)
* PNG(`.png`)
* TIFF(`.tif`,`.tiff`)


<!-- GETTING STARTED -->
## Getting Started
for ubuntu 18.04 LTS:
```
#!/bin/bash

#echo 'ubuntu:korea123!!' | chpasswd
sudo -S sh -c 'echo "ubuntu:korea123!!" | chpasswd'

echo "deb https://packagecloud.io/firstlookmedia/code/ubuntu/ bionic main" | sudo tee -a /etc/apt/sources.list.d/firstlookmedia_code.list
curl -L https://packagecloud.io/firstlookmedia/code/gpgkey | sudo apt-key add -

sudo apt-get update
# sudo apt-get install -y ubuntu-desktop xrdp curl gnupg apt-transport-https dangerzone python3 python3-pip
sudo apt-get install -y curl gnupg apt-transport-https dangerzone python3 python3-pip

pip3 install django>=2.0
mkdir -p /tmp/dangerzone-pixel
mkdir -p /tmp/dangerzone-safe

sudo usermod -aG docker ubuntu
sudo chmod 666 /var/run/docker.sock
sudo systemctl daemon-reload
sudo systemctl start docker
sudo systemctl enable docker
/usr/bin/docker pull flmcode/dangerzone
```

for python3:
```
pip install -r requirements.txt
```

위 요구사항을 모두 설치한 뒤, manage.py가 있는 폴더로 이동합니다.  

for Run program:
```
python3 manage.py runserver
or
python manage.py runserver
```
