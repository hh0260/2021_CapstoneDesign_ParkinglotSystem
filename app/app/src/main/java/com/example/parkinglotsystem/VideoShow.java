package com.example.parkinglotsystem;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.TextView;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;

public class VideoShow extends AppCompatActivity {

    String urlAddress = "http://keycalendar.iptime.org:5000/";
    String name;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_video_view);

        final Bundle bundle = new Bundle();

        new Thread(){
            @Override
            public void run() {
                Document doc = null;
                try {
                    doc = Jsoup.connect(urlAddress).get();
                    Elements contents = doc.select("#name");
                    name = contents.text();

                    bundle.putString("set_name", name);
                    Message msg = handler.obtainMessage();
                    msg.setData(bundle);
                    handler.sendMessage(msg);

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }.start();

        WebView webView = (WebView)findViewById(R.id.webView);

        webView.setBackgroundColor(0);
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setUseWideViewPort(true);

        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);

        webView.loadData("<html><body><div><img src='http://keycalendar.iptime.org:5000/video_feed'/></div></body></html>" ,"text/html",  "UTF-8");
    }

    Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            Bundle bundle = msg.getData();
            TextView tv1;
            tv1 = (TextView) findViewById(R.id.testview);
            tv1.setText(bundle.getString("set_name"));
        }
    };
}