import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import numpy as np
import os
import argparse


class charuco_detector(img):
    def __init__(self):
        super().__init__()

        # ArUco 및 Charuco 보드 설정
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_50)
        number_x_square = 5
        number_y_square = 5
        length_square = 0.098  # 사각형 크기 (미터 단위)
        length_marker = 0.073  # 마커 크기 (미터 단위)

        # CharucoBoard 생성
        self.charuco_board = cv2.aruco_CharucoBoard(
            (number_x_square, number_y_square),  # 칸 개수
            length_square,                      # 사각형 크기
            length_marker,                      # 마커 크기
            self.aruco_dict                     # ArUco 딕셔너리
        )

    
    def process_and_display(self):
        """
        Charuco 보드 코너를 검출하고 결과를 오버랩하여 출력
        """
        if self.cam0_image is not None:
            cam0_visualized = self.visualize_image(self.cam0_image, "Camera 0")
        if self.cam1_image is not None:
            cam1_visualized = self.visualize_image(self.cam1_image, "Camera 1")

        # 키 입력 처리 (하나의 메인 루프에서)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # 's' 키가 눌리면 이미지 저장
            if self.cam0_image is not None:
                save_path_cam0 = os.path.join(self.output_dir_camera1, f"cam0_image_{self.image_count}.png")
                cv2.imwrite(save_path_cam0, self.cam0_image)  # 원본 이미지 저장
                self.get_logger().info(f"Saved Camera 0 image: {save_path_cam0}")

            if self.cam1_image is not None:
                save_path_cam1 = os.path.join(self.output_dir_camera2, f"cam1_image_{self.image_count}.png")
                cv2.imwrite(save_path_cam1, self.cam1_image)  # 원본 이미지 저장
                self.get_logger().info(f"Saved Camera 1 image: {save_path_cam1}")

            self.image_count += 1

    def visualize_image(self, image, window_name):
        """
        Draw markers and resize image for visualization.
        """
        # 복사본 생성 (시각화를 위한 이미지)
        visualized_image = image.copy()
        gray = cv2.cvtColor(visualized_image, cv2.COLOR_BGR2GRAY)

        # ArUco 마커 탐지
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.aruco_dict)

        if ids is not None:
            # Charuco 코너 보정
            _, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(
                corners, ids, gray, self.charuco_board
            )

            # ArUco 마커 및 Charuco 코너 시각화
            cv2.aruco.drawDetectedMarkers(visualized_image, corners, ids)
            if charuco_corners is not None:
                for corner in charuco_corners:
                    cv2.circle(visualized_image, tuple(int(x) for x in corner[0]), 5, (0, 0, 255), -1)  # Charuco 코너(빨강)

        # 이미지 크기 조정 (절반 크기)
        resized_image = cv2.resize(visualized_image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow(window_name, resized_image)
        return resized_image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(conflict_handler='error', add_help=True, allow_abbrev=True)
    parser.add_argument('img', type=str)
    args = parser.parse_args()

