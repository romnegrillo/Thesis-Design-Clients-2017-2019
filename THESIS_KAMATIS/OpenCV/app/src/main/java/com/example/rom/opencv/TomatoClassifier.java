package com.example.rom.opencv;

// Module imports
import org.opencv.android.CameraBridgeViewBase;
import org.opencv.core.Mat;
import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.MatOfPoint;
import org.opencv.core.Scalar;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import org.opencv.core.Size;

import java.util.ArrayList;
import java.util.List;

public class TomatoClassifier {
    // Fields for For changing the orientation of the frame
    // because OpenCV in Android is displayed as landscape by default.
    private Mat mRgba;
    private Mat mRgbaF;
    private Mat mRgbaT;

    // Fields for image processing.
    private Mat imgOrig, imgOrigBGR, gray, blurred, binarized, imgLAB, imgHSV, maskedLab, maskedRGB, maskedHSV, newMask, binCopy,
    mask1,mask2,maskCpy;

    // For accessing scalars.
    private Scalar meanRGB, meanLAB;
    private double meanAStar;

    // Starting color range in HSV for red, orange, yellow and green.
    // Saturation is adjustable using threshold.
    Scalar colorRange1Low=new Scalar(0, 50, 100);
    Scalar colorRange1High=new Scalar(100, 255, 255);

    Scalar colorRange2Low=new Scalar(170, 50, 100);
    Scalar colorRange2High=new Scalar(180, 255, 255);

    // Constructor
    // No argument required.
    TomatoClassifier() {
    }

    // Method called whenever camera is first started.
    // Here we initialize/reinitialized the Mat objects
    // when the camera is loaded/reloaded.
    public void cameraOpened(int height, int width) {
        mRgba = new Mat(height, width, CvType.CV_8UC4);
        mRgbaF = new Mat(height, width, CvType.CV_8UC4);
        mRgbaT = new Mat(width, width, CvType.CV_8UC4);

        imgOrig = new Mat(width, height, CvType.CV_8UC3);
        imgOrigBGR = new Mat(width, height, CvType.CV_8UC3);
        gray = new Mat(width, height, CvType.CV_8U);
        blurred = new Mat(width, height, CvType.CV_8U);
        binarized = new Mat(width, height, CvType.CV_8U);
        imgLAB = new Mat(width, height, CvType.CV_8UC3);
        imgHSV = new Mat(width, height, CvType.CV_8UC3);
        maskedLab = new Mat(width, height, CvType.CV_8UC3);
        maskedRGB = new Mat(width, height, CvType.CV_8UC3);

        maskedHSV = new Mat(width, height, CvType.CV_8UC3);
        newMask = new Mat(width, height, CvType.CV_8U);

        binCopy = new Mat(width, height, CvType.CV_8U);

    }

    // Method called when the camera is closed.
    // It just clears the data form the Mat objects.
    public void cameraClosed() {
        mRgba.release();
        mRgbaF.release();
        mRgbaT.release();

        imgOrig.release();
        imgOrigBGR.release();
        gray.release();
        blurred.release();
        binarized.release();
        imgLAB.release();
        imgHSV.release();

        maskedLab.release();
        maskedRGB.release();

        maskedHSV.release();
        newMask.release();

        binCopy.release();

        mask1.release();
        mask2.release();
    }

