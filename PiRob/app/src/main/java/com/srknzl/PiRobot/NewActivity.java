package com.srknzl.PiRobot;

import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;


import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import java.util.ArrayList;
import java.util.Arrays;
public class NewActivity extends AppCompatActivity {
    ListView listView;
    ArrayList<Model> arrayList = new ArrayList<>();
    ListViewAdapter adapter;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Intent intent = getIntent();
        String mContent = intent.getStringExtra("activityName");
        //Acil
        String des[] = new String[100];
        Arrays.fill(des, null);
        int i[] = new int[100];
        Arrays.fill(i,R.drawable.car);
        //-----MainMenu
        if (mContent.equals("ManuelWithButtons")){

            extra(mContent);
            setContentView(R.layout.manuel_with_buttons);

            Button b1 = this.findViewById(R.id.top);
            b1.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Toast.makeText(NewActivity.this, "adfadf", Toast.LENGTH_SHORT).show();
                }
            });
        }
        if (mContent.equals("Auto")){
            extra(mContent);
            setContentView(R.layout.autonomous);
        }

        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

    }
    String mcon="none";
    boolean booleansearch =true;
    public void extra(String m){
        mcon=m;
        booleansearch =false;
    }
    public void setlist(String t[],String d[],int ic[]){
        arrayList.clear();
        Arrays.sort(t);
        listView = findViewById(R.id.listView);
        for (int i =0; i<t.length; i++){
            Model model = new Model(t[i], d[i], ic[i]);
            //bind all strings in an array
            arrayList.add(model);
        }
        adapter = new ListViewAdapter(this, arrayList);
        listView.setAdapter(adapter);
    }
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == android.R.id.home){
            this.finish();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
    public boolean onCreateOptionsMenu(Menu menu) {

        getMenuInflater().inflate(R.menu.menu, menu);
        return true;
    }
}