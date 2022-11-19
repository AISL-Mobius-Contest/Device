import cv2
import time
import requests
import encoding as enc

def sending():
    cap = cv2.VideoCapture(-1)  # 카메라 연결


    if cap.isOpened() :
        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, -1)
            # 카메라 한 프레임씩 읽기
            if ret:                                 # 비디오 프레임 제대로 읽으면 True, 실패하면 false
                # start = time.time()
                cv2.imshow('camera',frame)          # 프레임 화면에 표시
                cv2.imwrite('./image.jpg', frame)   # 프레임을 'image.jpg'에 저장(덮어쓰기)
                encoding = enc.encode_img('./image.jpg')
                encoding_str = encoding.decode('utf-8')

                data = [{"section":"section1","img":encoding_str}]
                print(data)
                
                url = "http://{Mobius IP & Port}/Mobius/Blossom/CCTV/section1"

                payload = "{\n    \"m2m:cin\": {\n        \"con\": \"" + str(data) +"\"\n    }\n}"
                headers = {
                'Accept': 'application/json',
                'X-M2M-RI': '12345',
                'X-M2M-Origin': 'CCTV',
                'Content-Type': 'application/json; ty=4'
                }

                requests.request("POST", url=url, headers=headers, data=payload)

                time.sleep(1)


    else:
        print('no camera!')
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    sending()