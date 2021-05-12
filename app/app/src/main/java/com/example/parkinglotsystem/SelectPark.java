package com.example.parkinglotsystem;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;

public class SelectPark extends AppCompatActivity {

    String[] urlAddress = {"http://keycalendar.iptime.org:5000/", "http://keycalendar.iptime.org:5000/", "http://keycalendar.iptime.org:5000/", "http://keycalendar.iptime.org:5000/", "http://keycalendar.iptime.org:5000/", "http://keycalendar.iptime.org:5000/", "http://keycalendar.iptime.org:5000/"};
//    String[] urlAddress = {"http://keycalendar.iptime.org:5000/"};
    String name;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_select__park);

        JsoupAsyncTask jsoupAsyncTask = new JsoupAsyncTask();
        jsoupAsyncTask.execute();
    }

    private class JsoupAsyncTask extends AsyncTask<Void, Void, String[]> {

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected String[] doInBackground(Void... params) {
            String count;
            Document[] doc = new Document[urlAddress.length];
            String[] ptext = new String[urlAddress.length];
            for(int i = 0; i < urlAddress.length; i++) {
                try {
                    doc[i] = Jsoup.connect(urlAddress[i]).get();
                } catch (IOException e) {
                    e.printStackTrace();
                    i--;
                }
            }
            for(int i = 0; i < urlAddress.length; i++) {
                Elements pcount = doc[i].select("#count");
                count = pcount.text();
                Elements pname = doc[i].select("#name");
                name = pname.text();
                ptext[i] = name + "  " + count;
            }
            return ptext;
        }

        @Override
        protected void onPostExecute(String[] result) {
            Button[] buttons = new Button[urlAddress.length];
            Integer[] button_id = {R.id.btn0, R.id.btn1, R.id.btn2, R.id.btn3, R.id.btn4, R.id.btn5, R.id.btn6};
            for(int i = 0; i < urlAddress.length; i++) {
                buttons[i] = (Button) findViewById(button_id[i]);
                buttons[i].setText(result[i]);
                int num = i;
                buttons[i].setOnClickListener(new Button.OnClickListener() {
                    @Override
                    public void onClick(View view) {
                        Intent intent = new Intent(getApplication(), VideoShow.class);
                        intent.putExtra("url", urlAddress[num]);
                        intent.putExtra("name", name);
                        startActivity(intent);
                    }
                });
            }
        }
    }

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