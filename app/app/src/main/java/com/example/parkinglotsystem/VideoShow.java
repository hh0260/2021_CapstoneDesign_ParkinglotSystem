package com.example.parkinglotsystem;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
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

    String name;
    String urlAddress;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_video_view);

        Intent secondIntent = getIntent();
        urlAddress = secondIntent.getStringExtra("url");
        name = secondIntent.getStringExtra("name");
        if(name == null)
            name = "서버연결 안됨";
        TextView tv1;
        tv1 = (TextView) findViewById(R.id.testview);
        tv1.setText(name);

        WebView webView = (WebView)findViewById(R.id.webView);

        webView.setBackgroundColor(0);
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setUseWideViewPort(true);

        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);

        webView.loadData("<html><body><div><img src='" + urlAddress + "video_feed'/></div></body></html>" ,"text/html",  "UTF-8");
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