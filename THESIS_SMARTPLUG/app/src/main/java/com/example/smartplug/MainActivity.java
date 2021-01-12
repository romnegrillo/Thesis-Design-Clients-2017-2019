package com.example.smartplug;

import android.graphics.Color;
import android.support.annotation.NonNull;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.mikhaellopez.circularprogressbar.CircularProgressBar;

public class MainActivity extends AppCompatActivity {

    // Firebase connections ===============================================
    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference ref = database.getReference();

    DatabaseReference modeRef = ref.child("mode");
    DatabaseReference tempRef = ref.child("temperature");
    DatabaseReference humidRef = ref.child("humidity");
    DatabaseReference heatRef = ref.child("heat_index");
    DatabaseReference modeSwitchRef = ref.child("mode");
    DatabaseReference airconSwitchRef = ref.child("aircon");
    DatabaseReference humidSwitchRef = ref.child("humidifier");


    // ====================================================================

    // GUI objects ========================================================
    CircularProgressBar tempProgressBar, humidProgressBar; //, heatProgressBar;
    TextView tempTextView, humidTextView, statusTextView; // heatTextView;
    Switch modeSwitch, airconSwitch, humidSwitch;
    // ====================================================================


    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        loadGUIObjects();
        loadCircularProgressBar();

        ref.child(".info/connected").addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {

                Toast.makeText(getApplicationContext(), dataSnapshot.getValue().toString(), Toast.LENGTH_LONG).show();

                if(dataSnapshot.getValue().toString()=="true")
                {
                    statusTextView.setText("CONNECTED");
                    statusTextView.setTextColor(Color.GREEN);
                }
                else
                {
                    statusTextView.setText("DISCONNECTED");
                    statusTextView.setTextColor(Color.RED);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {


            }
        });



        // Progressbar listeners

        modeRef.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                String mode = dataSnapshot.getValue().toString();

                Toast.makeText(getApplicationContext(), "Last Mode: " +  mode, Toast.LENGTH_LONG).show();

                if(mode.equals("MANUAL"))
                {
                    Toast.makeText(getApplicationContext(), "DEBUG", Toast.LENGTH_LONG).show();

                    modeSwitch.setText("MODE (MANUAL):");
                    modeSwitch.setChecked(false);

                    airconSwitch.setEnabled(true);
                    humidSwitch.setEnabled(true);


                }
                else
                {
                    modeSwitch.setText("MODE (AUTO):");
                    modeSwitch.setChecked(true);

                    airconSwitch.setEnabled(false);
                    humidSwitch.setEnabled(false);

                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });



        tempRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                tempTextView.setText(dataSnapshot.getValue().toString() + "\nC");
                tempProgressBar.setProgressWithAnimation(Float.parseFloat(dataSnapshot.getValue().toString()), (long) 1000); // =1s
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        humidRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                humidTextView.setText(dataSnapshot.getValue().toString() + "\n%");
                humidProgressBar.setProgressWithAnimation(Float.parseFloat(dataSnapshot.getValue().toString()), (long) 1000); // =1s
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