    // Process the image along with the specified threshold value chosen.
    public void processImage(CameraBridgeViewBase.CvCameraViewFrame inputFrame, int threshold) {

        colorRange1Low=new Scalar(0, threshold, 50);
        colorRange1High=new Scalar(100, 255, 255);

        colorRange2Low=new Scalar(170, threshold, 50);
        colorRange2High=new Scalar(180, 255, 255);

        // Get the image from the OpenCV Camera.
        mRgba=inputFrame.rgba();

        // Rotate mRgba 90 degrees because the default orientation
        // of OpenCV Camera is on landscape.
        Core.transpose(mRgba, mRgbaT);

        // Resize the transposed image to fit the width.
        Imgproc.resize(mRgbaT, mRgbaF, mRgbaF.size(), 0, 0, 0);
        Core.flip(mRgbaF, mRgba, 1);

        // Read the current frames.
        // All the rest of the code is patterned just like OpenCV in Python RPi.
        Imgproc.cvtColor(mRgba, imgOrig, Imgproc.COLOR_RGBA2RGB);
        Imgproc.cvtColor(imgOrig, imgOrigBGR, Imgproc.COLOR_RGBA2BGR);
        Imgproc.cvtColor(imgOrigBGR, imgLAB, Imgproc.COLOR_BGR2Lab);
        Imgproc.cvtColor(imgOrigBGR, imgHSV, Imgproc.COLOR_BGR2HSV);
        Imgproc.cvtColor(imgOrigBGR, gray, Imgproc.COLOR_BGR2GRAY);
        Imgproc.GaussianBlur(gray, blurred, new Size(5, 5), 0);


        /*
        // This block is removed from code to use HSV color detect instead.
        ///////////////////////////////////////////////////////////////////////////////////////
        Imgproc.threshold(blurred, binarized, threshold, 255, Imgproc.THRESH_BINARY_INV);

        // NOTE: The bitwise operator with mask only returns value of pixels that
        // are in the mask. Therefore, frames that previously have content will
        // not be overwritten if new value for that position is returned.
        // To solve that we reinitialized the object Mat.

        // Once the binary image for the threshold is obtained, we have obtained the ROI (tomato).
        // From the ROI, convert it to HSV and remove the black parts.
        // From the HSV ROI image, use inRange() function to return only the non-black parts.
        // New mask is now created.
        // Use the new mask to create new ROI which does not include black parts now.

        maskedRGB = new Mat(imgOrig.width(), imgOrig.height(), CvType.CV_8UC3);
        maskedLab = new Mat(imgOrig.width(), imgOrig.height(), CvType.CV_8UC3);

        Core.bitwise_and(imgOrigBGR, imgOrigBGR, maskedRGB, binarized);
        Imgproc.cvtColor(maskedRGB, maskedHSV, Imgproc.COLOR_BGR2HSV);
        Core.inRange(maskedHSV, new Scalar(0, 0, 0), new Scalar(255, 255, 30), newMask);

        // hsv will return all the black parts, we invert it to remove that black parts from
        // white pixels of the mask then we bitwise AND it again to the original mask.
        Core.bitwise_not(newMask, newMask);
        Core.bitwise_and(newMask, newMask, binarized);

        ///////////////////////////////////////////////////////////////////////////////////////
        */
        maskedRGB = new Mat(imgOrig.width(), imgOrig.height(), CvType.CV_8UC3);
        maskedLab = new Mat(imgOrig.width(), imgOrig.height(), CvType.CV_8UC3);

        // Get RED, GREEN and YELLOW colors in between.
        mask1=new Mat(mRgba.width(), mRgba.height(), CvType.CV_8U);
        mask2=new Mat(mRgba.width(), mRgba.height(), CvType.CV_8U);
        newMask=new Mat(mRgba.width(), mRgba.height(), CvType.CV_8U);

        Core.inRange(imgHSV,colorRange1Low,colorRange1High,mask1);
        Core.inRange(imgHSV,colorRange2Low,colorRange2High,mask2);
        Core.bitwise_or(mask1,mask2,newMask);

        maskCpy=new Mat(mRgba.width(), mRgba.height(), CvType.CV_8U);
        newMask.copyTo(maskCpy);
        List<MatOfPoint> cnts = new ArrayList<>();

        Imgproc.findContours(maskCpy,cnts, new Mat(),Imgproc.RETR_EXTERNAL, Imgproc.CHAIN_APPROX_SIMPLE);

        double maxVal = 0;
        int maxValIdx = 0;

        for(int i=0; i<cnts.size(); i++)
        {
            double contourArea = Imgproc.contourArea(cnts.get(i));

            if (maxVal < contourArea)
            {
                maxVal = contourArea;
                maxValIdx = i;
            }
        }

        //newMask=new Mat(mRgba.width(), mRgba.height(), CvType.CV_8U);

        Mat mask = new Mat( new Size( mRgba.cols(), mRgba.rows() ), CvType.CV_8UC1 );
        mask.setTo( new Scalar( 0.0 ) );
        mask.copyTo(newMask);

        Imgproc.drawContours(newMask,cnts,maxValIdx,new Scalar(255),-1);

        // Get the new mask.
        Core.bitwise_and(imgOrig, imgOrig, maskedRGB, newMask);
        Core.bitwise_and(imgLAB, imgLAB, maskedLab, newMask);

        meanRGB = Core.mean(maskedRGB, newMask);
        meanLAB = Core.mean(maskedLab, newMask);
        meanAStar = meanLAB.val[1];
    }

