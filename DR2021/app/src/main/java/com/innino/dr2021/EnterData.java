package com.innino.dr2021;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.ContentValues;
import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.speech.RecognizerIntent;
import android.speech.tts.TextToSpeech;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.Toast;

import com.innino.dr2021.ml.Mobilenetv2;

import org.tensorflow.lite.DataType;
import org.tensorflow.lite.support.tensorbuffer.TensorBuffer;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.List;
import java.util.Locale;

public class EnterData extends AppCompatActivity implements AdapterView.OnItemSelectedListener {
    final int bmpHeight = 416;
    final int bmpWidth = 416;
    static final int CAMERA_CODE = 1;
    Uri image_uri;
    TcpCLient mTcpClient;
    EditText upper, down, bit;
    int number_task = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_enter_data);
        upper = findViewById(R.id.upper);
        down = findViewById(R.id.down);
        bit = findViewById(R.id.bit);
        new ConnectTask().execute("");
        if (mTcpClient != null) {
            mTcpClient.sendMessage("testing");
        }
        Spinner spinner = (Spinner) findViewById(R.id.spinner);
        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.planets_array, android.R.layout.simple_spinner_item);

        spinner.setOnItemSelectedListener(this);
        String[] trainers = getResources().getStringArray(R.array.planets_array);
        CustomAdapter customAdapter=new CustomAdapter(getApplicationContext(),trainers);

        spinner.setAdapter(customAdapter);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == SPEECH_REQUEST_CODE && resultCode == RESULT_OK) {
            List<String> results = data.getStringArrayListExtra(
                    RecognizerIntent.EXTRA_RESULTS);
            String spokenText = results.get(0);
            Toast.makeText(EnterData.this, spokenText,
                    Toast.LENGTH_LONG).show();
            String[] splited = spokenText.split("\\s+");
            try {
                upper.setText(splited[0]);
                down.setText(splited[1]);
                bit.setText(splited[2]);
            } catch (Exception e) {

            }
            // Do something with spokenText.
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    private static final int SPEECH_REQUEST_CODE = 0;

    // Create an intent that can start the Speech Recognizer activity
    public void take_photo(View view) {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        startActivityForResult(intent, SPEECH_REQUEST_CODE);
    }

    public void send(View view) {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(Calendar.getInstance().getTime());
        String str = "ID " + "0 " + timeStamp + " " + upper.getText().toString() + " " +
                down.getText().toString() + " " + bit.getText().toString() + " " + number_task;
//        Toast.makeText(EnterData.this, str,
//                Toast.LENGTH_LONG).show();
        mTcpClient.sendMessage(str);
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        number_task = position;
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }

    public class ConnectTask extends AsyncTask<String, String, TcpCLient> {

        @Override
        protected TcpCLient doInBackground(String... message) {

            //we create a TCPClient object
            mTcpClient = new TcpCLient(new TcpCLient.OnMessageReceived() {
                @Override
                //here the messageReceived method is implemented
                public void messageReceived(String message) {
                    //this method calls the onProgressUpdate
                    publishProgress(message);
                }
            });
            mTcpClient.run();

            return null;
        }

        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
            //response received from server
            Log.d("test", "response " + values[0]);
            //process server response here....

        }
    }
}