//        heatRef.addValueEventListener(new ValueEventListener() {
//            @Override
//            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
//                heatTextView.setText(dataSnapshot.getValue().toString() + "\nC");
//                heatProgressBar.setProgressWithAnimation(Float.parseFloat(dataSnapshot.getValue().toString()), (long) 1000); // =1s
//            }
//
//            @Override
//            public void onCancelled(@NonNull DatabaseError databaseError) {
//            }
//        });

        modeSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked)
                {
                    // AUTO MODE
                    // Disable switch from aircon and humid.
                    // Let the values change by the device from parameter condition.

                    modeSwitchRef.setValue("AUTO");
                    modeSwitch.setChecked(true);

                    modeSwitch.setText("MODE (AUTO):");


                    airconSwitch.setEnabled(false);
                    humidSwitch.setEnabled(false);



                }
                else
                {
                    // MANUAL MODE
                    // Enable switch from aircon and humid.
                    // Switch off all the plugs first then it can be controlled manually.

                    modeSwitchRef.setValue("MANUAL");
                    modeSwitch.setChecked(false);

                    modeSwitch.setText("MODE (MANUAL):");


                    airconSwitch.setEnabled(true);
                    humidSwitch.setEnabled(true);


                }
            }
        });



        airconSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked)
                {
                    airconSwitchRef.setValue("ON");
                }
                else
                {
                    airconSwitchRef.setValue("OFF");
                }

            }
        });

        humidSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(isChecked)
                {
                    humidSwitchRef.setValue("ON");
                }
                else
                {
                    humidSwitchRef.setValue("OFF");
                }
            }
        });

        airconSwitchRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                if(dataSnapshot.getValue().toString().equals("ON"))
                {
                    airconSwitch.setText("AIRCON (ON):");
                    airconSwitch.setChecked(true);
                }
                else
                {
                    airconSwitch.setText("AIRCON (OFF):");
                    airconSwitch.setChecked(false);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

        humidSwitchRef.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                if(dataSnapshot.getValue().toString().equals("ON"))
                {
                    humidSwitch.setText("HUMIDIFIER (ON):");
                    humidSwitch.setChecked(true);
                }
                else
                {
                    humidSwitch.setText("HUMIDIFIER (OFF):");
                    humidSwitch.setChecked(false);
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });

    }

    private void loadGUIObjects()
    {
        tempTextView = findViewById(R.id.tempTextView);
        humidTextView = findViewById(R.id.humTextView);
        //heatTextView = findViewById(R.id.heatTextView);
        statusTextView = findViewById(R.id.statusTextView);

        tempProgressBar = findViewById(R.id.tempProgressBar);
        humidProgressBar = findViewById(R.id.humProgressBar);
        //heatProgressBar = findViewById(R.id.heatProgressBar);

        modeSwitch = findViewById(R.id.modeSwitch);
        airconSwitch = findViewById(R.id.airconSwitch);
        humidSwitch = findViewById(R.id.humidSwitch);

        modeSwitch.setChecked(true);
        airconSwitch.setEnabled(false);
        humidSwitch.setEnabled(false);

    }

    private void loadCircularProgressBar()
    {
        tempProgressBar.setProgressWithAnimation(0f, (long) 1000); // =1s
        tempProgressBar.setProgressMax(100f);
        tempProgressBar.setProgressBarColorStart(Color.GRAY);
        tempProgressBar.setProgressBarColorEnd(Color.BLUE);
        tempProgressBar.setProgressBarColorDirection(CircularProgressBar.GradientDirection.TOP_TO_BOTTOM);
        tempProgressBar.setBackgroundProgressBarColor(Color.GRAY);
        tempProgressBar.setProgressBarWidth(7f); // in DP
        tempProgressBar.setBackgroundProgressBarWidth(3f); // in DP
        tempProgressBar.setRoundBorder(true);
        tempProgressBar.setStartAngle(180f);
        tempProgressBar.setProgressDirection(CircularProgressBar.ProgressDirection.TO_RIGHT);


        humidProgressBar.setProgressWithAnimation(0f, (long) 1000); // =1s
        humidProgressBar.setProgressMax(100f);
        humidProgressBar.setProgressBarColorStart(Color.GRAY);
        humidProgressBar.setProgressBarColorEnd(Color.BLUE);
        humidProgressBar.setProgressBarColorDirection(CircularProgressBar.GradientDirection.TOP_TO_BOTTOM);
        humidProgressBar.setBackgroundProgressBarColor(Color.GRAY);
        humidProgressBar.setProgressBarWidth(7f); // in DP
        humidProgressBar.setBackgroundProgressBarWidth(3f); // in DP
        humidProgressBar.setRoundBorder(true);
        humidProgressBar.setStartAngle(180f);
        humidProgressBar.setProgressDirection(CircularProgressBar.ProgressDirection.TO_RIGHT);


//        heatProgressBar.setProgressWithAnimation(0f, (long) 1000); // =1s
//        heatProgressBar.setProgressMax(100f);
//        heatProgressBar.setProgressBarColorStart(Color.GRAY);
//        heatProgressBar.setProgressBarColorEnd(Color.BLUE);
//        heatProgressBar.setProgressBarColorDirection(CircularProgressBar.GradientDirection.TOP_TO_BOTTOM);
//        heatProgressBar.setBackgroundProgressBarColor(Color.GRAY);
//        heatProgressBar.setProgressBarWidth(7f); // in DP
//        heatProgressBar.setBackgroundProgressBarWidth(3f); // in DP
//        heatProgressBar.setRoundBorder(true);
//        heatProgressBar.setStartAngle(180f);
//        heatProgressBar.setProgressDirection(CircularProgressBar.ProgressDirection.TO_RIGHT);
    }

}
