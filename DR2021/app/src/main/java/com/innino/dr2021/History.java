package com.innino.dr2021;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.content.ContentValues;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

public class History extends AppCompatActivity {
    DBHelper dbHelper;
    SQLiteDatabase db;
    RecyclerView rv;
    List<HistoryEntitle> entitles = new ArrayList<HistoryEntitle>() {};
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_history);
        dbHelper = new DBHelper(History.this);
        db = dbHelper.getWritableDatabase();
        rv = findViewById(R.id.rv);
        rv.setHasFixedSize(true);
        LinearLayoutManager llm = new LinearLayoutManager(History.this);
        rv.setLayoutManager(llm);
        HistoryEntitle test = new HistoryEntitle("22", "11", "22",
                new SimpleDateFormat("yyyyMMdd_HHmmss").format(Calendar.getInstance().getTime()).toString());
        entitles.add(test);
        AdapterHis adapter = new AdapterHis(entitles);
        rv.setAdapter(adapter);
    }
}