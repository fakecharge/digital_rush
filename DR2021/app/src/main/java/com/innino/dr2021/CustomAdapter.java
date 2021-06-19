package com.innino.dr2021;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.TextView;

import androidx.cardview.widget.CardView;

public class CustomAdapter extends BaseAdapter {
    Context context;
    String[] trainers;
    LayoutInflater inflter;

    public CustomAdapter(Context applicationContext, String[] trainers) {
        this.context = applicationContext;
        this.trainers = trainers;
        inflter = (LayoutInflater.from(applicationContext));
    }
    @Override
    public int getCount() {
        return trainers.length;
    }

    @Override
    public Object getItem(int position) {
        return null;
    }

    @Override
    public long getItemId(int position) {
        return 0;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        convertView = inflter.inflate(R.layout.custom_spinner, null);
        TextView btn = convertView.findViewById(R.id.textView);
        btn.setText(trainers[position]);
        return convertView;
    }
}