    public Mat getRGBFrame() {
        return imgOrig;
    }

    public Mat getBinarizedFrame() {
        return newMask;
    }

    public Mat getLABFrame() {
        return maskedLab;
    }

    public Scalar getMeanRGB() {
        return meanRGB;
    }

    public Scalar getMeanLAB() {
        return meanLAB;
    }

    public double getMeanAStar() {
        return meanAStar;
    }


//               Reference Table
//
//                    a*<-5.8            10%-20% Maturity, Breaker
//                    -5.8<=a*<2.1       30%-40% Maturity, Turning
//                    2.1<=a*<9.2        50%-60% Maturity, Pink
//                    9.2<=a*<21.5       70%-80% Maturity, Light Red
//                    21.5<=a*           Full maturity, Red
//
//               Edited reference because image is read as 8-bit unsigned integer.
//
//                    a*<121.2           10%-20% Maturity, Breaker
//                    121.2<=a*129.1     30%-40% Maturity, Turning
//                    129.1<=a*<136.2    50%-60% Maturity, Pink
//                    136.2<=a*<148.5    70%-80% Maturity, Light Red
//                    148.5<-a*          Full maturity, Red

    public String getMaturity() {

        if (meanAStar < 121.2) {
            return "Breaker";

        } else if (meanAStar >= 121.2 && meanAStar < 129.1) {
            return "Turning";

        } else if (meanAStar >= 129.1 && meanAStar < 136.2) {
            return "Pink";

        } else if (meanAStar >= 136.2 && meanAStar < 148.5) {
            return "Light Red";

        } else if (meanAStar >= 148.5) {
            return "Red";
        }

        return "Unknown";
    }

    public String getLifeExpectancy() {

        if (meanAStar < 121.2) {
            return "6~10 Days";
        } else if (meanAStar >= 121.2 && meanAStar < 129.1) {
            return "4~7 Days";
        } else if (meanAStar >= 129.1 && meanAStar < 136.2) {
            return "2~5 Days";
        } else if (meanAStar >= 136.2 && meanAStar < 148.5) {
            return "1~2 Days";
        } else if (meanAStar >= 148.5) {
            return "0 Days";
        }

        return "Unknown";
    }

    public String getSuggestedUse()
    {
        if (meanAStar < 121.2) {
            return "1~2 Days Before Turning";
        } else if (meanAStar >= 121.2 && meanAStar < 129.1) {
            return "2~3 Days Before Pink";
        } else if (meanAStar >= 129.1 && meanAStar < 136.2) {
            return "1~3 Days Before Light Red";
        } else if (meanAStar >= 136.2 && meanAStar < 148.5) {
            return "1~2 Days Before Red";
        } else if (meanAStar >= 148.5) {
            return "Fully Matured";
        }

        return "Unknown";
    }

    public String getNutrionalContent()
    {
        if (meanAStar < 121.2) {
            return "Crude Fiber: 1.32%\n" +
                    "Potassium: 2065 mg/kg\n";
        } else if (meanAStar >= 121.2 && meanAStar < 129.1) {
            return "Crude Fiber: 1.12%\n" +
                    "Potassium: 1487 mg/kg\n";
        } else if (meanAStar >= 129.1 && meanAStar < 136.2) {
            return "Crude Fiber: 0.19%\n" +
                    "Potassium: 1619 mg/kg\n";
        } else if (meanAStar >= 136.2 && meanAStar < 148.5) {
            return "Crude Fiber: 1.17%\n" +
                    "Potassium: 2028 mg/kg\n";
        } else if (meanAStar >= 148.5) {
            return "Crude Fiber: 0.45%\n" +
                    "Potassium: 1844 mg/kg\n";
        }

        return "Unknown";
    }
}
