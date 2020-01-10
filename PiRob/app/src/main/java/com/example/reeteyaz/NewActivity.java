package com.example.reeteyaz;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.ActionBar;
import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;
import java.util.Arrays;
public class NewActivity extends AppCompatActivity {
    ListView listView;
    ArrayList<Model> arrayList = new ArrayList<Model>();
    String[] t;
    String[] des;
    int[] i;
    ListViewAdapter adapter;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_new);

        ActionBar actionBar = getSupportActionBar();
        TextView mDetailTv = findViewById(R.id.textView);

        Intent intent = getIntent();
        String mContent = intent.getStringExtra("contentTv");
        //Acil
        String des[] = new String[100];
        Arrays.fill(des, null);
        int i[] = new int[100];
        Arrays.fill(i,R.drawable.scrapbook);
        //-----MainMenu
        if (mContent.startsWith("m")){ extra(mContent);setContentView(R.layout.genel02);
                Button b1 = (Button) this.findViewById(R.id.top);
                b1.setOnClickListener(new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        Toast.makeText(NewActivity.this, "adfadf", Toast.LENGTH_SHORT).show();
                    }
                });
        }
        if (mContent.startsWith("b")){ extra(mContent);
        }
        if (mContent.startsWith("a")){ extra(mContent);setContentView(R.layout.genel03);


        }
        // -----------help
        //if (mContent.startsWith("help3")){ extra(mContent);setContentView(R.layout.help3);
        // Button b1 = (Button) this.findViewById(R.id.send);}
        //b1.setOnClickListener(new View.OnClickListener() {public void onClick(View view) { sendmes(); }});
        //------------
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
        if (id==R.id.home){
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