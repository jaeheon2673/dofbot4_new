1.터미널에서 가상환경 myenv를 설정
2.main1.py를 실행한다.
3.main1.py는 juicy의 모든 동작을 담당한다.
4.catch : 주전자를 잡는다.
5.move : 주전자를 옮긴다.
6.water : 물을 따른다.
7.return : 주전자를 제자리로 옮긴다.
8.initial : 로봇팔을 원위치 시킨다.
9.main1.py
10.depth camera인 intelrealsense가 연결되고 화면이 보인다.
11.다른 로봇팔 tae가 move상태, 즉 0인 컵을 들고 있는 상태를 확인한다.
12.그러면 바운딩 박스가 쳐지면서 신뢰도와 label 0이 나온다.
13.tae가 move2 코드를 통해서 컵받침으로 컵을 옮기면 카메라를 통해서 1의 상태를 인지하고 물을 따르기 위한 동작을 실행한다.
14.catch move water return initial순으로 실행되고 동작이 마무리된다.