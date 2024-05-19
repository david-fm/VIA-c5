import cv2 as cv
import numpy as np

def ask_for_measure(image_ref):
    """
    Ask for the scale in the image by asking for 2 points 
    and the distance between them"""

    points = []
    copy_image = image_ref.copy()

    def funImg(event, x, y, flags, param):
        """
        Callback function for the mouse event in the image"""
        if event == cv.EVENT_LBUTTONDOWN:
            points.append((x,y))
            cv.putText(copy_image, str(len(points)), (x,y), 
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv.circle(copy_image, (x,y), 5, (0,0,255), -1)
    
    cv.namedWindow('Image')
    cv.setMouseCallback('Image', funImg)

    cv.namedWindow('Explanation')
    explanation = np.zeros((250, 500, 3), np.uint8)
    cv.putText(explanation, "Select 2 points in the image to measure the distance", 
               (10,50), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv.putText(explanation, "Press 'c' to clear the points",
                (10,80), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv.putText(explanation, "Press 'q' to finish",
                (10,110), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv.putText(explanation, "Then enter the real distance between the points "
                ,(10,150), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv.putText(explanation, "in meters in the terminal",
                (10,180), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv.imshow('Explanation', explanation)

    while True:
        cv.imshow('Image', copy_image)
        
        pressedKey = cv.waitKey(1) & 0xFF
        if pressedKey == ord('q'):
            break
        elif pressedKey == ord('c'):
            points = []
            copy_image = image_ref.copy()
    
    cv.destroyAllWindows()

    if(len(points) != 2):
        raise ValueError("You must select 2 points in the image")
    
    d = np.linalg.norm(np.array(points[0]) - np.array(points[1]))

    real_d = float(input("Enter the real distance between the points in meters: "))
    scale = real_d/d
    return scale

def rectify(image, image_ref, points, points_ref):
    """
    Rectify a plane given 4 points of reference in the image to be 
    rectifyed and in an already rectifyied image"""
    print(points)
    print(points_ref)
    points = np.array(points)
    points_ref = np.array(points_ref)
    H, _ = cv.findHomography(points, points_ref)
    rec = cv.warpPerspective(image,H,(image_ref.shape[1],image_ref.shape[0]))

    # put rec over image_ref

    rec = np.where(rec != 0, rec, image_ref)
    return rec

def get_final_measure(rectifyied, scale):
    """
    Get 2 points and given the scale measure the distance 
    between them"""
    points = []
    copy_image = rectifyied.copy()

    def funImg(event, x, y, flags, param):
        """
        Callback function for the mouse event in the image"""
        if event == cv.EVENT_LBUTTONDOWN:
            points.append((x,y))
            cv.putText(copy_image, str(len(points)), (x,y), 
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv.circle(copy_image, (x,y), 5, (0,0,255), -1)
            if len(points) == 2:
                d = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
                real_d = d*scale
                # draw a line and put the distances in meters 
                cv.line(copy_image, points[0], points[1], (0,255,0), 2)
                cv.putText(copy_image, "{:.2f} m".format(real_d), 
                           (int((points[0][0] + points[1][0])/2), 
                            int((points[0][1] + points[1][1])/2)),
                           cv.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    
    cv.namedWindow('Image')
    cv.setMouseCallback('Image', funImg)

    cv.namedWindow('Explanation')
    explanation = np.zeros((250, 500, 3), np.uint8)
    cv.putText(explanation, "Select 2 points in the image to measure the distance", 
               (10,50), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv.putText(explanation, "Press 'c' to clear the points",
                (10,80), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv.putText(explanation, "Press 'q' to finish",
                (10,110), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    cv.imshow('Explanation', explanation)

    while True:
        cv.imshow('Image', copy_image)
        
        pressedKey = cv.waitKey(1) & 0xFF
        if pressedKey == ord('q'):
            break
        elif pressedKey == ord('c'):
            points = []
            copy_image = rectifyied.copy()
    
    cv.destroyAllWindows()


def get_points(image, ref_image):
    """
    Get the points of reference and the points to be rectifyied
    in the image"""
    print("Select 4 points in the image to be rectifyed and 4 points in the reference image")
    points_to_rectify = []
    ref_points = []

    copy_image = image.copy()
    copy_ref_image = ref_image.copy()

    def funImg(event, x, y, flags, param):
        """
        Callback function for the mouse event in the reference image"""
        if (event == cv.EVENT_LBUTTONDOWN 
            and len(ref_points) < 4):
            ref_points.append((x,y))
            cv.putText(copy_ref_image, str(len(ref_points)), (x,y),
                          cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv.circle(copy_ref_image, (x,y), 5, (0,0,255), -1)
    
    def funImgRef(event, x, y, flags, param):
        """
        Callback function for the mouse event in the image"""
        if (event == cv.EVENT_LBUTTONDOWN 
            and len(points_to_rectify) < 4):
            points_to_rectify.append((x,y))
            cv.putText(copy_image, str(len(points_to_rectify)), (x,y), 
                       cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv.circle(copy_image, (x,y), 5, (0,0,255), -1)
    
    cv.namedWindow('Reference image')
    cv.setMouseCallback('Reference image', funImg)
    
    cv.namedWindow('Image')
    cv.setMouseCallback('Image', funImgRef)

    while True:
        cv.imshow('Reference image', copy_ref_image)
        cv.imshow('Image', copy_image)
        
        pressedKey = cv.waitKey(1) & 0xFF
        if pressedKey == ord('q'):
            break
        elif pressedKey == ord('c'):
            ref_points = []
            points_to_rectify = []
            copy_image = image.copy()
            copy_ref_image = ref_image.copy()
    
    cv.destroyAllWindows()

    if(len(points_to_rectify) != 4 or len(ref_points) != 4):
        raise ValueError("You must select 4 points in each image")
    
    return points_to_rectify, ref_points


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Rectify a plane given 4 points of reference in the image to be rectifyed and in an already rectifyied image')
    parser.add_argument('image', help='Image to be rectifyed')
    parser.add_argument('image_ref', help='Reference image')
    args = parser.parse_args()


    image = cv.imread(args.image)
    ref_image = cv.imread(args.image_ref)

    scale = ask_for_measure(ref_image)

    points, ref_points = get_points(image, ref_image)
    rec = rectify(image, ref_image, points, ref_points)
    get_final_measure(rec, scale)
