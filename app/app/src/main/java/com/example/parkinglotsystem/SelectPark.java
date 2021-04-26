package com.example.parkinglotsystem;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
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

    String[] urlAddress = {"http://keycalendar.iptime.org:5000/", "http://keycalendar.iptime.org:5000/"};
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
                    for(int i = 0; i < urlAddress.length; i++) {
                        doc = Jsoup.connect(urlAddress[i]).get();
                        Elements contents = doc.select("#count");
                        count = contents.text();
                        contents = doc.select("#name");
                        name = contents.text();
                        String text = name + "  " + count;

                        bundle.putString("set_text", text);
                        bundle.putInt("index", i);
                        Message msg = handler.obtainMessage();
                        msg.setData(bundle);
                        handler.sendMessage(msg);
                    }

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
            Integer[] button_id = {R.id.btn0, R.id.btn1, R.id.btn2, R.id.btn3, R.id.btn4, R.id.btn5, R.id.btn6};
            int btn_num = bundle.getInt("index");
            Button button = (Button) findViewById(button_id[btn_num]);
            button.setText(bundle.getString("set_text"));
            button.setOnClickListener(new Button.OnClickListener() {
                @Override
                public void onClick(View view) {
                    Intent intent=new Intent(getApplication(), VideoShow.class);
                    intent.putExtra("url", urlAddress[btn_num]);
                    startActivity(intent);
                }
            });

        }
    };

    @Override
    protected  void onRestart(){
        super.onRestart();
        finish();
        Intent intent= new Intent(this, SelectPark.class);
        startActivity(intent);
    }

    public void click_parkinglot(View view) {
        Intent intent=new Intent(this, VideoShow.class);
        startActivity(intent);
    }

    public void click_reset(View view) {
        finish();
        Intent intent= new Intent(this, SelectPark.class);
        startActivity(intent);
    }

}