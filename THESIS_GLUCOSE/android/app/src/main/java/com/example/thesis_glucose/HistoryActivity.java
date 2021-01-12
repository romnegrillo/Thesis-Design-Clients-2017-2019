package com.example.thesis_glucose;

import android.content.Context;
import android.content.DialogInterface;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class HistoryActivity extends AppCompatActivity {


    TextView dataTextView, dataTextView2;
    Button clearHistoryButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);

        dataTextView = findViewById(R.id.dataTextView);
        dataTextView2 = findViewById(R.id.dataTextView2);
        clearHistoryButton = findViewById(R.id.clearHistoryButton);

        final AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Confirm");
        builder.setMessage("Are you sure you want to clear the history?");
        builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {

            public void onClick(DialogInterface dialog, int which) {


                try {
                    OutputStreamWriter outputStreamWriter = new OutputStreamWriter(getApplicationContext().openFileOutput("data.txt", Context.MODE_PRIVATE));

                    outputStreamWriter.close();

                    String data = readFromFile(getApplicationContext());

                    dataTextView.setText(data);
                    dataTextView2.setText(data);

                } catch (IOException e) {
                    e.printStackTrace();
                }

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


        clearHistoryButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                AlertDialog alert = builder.create();
                alert.show();

            }
        });

        //writeToFile("Time: RomTest Hehe", this);

        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd hh:mm a");

        Date today = Calendar.getInstance().getTime();

        String timeNow = dateFormat.format(today);
//
//       String toWrite = "";
//        toWrite += "Insulin Needed: " + String.valueOf(20);
//       toWrite += "\n";
//        toWrite += "Glucose Level: " + String.valueOf(95.32);
//        toWrite += "\n";
//       toWrite += "Time: " + timeNow;
//        toWrite += "\n";



        //toWrite+="Time: Test";

        //writeToFile(toWrite, this);

        String data = readFromFile(this);
        String dataTime = readFromFileTime(this);

        dataTextView2.setText(data);
        dataTextView.setText(dataTime);

        Log.e("Data", data);
    }



    private void writeToFile(String data, Context context) {
        try {
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(context.openFileOutput("data.txt", Context.MODE_APPEND));
            outputStreamWriter.write(data);
            outputStreamWriter.close();
        }
        catch (IOException e) {
            Log.e("Exception", "File write failed: " + e.toString());
        }
    }

    private String readFromFile(Context context) {

        String ret = "";

        try {
            InputStream inputStream = context.openFileInput("data.txt");

            if ( inputStream != null ) {
                InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
                String receiveString = "";
                StringBuilder stringBuilder = new StringBuilder();
                List toReverse = new ArrayList();

                int counter=0;

                while ( (receiveString = bufferedReader.readLine()) != null ) {

                    //Log.e("Data", receiveString);
                    counter++;
                    if(receiveString.startsWith("Time: ")) {
                        continue;
                    }

                    receiveString = receiveString.replace("\n", "").replace("\r", "");


                    toReverse.add(receiveString);

                   //stringBuilder.append(receiveString).append("\n");
                }


                for(int i=toReverse.size()-1; i>=0; i--)
                {
                    // G3DEdit

                    stringBuilder.append(toReverse.get(i)+"\n");
                }

                inputStream.close();

                ret = ret.replace("Glucose Level:", "Glucose Level:\n");

                ret = ret.replace("Insulin Level:", "Insulin Level:\n");

                ret = stringBuilder.toString();

            }

            inputStream.close();
        }
        catch (FileNotFoundException e) {
            Log.e("login activity", "File not found: " + e.toString());
        } catch (IOException e) {
            Log.e("login activity", "Can not read file: " + e.toString());
        }


        return ret;
    }

    private String readFromFileTime(Context context) {

        String ret = "";

        try {
            InputStream inputStream = context.openFileInput("data.txt");

            if ( inputStream != null ) {
                InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
                String receiveString = "";
                StringBuilder stringBuilder = new StringBuilder();
                List toReverse = new ArrayList();

                int counter=0;

                while ( (receiveString = bufferedReader.readLine()) != null ) {

                    Log.e("Data", receiveString);

                    if(receiveString.startsWith("Time: ")) {

                        // G3DEdit
                        receiveString=receiveString.replace("Time:", "");
                        counter++;


                        // G3DEdit
                        //toReverse.add("\n"+receiveString+"\n\n\n\n");
                        toReverse.add("\n"+receiveString+"\n");


                    }


                    // stringBuilder.append(receiveString).append("\n");
                }

                //Toast.makeText(getApplicationContext(), String.valueOf(counter), Toast.LENGTH_SHORT).show();

                for(int i=toReverse.size()-1; i>=0; i--)
                {
                    stringBuilder.append(toReverse.get(i));
                }

                inputStream.close();


                ret = stringBuilder.toString();
            }

            inputStream.close();
        }
        catch (FileNotFoundException e) {
            Log.e("login activity", "File not found: " + e.toString());
        } catch (IOException e) {
            Log.e("login activity", "Can not read file: " + e.toString());
        }


        return ret;
    }
}
