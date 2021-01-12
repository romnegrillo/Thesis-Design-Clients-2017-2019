package com.example.rom.opencv;

// Import modules.

import android.content.pm.ActivityInfo;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import org.opencv.android.CameraBridgeViewBase;
import org.opencv.android.JavaCameraView;
import org.opencv.android.OpenCVLoader;
import org.opencv.core.Mat;
import org.opencv.core.Scalar;

import java.util.Locale;

// Implement the Camera BridgeViewBase.CvCameraViewListener so that this class
// can use the CameraBridgeViewBase
public class MainActivity extends AppCompatActivity implements CameraBridgeViewBase.CvCameraViewListener2 {

    // Class fields.

    // Create the CameraBridgeViewBase
    // This object will be the bridge between the JavaCameraView and OpenCV
    CameraBridgeViewBase cameraBridgeViewBase;

    // Buttons
    Button rgbButton, binaryButton, labButton, captureButton;

    // Seekbar
    SeekBar seekBar;

    // Labels
    TextView thresholdLabel, maturityStageLabel, lifeExpectancyLabel, aStarLabel, aveRGBLabel, aveLABLabel,
            nutritionalContentLabel, suggestedUseLabel;

    // Variables used to switch color space view.
    int ctr = 1;

    // Threshold starting reference.
    int threshold = 100;

    // Object for classifying tomato.
    TomatoClassifier tomatoClassifier;

    // This function executes whenever the app is first run.
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // Make the view portrait.
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);

        // Check if OpenCV can be loaded.
        if (OpenCVLoader.initDebug()) {
            Toast.makeText(getApplicationContext(), "Open CV Loaded!", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(getApplicationContext(), "Open could not be loaded!", Toast.LENGTH_SHORT).show();
        }

        // Tomato classifier object.
        tomatoClassifier = new TomatoClassifier();

        // Connect the cameraBridgeViewBase to the JavaCameraView that is create in the XML file.
        // It is disabled by default to we enable it.
        cameraBridgeViewBase = (JavaCameraView) findViewById(R.id.myCamView);
        cameraBridgeViewBase.setVisibility(SurfaceView.VISIBLE);
        cameraBridgeViewBase.enableView();

        // Connect a listener to the current instance of the object which is basically this class.
        cameraBridgeViewBase.setCvCameraViewListener(this);

        // Connect the buttons in the XML.
        rgbButton = findViewById(R.id.rgbButton);
        binaryButton = findViewById(R.id.binaryButton);
        labButton = findViewById(R.id.labButton);
        captureButton = findViewById(R.id.captureButton);

        // Button listeners.
        rgbButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ctr = 1;
            }
        });

        binaryButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ctr = 2;
            }
        });

        labButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ctr = 3;
            }
        });

        captureButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {

                Scalar meanRGB = tomatoClassifier.getMeanRGB();
                Scalar meanLAB = tomatoClassifier.getMeanLAB();
                double meanAStar = tomatoClassifier.getMeanAStar();

                aveRGBLabel.setText(String.format(Locale.US,"(%.2f, %.2f, %.2f)", meanRGB.val[0], meanRGB.val[1], meanRGB.val[2]));
                aveLABLabel.setText(String.format(Locale.US,"(%.2f, %.2f, %.2f)", meanLAB.val[0], meanLAB.val[1], meanLAB.val[2]));
                aStarLabel.setText(String.format(Locale.US,"%.2f", meanAStar));
                maturityStageLabel.setText(tomatoClassifier.getMaturity());
                lifeExpectancyLabel.setText(tomatoClassifier.getLifeExpectancy());
                nutritionalContentLabel.setText(tomatoClassifier.getNutrionalContent());
                suggestedUseLabel.setText(tomatoClassifier.getSuggestedUse());


            }
        });

        // Connect the labels in XML.
        thresholdLabel = findViewById(R.id.thresholdLabel);
        maturityStageLabel = findViewById(R.id.maturityStageLabel);
        lifeExpectancyLabel = findViewById(R.id.lifeExpectancyLabel);
        aStarLabel = findViewById(R.id.aStarLabel);
        aveRGBLabel = findViewById(R.id.aveRGBLabel);
        aveLABLabel = findViewById(R.id.aveLabLabel);
        nutritionalContentLabel = findViewById(R.id.nutritionalContentLabel);
        suggestedUseLabel = findViewById(R.id.suggestedUseLabel);

        // Default text labels.
        thresholdLabel.setText(String.format(Locale.US,"%s",threshold));
        maturityStageLabel.setText("-");
        lifeExpectancyLabel.setText("-");
        aStarLabel.setText("-");
        aveRGBLabel.setText("-");
        aveLABLabel.setText("-");
        nutritionalContentLabel.setText("-");
        suggestedUseLabel.setText("-");

        // Seekbar for adjusting threshold.
        seekBar = findViewById(R.id.seekBar);
        seekBar.setMax(255);
        seekBar.setProgress(100);

        // Seekbar event listener.
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int i, boolean b) {
                threshold = i;
                thresholdLabel.setText(String.format(Locale.US,"%s",threshold));
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                // No action.
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // No action.
            }
        });
    }

    // This function receives the frames from the camera and returns it to
    // the JavaCameraView and displayed.
    // All image processing tasks is displayed here.
    @Override
    public Mat onCameraFrame(CameraBridgeViewBase.CvCameraViewFrame inputFrame) {

        // Garbage collector.
        System.gc();

        try {
            tomatoClassifier.processImage(inputFrame, threshold);

            if (ctr == 1) {
                return tomatoClassifier.getRGBFrame();
            } else if (ctr == 2) {
                return tomatoClassifier.getBinarizedFrame();
            } else if (ctr == 3) {
                return tomatoClassifier.getLABFrame();
            }
        } catch (Exception exp) {
            return tomatoClassifier.getRGBFrame();
        }
        return tomatoClassifier.getRGBFrame();
    }

    // Called whenever the camera is closed.
    @Override
    public void onCameraViewStopped() {
        tomatoClassifier.cameraClosed();
    }

    // Called whenever the camera is started.
    // We instantiate the Mat objects here.
    @Override
    public void onCameraViewStarted(int width, int height) {
        tomatoClassifier.cameraOpened(height, width);
    }

    @Override
    protected void onPause() {
        super.onPause();

        if (cameraBridgeViewBase != null) {
            cameraBridgeViewBase.disableView();
        }
    }

    // Called again when the camera is clicked, it will resume the view.
    @Override
    protected void onResume() {
        super.onResume();

        if (OpenCVLoader.initDebug()) {
            Toast.makeText(getApplicationContext(), "Open CV Loaded!", Toast.LENGTH_SHORT).show();
            cameraBridgeViewBase.enableView();
        } else {
            Toast.makeText(getApplicationContext(), "Open could not be loaded!", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

        if (cameraBridgeViewBase != null) {
            cameraBridgeViewBase.disableView();
        }
    }
}
