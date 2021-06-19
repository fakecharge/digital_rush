package com.innino.dr2021;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main);
        Intent intent = new Intent(MainActivity.this, Second.class);
//        intent.putExtra("UserID", userId.getText().toString());
        startActivity(intent);
    }
}