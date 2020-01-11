package com.srknzl.PiRobot;

import android.content.Context;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.ListView;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import java.util.ArrayList;
import java.util.Vector;

public class MainActivity extends AppCompatActivity {

    ListView listView;
    ListViewAdapter adapter;
    ArrayList<Model> arrayList = new ArrayList<>();
    final Context context = this;
    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Toolbar toolbar = findViewById(R.id.toolbar);
        Button bluetoothButton = toolbar.findViewById(R.id.bluetooth_button);
        final CheckBox c = toolbar.findViewById(R.id.connection_status);

        bluetoothButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Bluetooth.connectIfPaired(context);
            }
        });
        setSupportActionBar(toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(false);

//---------
        mainmenu();
//-----------
    }
    public void setlist(Vector<String> titles, Vector<String> descs, Vector<Integer> icons) {// Title desc icon
        arrayList.clear();
        listView = findViewById(R.id.listView);
        for (int i =0; i<titles.size(); i++){
            Model model = new Model(titles.elementAt(i), descs.elementAt(i), icons.elementAt(i));
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
        Vector<String> titles = new Vector<>();
        Vector<String> descs = new Vector<>();
        Vector<Integer> icons = new Vector<>();

        titles.add("Manuel with Buttons");
        descs.add("Control the car with buttons");
        icons.add(R.drawable.car);

        titles.add("Auto");
        descs.add("Control the car in autonomous mode");
        icons.add(R.drawable.car);

        setlist(titles,descs,icons);
    }
    @Override public boolean onOptionsItemSelected(MenuItem item) {
        return super.onOptionsItemSelected(item);
    }
}