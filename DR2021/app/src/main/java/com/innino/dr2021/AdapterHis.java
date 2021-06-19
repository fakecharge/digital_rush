package com.innino.dr2021;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.cardview.widget.CardView;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class AdapterHis extends RecyclerView.Adapter<AdapterHis.ViewHolder> {

    List<HistoryEntitle> histories;
    AdapterHis(List<HistoryEntitle> histories){
        this.histories = histories;
    }

    @NonNull
    @Override
    public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext()).inflate(R.layout.card_history, parent, false);
        ViewHolder viewHolder = new ViewHolder(v);
        return viewHolder;
    }

    @Override
    public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
        holder.top_D.setText(histories.get(position).td);
        holder.down_D.setText(histories.get(position).dd);
        holder.bpm.setText(histories.get(position).bpm);
        holder.time.setText(histories.get(position).time);
    }

    @Override
    public void onAttachedToRecyclerView(RecyclerView recyclerView) {
        super.onAttachedToRecyclerView(recyclerView);
    }

    @Override
    public int getItemCount() {
        return histories.size();
    }

    public static class ViewHolder extends RecyclerView.ViewHolder {
        TextView top_D;
        CardView cv;
        TextView down_D;
        TextView bpm;
        TextView time;

        public ViewHolder(View view) {
            super(view);
            // Define click listener for the ViewHolder's View
            cv = view.findViewById(R.id.card_view);

            top_D = (TextView) view.findViewById(R.id.vd);
            down_D = (TextView) view.findViewById(R.id.nd);
            bpm = (TextView) view.findViewById(R.id.bpm_t);
            time = (TextView) view.findViewById(R.id.time);
        }
    }
}
