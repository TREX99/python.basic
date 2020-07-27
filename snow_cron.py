import cv2, dlib, sys
import numpy as np

# 동영상 크기 조정
showRate = 0.6

# 동영상 읽기
movie = cv2.VideoCapture("video.mp4")

# face 검출기 생성
face_detector = dlib.get_frontal_face_detector()

# face 특징점 추출 (64개)
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# 얼굴을 대체할 이미지
face_replacer = cv2.imread("replace.png", cv2.IMREAD_UNCHANGED)


### 얼굴을 대체이미지로 덮어쓰는 함수
def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size = None):
    bg_img = background_img.copy()
    # convert 3 channels to 4 channels
    if bg_img.shape[2] == 3:
        bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGR2BGRA)

    if overlay_size is not None:
        img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

    b, g, r, a = cv2.split(img_to_overlay_t)

    mask = cv2.medianBlur(a, 5)

    h, w, _ = img_to_overlay_t.shape
    roi = bg_img[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)]

    img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask=cv2.bitwise_not(mask))
    img2_fg = cv2.bitwise_and(img_to_overlay_t, img_to_overlay_t, mask=mask)

    bg_img[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)] = cv2.add(img1_bg, img2_fg)

    # convert 4 channels to 4 channels
    bg_img = cv2.cvtColor(bg_img, cv2.COLOR_BGRA2BGR)

    return bg_img


while True:
    # 동영상 읽기
    retValue, videoCut = movie.read()
    
    # 동영상을 끝까지 읽었는지 확인
    if not retValue:
        break

    # 동영상 크기 조정
    videoCut = cv2.resize(videoCut, (int(videoCut.shape[1] * showRate), int(videoCut.shape[0] * showRate)))
    videoCut_original = videoCut.copy()

    # 얼굴 검출해서 있으면 얼굴에 BOX 표시된 이미지로 변경
    faces = face_detector(videoCut)
    if len(faces) > 0:
        for face in faces:

            # 얼굴로 검출된 외곽을 BOX 처리
            box_pt1 = (face.left(), face.top())
            box_pt2 = (face.right(), face.bottom())
            cv2.rectangle(videoCut, box_pt1, box_pt2, color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)

            # 특징점 64개를 흰점으로 출력
            shape_64_points = predictor(videoCut, face)
            face_64_points = np.array([[p.x, p.y] for p in shape_64_points.parts()])
            for p in face_64_points:
                cv2.circle(videoCut, center=tuple(p), radius=1, color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)

            # 좌상단, 우하단의 점좌표 획득
            left_top = np.min(face_64_points, axis=0)
            right_bottom = np.max(face_64_points, axis=0)
            center_x, center_y = np.mean(face_64_points, axis=0).astype(np.int)
            cv2.circle(videoCut, center=tuple(left_top), radius=1, color=(255, 0, 0), thickness=5, lineType=cv2.LINE_AA)
            cv2.circle(videoCut, center=tuple(right_bottom), radius=1, color=(255, 0, 0), thickness=5, lineType=cv2.LINE_AA)
            cv2.circle(videoCut, center=tuple((center_x, center_y)), radius=1, color=(0, 0, 255), thickness=5, lineType=cv2.LINE_AA)

            # 얼굴을 다른 이미지로 대체하기
            face_size = max(right_bottom - left_top)
            result = overlay_transparent(videoCut_original, face_replacer, center_x, center_y, overlay_size=(face_size, face_size))

    # 동영상 출력
    cv2.imshow("snow cron movie", videoCut)
    cv2.imshow("snow cron movie - replace", result)

    # 재생하는 중간에 중지키(q)를 입력했는지 확인
    keyValue = cv2.waitKey(1)
    if keyValue == ord('q'):
        break

