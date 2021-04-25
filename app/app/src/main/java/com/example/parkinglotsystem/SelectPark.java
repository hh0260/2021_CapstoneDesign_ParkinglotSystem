package com.example.parkinglotsystem;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.view.View;
import android.widget.Button;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;

public class SelectPark extends AppCompatActivity {

    String urlAddress = "http://keycalendar.iptime.org:5000/";
    String count, name;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_select__park);
        final Bundle bundle = new Bundle();

        new Thread(){
            @Override
            public void run() {
                Document doc = null;
                try {
                    doc = Jsoup.connect(urlAddress).get();
                    Elements contents = doc.select("#count");
                    count = contents.text();
                    contents = doc.select("#name");
                    name = contents.text();
                    String text = name + "  " + count;

                    bundle.putString("set_text", text);
                    Message msg = handler.obtainMessage();
                    msg.setData(bundle);
                    handler.sendMessage(msg);

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }.start();

    }

    Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            Bundle bundle = msg.getData();
            Button button1;
            button1 = (Button) findViewById(R.id.btn1);
            button1.setText(bundle.getString("set_text"));
        }
    };

    @Override
    protected  void onRestart(){
        super.onRestart();
        finish();
        Intent intent= new Intent(getApplication(), SelectPark.class);
        startActivity(intent);
    }

    public void click_parkinglot(View view) {
        Intent intent=new Intent(this, VideoShow.class);
        startActivity(intent);
    }

    public void click_reset(View view) {
        finish();
        Intent intent= new Intent(getApplication(), SelectPark.class);
        startActivity(intent);
    }

}