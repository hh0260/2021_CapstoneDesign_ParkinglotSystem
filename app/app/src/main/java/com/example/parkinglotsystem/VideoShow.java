package com.example.parkinglotsystem;

import androidx.appcompat.app.AppCompatActivity;

import android.os.AsyncTask;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.TextView;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;

public class VideoShow extends AppCompatActivity {

    String urlAddress = "uml";
    String name;
    Name nametext = new Name();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_video_view);

        nametext.execute();

        WebView webView = (WebView)findViewById(R.id.webView);
        webView.setWebViewClient(new WebViewClient());
        webView.setBackgroundColor(255);
        webView.getSettings().setLoadWithOverviewMode(true);
        webView.getSettings().setUseWideViewPort(true);

        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);

        webView.loadData("<html><body><div><img src='uml/video_feed'/></div></body></html>" ,"text/html",  "UTF-8");
    }

    @Override
    protected void onDestroy(){
        super.onDestroy();
    }

    private class Name extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... params) {
            try {
                Document doc = Jsoup.connect(urlAddress).get();
                Elements contents = doc.select("#name");
                name = contents.text();
                TextView tv1;
                tv1 = (TextView) findViewById(R.id.testview);
                tv1.setText(name);

            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
    }

}