#!/usr/bin/env python3
#coding=utf-8

import time
from Arm_Lib import Arm_Device

# 로봇 팔 객체 생성
Arm = Arm_Device()

# 잠시 대기
time.sleep(0.1)

def main():
    # 서보를 중앙 위치로 초기화
    Arm.Arm_serial_servo_write6(90, 90, 90, 90, 90,160, 1500)
    time.sleep(1)


try:
    main()
except KeyboardInterrupt:
    print("프로그램이 종료되었습니다!")
    pass

# 로봇 팔 객체 해제
del Arm
