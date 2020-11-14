import numpy as np
import cv2
from cv2 import aruco
from utils import parse_options


def find_params_by_aruco_id(aruco_id, params):
    show_aruco = True
    for robo_params in params["robots"]:
        if robo_params["aruco_id"] == aruco_id:
            return show_aruco, robo_params

    if params["defaults"]["tag_unknown_arucos"] is False:
        show_aruco = False
    return show_aruco, params["defaults"]


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def main():
    params = parse_options("params.yaml")

    cap = cv2.VideoCapture(params["video_path"])
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)

    aruco_params = aruco.DetectorParameters_create()
    aruco_params.cornerRefinementMethod = \
        aruco.CORNER_REFINE_SUBPIX
    aruco_params.cornerRefinementWinSize = 5
    aruco_params.minMarkerDistanceRate = 0.05
    aruco_params.cornerRefinementMinAccuracy = 0.5

    resize_factor = params["aruco_detection_resize_factor"]

    print("\n==============")
    print("Press CTRL and C simuntaniously to exit program")
    print("==============\n")
    try:
        while True:
            ret, frame = cap.read()

            width = int(frame.shape[1] * resize_factor)
            height = int(frame.shape[0] * resize_factor)
            dim = (width, height)
            resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            corners, aruco_ids, rejected = aruco.detectMarkers(
                resized_frame,
                aruco_dict,
                parameters=aruco_params)

            if len(corners) > 0:
                for corner, aruco_id in zip(corners, aruco_ids):
                    show_aruco, robo_params = find_params_by_aruco_id(aruco_id, params)
                    if show_aruco is False:
                        continue

                    center = np.mean(corner, axis=1, dtype=np.int32)[0]

                    overlay = np.full([params["box"]["y_size"], params["box"]["x_size"], 3],
                                      robo_params["box_color"][::-1],
                                      dtype=np.uint8)

                    # TODO: X and Y use is abmiguous. Which one is which?
                    x_start = int((center[1] / resize_factor) - int(params["box"]["y_size"] / 2))
                    x_stop = x_start + int(params["box"]["y_size"])
                    y_start = int((center[0] / resize_factor) - int(params["box"]["x_size"] / 2))
                    y_stop = y_start + int(params["box"]["x_size"])

                    x_start_idx = clamp(x_start, 0, frame.shape[0] - params["box"]["y_size"])
                    x_stop_idx = clamp(x_stop, params["box"]["y_size"], frame.shape[0])
                    y_start_idx = clamp(y_start, 0, frame.shape[1] - params["box"]["x_size"])
                    y_stop_idx = clamp(y_stop, params["box"]["x_size"], frame.shape[1])

                    # https://stackoverflow.com/questions/40895785/using-opencv-to-overlay-transparent-image-onto-another-image
                    overlay = cv2.addWeighted(frame[x_start_idx:x_stop_idx,
                                                    y_start_idx:y_stop_idx],
                                              params["box"]["transparentness"],
                                              overlay,
                                              1 - params["box"]["transparentness"],
                                              0)
                    frame[x_start_idx:x_stop_idx, y_start_idx:y_stop_idx] = overlay

                    text_start = (int((center[0] + params["text"]["offset_x"]) / resize_factor),
                                  int((center[1] + params["text"]["offset_y"]) / resize_factor))

                    aruco_text = robo_params["name"]
                    cv2.putText(frame,
                                aruco_text,
                                text_start,
                                getattr(cv2,
                                        params["text"]["font_name"],
                                        "FONT_HERSHEY_SIMPLEX"),
                                params["text"]["size"],
                                robo_params["text_color"][::-1],
                                params["text"]["thickness"],
                                cv2.LINE_4)

            if params["show_aruco_detection_image"]:
                cv2.imshow('Aruco marker detection image', resized_frame)
            cv2.imshow('out', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture

    except KeyboardInterrupt:
        print("Exiting")
    # except Exception as error:
    #     print(f'Got unexpected exception in "main" Message: {error}')
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
