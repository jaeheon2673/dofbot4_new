#!/usr/bin/env python3
#coding=utf-8

import time
import random  # 랜덤 각도 생성을 위한 모듈
from Arm_Lib import Arm_Device

# 로봇 팔 객체 생성
Arm = Arm_Device()

time.sleep(0.1)

# 모든 서보 모터를 랜덤 각도로 이동시키고 각도를 읽는 함수
def move_and_read_random_servo_angles():
    # 서보 모터의 각도를 랜덤으로 설정 (각 서보마다 0~180도 범위에서 랜덤 선택)
    servo_angles = [random.randint(0, 180) for _ in range(6)]

    # 서보 모터를 랜덤 각도로 이동
    for i in range(6):
        angle = servo_angles[i]
        try:
            print(f"Moving Servo {i+1} to {angle} degrees")
            Arm.Arm_serial_servo_write(i+1, angle, 500)  # 각도 이동 (500ms 동안 이동)
            time.sleep(0.5)  # 각 서보의 이동이 완료되도록 대기
        except Exception as e:
            print(f"Error moving servo {i+1}: {str(e)}")  # 에러 메시지를 안전하게 출력

    # 모든 서보 모터의 현재 각도를 읽고 출력
    print("\nReading current angles of all servos:")
    for i in range(6):
        try:
            current_angle = Arm.Arm_serial_servo_read(i+1)  # 각 서보의 현재 각도 읽기
            print(f"Servo {i+1} current angle: {current_angle} degrees")
            time.sleep(0.1)  # 각도 읽기 후 약간의 대기
        except Exception as e:
            print(f"Error reading servo {i+1}: {str(e)}")  # 에러 메시지를 안전하게 출력

try:
    move_and_read_random_servo_angles()
except KeyboardInterrupt:
    print(" 프로그램이 종료되었습니다!")
finally:
    # 로봇 팔 객체 해제
    del Arm
    print("로봇 팔이 초기화되었습니다.")



