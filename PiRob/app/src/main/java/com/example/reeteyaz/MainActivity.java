package com.example.reeteyaz;

import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ListView;

import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;

import java.util.ArrayList;
import java.util.Arrays;

public class MainActivity extends AppCompatActivity {

    ListView listView;
    ListViewAdapter adapter;
    String[] t;
    String[] description;
    int[] icon;
    ArrayList<Model> arrayList = new ArrayList<Model>();
    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ActionBar actionBar = getSupportActionBar();
        actionBar.setTitle("PiRobot Controller");
//---------
        mainmenu();
//-----------
    }
    public void setlist(String t[],String d[],int ic[]){
        arrayList.clear();
        Arrays.sort(t);
        listView = findViewById(R.id.listView);
        for (int i =0; i<t.length; i++){
            Model model = new Model(t[i], d[i], ic[i]);
            arrayList.add(model);
        }
        adapter = new ListViewAdapter(this, arrayList);
        listView.setAdapter(adapter);
    }
    @Override public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu, menu);
        return true;
    }
    public void mainmenu(){
        t = new String[]{"Bluetooth","Manuel", "Auto"};
        String de[] = new String[20];
        Arrays.fill(de, null);
        int ic[] = new int[20];
        Arrays.fill(ic,R.drawable.scrapbook);
        //Pngs
        //ic[0]=R.drawable.eme;
        //ic[1]=R.drawable.derma;
        //Start
        setlist(t,de,ic);
        ActionBar actionBar = getSupportActionBar();actionBar.setTitle("PiRobot Controller");
    }
    @Override public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id==R.id.home){
            mainmenu();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}