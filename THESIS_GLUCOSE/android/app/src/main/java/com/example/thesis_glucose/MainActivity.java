package com.example.thesis_glucose;

import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

import android.app.AlertDialog;
import android.view.inputmethod.InputMethodManager;

public class MainActivity extends AppCompatActivity {

    Button measureButton, clearButton, saveButton;
    EditText heightEdit, weightEdit;
    TextView BMITextView, glucoseLevelTextView, insulinTextView, assessmentTextView;

    GlucoseLevelMeasurement glucObj;

    Socket s;
    String message;
    DataInputStream din;

    MyThread myThread = new MyThread();
    Thread t = new Thread(myThread);

    boolean isThreadStarted = false;
    boolean isSocketNext = false;
    boolean isDisconnectNext = false;

    int readingCtr=0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        measureButton = (Button) findViewById(R.id.measureButton);
        clearButton = (Button) findViewById(R.id.clearButton);
        saveButton = (Button) findViewById(R.id.saveButton);

        heightEdit = (EditText) findViewById(R.id.heightEdit);
        weightEdit = (EditText) findViewById(R.id.weightEdit);
        BMITextView = (TextView) findViewById(R.id.BMITextView);
        glucoseLevelTextView = (TextView) findViewById(R.id.glucoseLevelTextView);
        insulinTextView = (TextView) findViewById(R.id.insulinTextView);
        assessmentTextView= (TextView) findViewById(R.id.assessmentTextView);

        glucObj = new GlucoseLevelMeasurement();
        final AlertDialog.Builder dlgAlert = new AlertDialog.Builder(this);

        final android.support.v7.app.AlertDialog.Builder builder = new android.support.v7.app.AlertDialog.Builder(this);
        builder.setTitle("Confirm");
        builder.setMessage("Are you sure you want to save current reading?");
        builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {

            public void onClick(DialogInterface dialog, int which) {

                String BMI = BMITextView.getText().toString();
                String glucose_level = glucoseLevelTextView.getText().toString();
                String insulin_level = insulinTextView.getText().toString();

                if(!glucose_level.isEmpty() && !BMI.isEmpty() && !insulin_level.isEmpty()) {

                }

                SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm a");

                Date today = Calendar.getInstance().getTime();

                String timeNow = dateFormat.format(today);




                String toWrite = "";
                toWrite += "Insulin Needed: " + insulin_level;
                toWrite += "\n";
                toWrite += "Glucose Level: " + glucose_level;
                toWrite += "\n";
                toWrite += "Time: " + timeNow;
                toWrite += "\n";


                writeToFile(toWrite);

                dialog.dismiss();
            }
        });

        builder.setNegativeButton("NO", new DialogInterface.OnClickListener() {

            @Override
            public void onClick(DialogInterface dialog, int which) {

                // Do nothing
                dialog.dismiss();
            }
        });




        measureButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    double height = Double.parseDouble(heightEdit.getText().toString());
                    double weight = Double.parseDouble(weightEdit.getText().toString());

                    BMITextView.setText(Double.toString(glucObj.getBMILevel(weight, height)));
                } catch (Exception e) {

                    dlgAlert.setMessage("Invalid height and/or weight!");
                    dlgAlert.setTitle("Error");
                    dlgAlert.setPositiveButton("OK", null);
                    dlgAlert.setCancelable(true);
                    dlgAlert.create().show();

                    return;
                }

                try {
                    if (!isThreadStarted) {
                        t.start();
                        isThreadStarted = true;

                    }

                    if (!myThread.getStarted()) {
                        myThread.setStarted(true);
                        isSocketNext = true;
                        glucoseLevelTextView.setText(". . .");
                        insulinTextView.setText(". . .");
                        assessmentTextView.setText(". . .");
                        readingCtr=0;
                    }

                } catch (Exception e) {

                    dlgAlert.setMessage("Network error, please restart the app and connect to the device patch again.");
                    dlgAlert.setTitle("Error");
                    dlgAlert.setPositiveButton("OK", null);
                    dlgAlert.setCancelable(true);
                    dlgAlert.create().show();
                }

                InputMethodManager inputManager = (InputMethodManager)
                        getSystemService(Context.INPUT_METHOD_SERVICE);

                inputManager.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(),
                        InputMethodManager.HIDE_NOT_ALWAYS);
            }


        });

        clearButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try {
                    if (myThread.getStarted()) {
                        myThread.setStarted(false);
                        isDisconnectNext = true;
                        readingCtr=0;
                    }

                    heightEdit.setText("");
                    weightEdit.setText("");
                    BMITextView.setText("");
                    glucoseLevelTextView.setText("");
                    insulinTextView.setText("");
                    assessmentTextView.setText("");

                } catch (Exception e) {
                    Toast.makeText(getApplicationContext(), e.getMessage(), Toast.LENGTH_LONG);
                }
            }
        });

        saveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                android.support.v7.app.AlertDialog alert = builder.create();
                alert.show();

            }
        });
    }

    private void writeToFile(String data) {
        try {
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(this.openFileOutput("data.txt", this.MODE_APPEND));
            outputStreamWriter.write(data+"\n");
            outputStreamWriter.close();
        }
        catch (IOException e) {
            Log.e("Exception", "File write failed: " + e.toString());
        }
    }


    class MyThread implements Runnable {
        private boolean started = false;


        @Override
        public void run() {
            try {
                while (true) {

                    if (getStarted()) {

                        if (isSocketNext) {
                            // Connect to socket.
                            // Needs to be done on this thread.

                                s = new Socket("192.168.4.1", 8888);
                                isSocketNext = false;

                        }

                        // Get data.
                        din = new DataInputStream(s.getInputStream());
                        message = din.readLine();
                        final String NIR_reading=message;
                        readingCtr++;

                        if(readingCtr==10) {

                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {


                                    if (Double.parseDouble(message) < 3000) {
                                        glucoseLevelTextView.setText("Patch too loose!");
                                        insulinTextView.setText("-");
                                        assessmentTextView.setText("-");
                                    } else if (Double.parseDouble(message) > 7000) {
                                        glucoseLevelTextView.setText("Patch too tight!");
                                        insulinTextView.setText("-");
                                        assessmentTextView.setText("-");
                                    } else {

                                        glucObj.setGlucoseLevel(Double.parseDouble(NIR_reading));


                                        glucoseLevelTextView.setText(String.format("%.2f", glucObj.getGlucoseLevel()));
                                        insulinTextView.setText(String.format("%.2f", glucObj.getInsulin()));

                                        if(glucObj.getGlucoseLevel() < 70.0)
                                        {
                                            // Hypoglycemia
                                            assessmentTextView.setText("Hypoglycemia");
                                        }
                                        else if(glucObj.getGlucoseLevel() >= 70.0 && glucObj.getGlucoseLevel() <= 140.0 )
                                        {
                                            // Normal
                                            assessmentTextView.setText("Normal");
                                        }
                                        else
                                        {
                                            // Hyperglycemia
                                            assessmentTextView.setText("Hyperglycemia");
                                        }
                                    }

                                }
                            });



                        }
                    } else if (isDisconnectNext) {
                        s.close();
                        isDisconnectNext = false;
                    }


                    Thread.sleep(500);
                }

            } catch (Exception e) {
                Toast.makeText(getApplicationContext(), e.getMessage(), Toast.LENGTH_LONG);
            }
        }

        public void setStarted(boolean started) {
            this.started = started;
        }

        public boolean getStarted() {
            return this.started;
        }
    }
}


