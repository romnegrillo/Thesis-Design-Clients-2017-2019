import cv2
import numpy as np
import os

# 66 percent, 2 doctors directory.
doctor_66_light_dir = "./66/Light"
doctor_66_moderate_dir = "./66/Moderate"
doctor_66_severe_dir = "./66/Severe"

# 100 percent, 3 doctors directory
doctor_100_light_dir = "./100/Light"
doctor_100_moderate_dir = "./100/Moderate"
doctor_100_severe_dir = "./100/Severe"

# Not measales directory
not_measalaes_dir = "./not_measeles"

dir_list = []
dir_list.append(doctor_66_light_dir)
dir_list.append(doctor_66_moderate_dir)
dir_list.append(doctor_66_severe_dir)
dir_list.append(doctor_100_light_dir)
dir_list.append(doctor_100_moderate_dir)
dir_list.append(doctor_100_severe_dir)
dir_list.append(not_measalaes_dir)

##for dir_image in dir_list:
##    print(dir_image)

with open("data.csv","w") as f:
    f.write("filename,doctor_evaluation,severity,numpixel_image,numpixel_red,numpixel_skin,unknown_pixel,severity_percentage,anded"+"\n")

with open("data.csv","a") as f:
    
    for dir_image in dir_list:
        
        for fileName in os.listdir(dir_image):

            if "red.jpg" in fileName:
                continue

            rel_filename = dir_image+"/"+fileName
            print(rel_filename)
            
            img = cv2.imread(dir_image+"/"+fileName)
            #cv2.imshow("img", img)
            

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            #cv2.imshow("hsv", hsv)
            cv2.imwrite(rel_filename+"_hsv.jpg", hsv)

            # Red range.
            low_red_1 = np.array([0, 100, 100], dtype="uint8")
            high_red_1 = np.array([8, 255, 255], dtype="uint8")
            red_mask_1 = cv2.inRange(hsv, low_red_1, high_red_1)

            low_red_2 = np.array([160, 100, 100], dtype="uint8")
            high_red_2 = np.array([179, 255, 255], dtype="uint8")
            red_mask_2 = cv2.inRange(hsv, low_red_2, high_red_2)

            # Brown skin range.
            low_brown = np.array([0, 48, 80], dtype="uint8")
            high_brown = np.array([20, 255, 255], dtype="uint8")

            total_red_mask = cv2.bitwise_or(red_mask_1, red_mask_2)
            cv2.imwrite(rel_filename+"_red_mask.jpg", total_red_mask)
            red_detected = cv2.bitwise_and(img, img, mask=total_red_mask)
            #cv2.imshow("red", red_detected)
            cv2.imwrite(rel_filename+"_red.jpg",red_detected)

            total_brown_mask = cv2.inRange(hsv, low_brown, high_brown)
            cv2.imwrite(rel_filename+"_brown_mask.jpg", total_brown_mask)
            brown_detected = cv2.bitwise_and(img, img, mask=total_brown_mask)
            #cv2.imshow("brown", brown_detected)
            cv2.imwrite(rel_filename+"_brown.jpg", brown_detected)

            allSkinMask=cv2.bitwise_or(total_red_mask,total_brown_mask)
            andDetected = cv2.bitwise_and(img, img, mask=allSkinMask)
            cv2.imwrite(rel_filename+"_ANDED.jpg", allSkinMask)

            
            numpixel_image = img.shape[0]*img.shape[1]
            numpixel_red = cv2.countNonZero(total_red_mask)
            numpixel_brown = cv2.countNonZero(total_brown_mask)
            unknown_pixels = numpixel_image -  numpixel_red - numpixel_brown
            andedpixels = cv2.countNonZero(allSkinMask)
            try:
                severity_percentage = (numpixel_red/(numpixel_red+numpixel_brown))*100
            except:
                severity_percentage=0
                
            print(f"Total image pixels: {numpixel_image}")
            print(f"Total red pixels: {numpixel_red}")
            print(f"Total skin pixels: {numpixel_brown}")
            print(f"Unknown Pixels: {unknown_pixels}")
            print(f"Severity: {severity_percentage}")             
            print("")

            to_write = rel_filename
            to_write += ","
            to_write += "<doctor_evaluation>"
            to_write += ","
            to_write += "<severity>"
            to_write += ","
            to_write += str(numpixel_image)
            to_write += ","
            to_write += str(numpixel_red)
            to_write += ","
            to_write += str(numpixel_brown)
            to_write += ","
            to_write += str(unknown_pixels)
            to_write += ","
            to_write += str(severity_percentage)
            to_write += ","
            to_write += str(andedpixels)
            

            if dir_image == doctor_66_light_dir:
                to_write=to_write.replace("<doctor_evaluation>", "66")
                to_write=to_write.replace("<severity>", "light")
            elif dir_image == doctor_66_moderate_dir:
                to_write=to_write.replace("<doctor_evaluation>", "66")
                to_write=to_write.replace("<severity>", "moderate")
            elif dir_image == doctor_66_severe_dir:
                to_write=to_write.replace("<doctor_evaluation>", "66")
                to_write=to_write.replace("<severity>", "severe")
            elif dir_image == doctor_100_light_dir:
                to_write=to_write.replace("<doctor_evaluation>", "100")
                to_write=to_write.replace("<severity>", "light")
            elif dir_image == doctor_100_moderate_dir:
                to_write=to_write.replace("<doctor_evaluation>", "100")
                to_write=to_write.replace("<severity>", "moderate")
            elif dir_image == doctor_100_severe_dir:
                to_write=to_write.replace("<doctor_evaluation>", "100")
                to_write=to_write.replace("<severity>", "severe")
            elif dir_image == not_measalaes_dir:
                to_write=to_write.replace("<doctor_evaluation>", "not_measles")
                to_write=to_write.replace("<severity>", "not_measles")

            f.write(to_write+"\n")
        

cv2.waitKey(0)
cv2.destroyAllWindows
