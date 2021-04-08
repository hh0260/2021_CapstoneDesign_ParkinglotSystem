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

    String urlAddress = "uml";
    String count, name;
    CarCount carCount = new CarCount();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_select__park);
        carCount.execute();
    }

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

    private class CarCount extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
            try {
                Document doc = Jsoup.connect(urlAddress).get();
                Elements contents = doc.select("#count");
                count = contents.text();
                contents = doc.select("#name");
                name = contents.text();
                Button button1;
                button1 = (Button) findViewById(R.id.btn1);
                button1.setText(name + "   " + count);

            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }

}