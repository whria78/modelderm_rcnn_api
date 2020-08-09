JAMA Dermatology (doi @) 와 PLOS Medicine (doi @) 에 publish 되었던 region-based CNN 모델의 online API 입니다. 모델 API 는  are provided without restriction. 전송된 사진은 IP 정보와 함께 저장되며 algorithm 의 정확도 개선을 위한 목적으로만 사용됩니다.

# Requirement
1) python 3
2) opencv
pip3 install opencv-python
or
sudo pip3 install opencv-python

# How to Use 
python test.py [test_folder or test_jpg file] [save_folder]

# Example
실행 command 사진


![capture_exmaple](./img/capture_example_folder.PNG)
![capture_exmaple](./img/capture_result_folder.PNG)
![capture_exmaple](./img/download_anaconda.PNG)
![capture_exmaple](./img/run_folder.PNG)
![capture_exmaple](./img/run_one_file.PNG)

폴더 사진
결과 사진
결과 excel 사진

# Waiting Policy
현재 test server 는 1장을 분석하는데 10,30초정도 소요되며, 대략 1주일에 2만,3만장을 분석할 수 있는 capacity 를 가지고 있습니다. IP 기준으로 동시 사용자가 3명을 초과하는 경우 누적 사용량이 많은 user 가 wait 하는 방식으로 운영되고 있습니다.

# Contact Information
다량의 사진 분석이 필요한 경우나, IRB issue 로 사진이 저장되기를 원하지 않는 경우 Han Seung Seog (whria78@gmail.com) 에 contact 하세요. 

# Citation
