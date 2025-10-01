import cv2, time

path = "output_trimmed.mp4"
templ = cv2.imread('/home/ubuntu/Code/twitch_detections/twitch_detections/test/frame/double_kill_tighter.png', cv2.IMREAD_GRAYSCALE)
x,y,w,h = 710,479,200,200   # change to 50,75 etc.

cap = cv2.VideoCapture(path)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
cv2.setUseOptimized(True)

n=0; t_decode=0.0; t_gray=0.0; t_match=0.0
while True:
    t0=time.time()
    ok = cap.grab()
    if not ok: break
    ok, frame = cap.retrieve()
    t_decode += time.time()-t0
    if not ok: break

    roi = frame[y:y+h, x:x+w]

    t0=time.time()
    roi_g = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    t_gray += time.time()-t0

    t0=time.time()
    res = cv2.matchTemplate(roi_g, templ, cv2.TM_CCOEFF_NORMED)
    _ = cv2.minMaxLoc(res)
    t_match += time.time()-t0
    n+=1

cap.release()
print(f"frames={n} decode={t_decode:.3f}s gray={t_gray:.3f}s match={t_match:.3f}s total={t_decode+t_gray+t_match:.3f}s")
