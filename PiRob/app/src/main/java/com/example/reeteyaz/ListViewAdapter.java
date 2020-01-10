package com.example.reeteyaz;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class ListViewAdapter extends BaseAdapter{

    Context mContext;
    LayoutInflater inflater;
    List<Model> modellist;
    ArrayList<Model> arrayList;

    //const
    public ListViewAdapter(Context context, List<Model> modellist) {
        mContext = context;
        this.modellist = modellist;
        inflater = LayoutInflater.from(mContext);
        this.arrayList = new ArrayList<Model>();
        this.arrayList.addAll(modellist);
    }

    public class ViewHolder{
        TextView mTitleTv, mDescTv;
        ImageView mIconIv;
    }

    @Override
    public int getCount() {
        return modellist.size();
    }

    @Override
    public Object getItem(int i) {
        return modellist.get(i);
    }

    @Override
    public long getItemId(int i) {
        return i;
    }

    @Override
    public View getView(final int postition, View view, ViewGroup parent) {
        ViewHolder holder;
        if (view==null){
            holder = new ViewHolder();
            view = inflater.inflate(R.layout.row, null);

            holder.mTitleTv = view.findViewById(R.id.mainTitle);
            holder.mDescTv = view.findViewById(R.id.mainDesc);
            holder.mIconIv = view.findViewById(R.id.mainIcon);

            view.setTag(holder);

        }
        else {
            holder = (ViewHolder)view.getTag();
        }
        holder.mTitleTv.setText(modellist.get(postition).getTitle());
        holder.mDescTv.setText(modellist.get(postition).getDesc());
        holder.mIconIv.setImageResource(modellist.get(postition).getIcon());

        view.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //MainMenu-------
                if (modellist.get(postition).getTitle().equals("Manuel")){ Intent intent = new Intent(mContext, NewActivity.class);
                    intent.putExtra("contentTv", "m");mContext.startActivity(intent); }
                if (modellist.get(postition).getTitle().equals("Auto")){ Intent intent = new Intent(mContext, NewActivity.class);
                    intent.putExtra("contentTv", "a");mContext.startActivity(intent); }
                if (modellist.get(postition).getTitle().equals("Bluetooth")){ Intent intent = new Intent(mContext, NewActivity.class);
                    intent.putExtra("contentTv", "b");mContext.startActivity(intent); }
            }});

        return view;
    }/*
    int maxprogramline =300;
    String[] sname=new String[maxprogramline];
    String[] scontent=new String[maxprogramline];
    int[] sid= new int[maxprogramline];
    public void adse(){
        sname[0]="Akciğer ödemi / Akut kalp yetmezliği"; scontent[0]="a1"; sid[0] =R.layout.aa1;
    }*/
    //filter
    public void filter(String charText){
        charText = charText.toLowerCase(Locale.getDefault());
        modellist.clear();
        if (charText.length()==0){
            modellist.addAll(arrayList);
        }
        else {
            for (Model model : arrayList){
                if (model.getTitle().toLowerCase(Locale.getDefault()).contains(charText)){
                    modellist.add(model);
                }



            }
        }
        notifyDataSetChanged();
    }

}