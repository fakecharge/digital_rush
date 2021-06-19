package com.innino.dr2021;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.snackbar.Snackbar;

import java.util.ArrayList;

public class Second extends AppCompatActivity implements SensorEventListener {

    ArrayList<String> users;

    RecyclerView rv;
    ProgressBar progressBar, progressBar2, progressBar3;
    TextView son, steps, bpm;
    SensorManager sensorManager;
    boolean isRunning = false;


    @RequiresApi(api = Build.VERSION_CODES.N)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_second);
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        Bundle arguments = getIntent().getExtras();
//        String id_str = arguments.get("UserID").toString();
//        int id = Integer.parseInt(id_str);
        progressBar = findViewById(R.id.progressBar);
        progressBar2 = findViewById(R.id.progressBar2);
        progressBar3 = findViewById(R.id.progressBar3);
        son = findViewById(R.id.son);
        steps = findViewById(R.id.steps);
        bpm = findViewById(R.id.bpm);
        setProgressBars(1);
        setValues();
    }

    @Override
    protected void onResume()
    {
        super.onResume();
        isRunning = true;
        Sensor countSensor = sensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER);
        if (countSensor != null)
        {
            sensorManager.registerListener(this, countSensor, SensorManager.SENSOR_DELAY_UI);
        }
        else
        {
            Toast.makeText(this, "STEP_COUNTER sensor not found", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onPause()
    {
        super.onPause();
        isRunning = false;
    }

    void showSnackbar(int position) {
        Snackbar.make(rv, "Карточка с номером "+position, Snackbar.LENGTH_LONG).show();
    }

    @SuppressLint("SetTextI18n")
    void setValues() {
        int value1 = (int)(4.8 * progressBar.getProgress() / 60);
        int value2 = (int)(4.8 * progressBar.getProgress() % 60);
        int value3 = (int) ((int) 100 * progressBar2.getProgress() + Math.random() * 200 - 100);
        int value4 = (int)(1.8 * progressBar3.getProgress());

        son.setText(value1 + "h:" + value2 + "m" );
        steps.setText("" + value3);
        bpm.setText(value4 + "bpm");

    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    void setProgressBars(int id) {
        switch (id) {
            case (1) :
                progressBar.setProgress(10, true);
                progressBar2.setProgress(30, true);
                progressBar3.setProgress(50, true);
                break;
            case (2) :
                progressBar.setProgress(80, true);
                progressBar2.setProgress(70, true);
                progressBar3.setProgress(70, true);
                break;
            case (3) :
                progressBar.setProgress(100, true);
                progressBar2.setProgress(40, true);
                progressBar3.setProgress(50, true);
                break;
            default:
                progressBar.setProgress(0, true);
                progressBar2.setProgress(0, true);
                progressBar3.setProgress(0, true);
                break;
        }
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (isRunning)
        {
            steps.setText(String.valueOf(event.values[0]));
            progressBar2.setProgress((int)(event.values[0] / 100));
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    public void measurement(View view) {
        Intent intent = new Intent(Second.this, EnterData.class);
        startActivity(intent);
    }

    public void call(View view) {
        Uri call = Uri.parse("tel:89991363729");
        Intent surf = new Intent(Intent.ACTION_DIAL, call);
        startActivity(surf);
    }

    public void history(View view) {
        Intent intent = new Intent(Second.this, History.class);
        startActivity(intent);
    }
}