package com.example.musicplayer;

import android.util.Log;

import android.os.AsyncTask;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.entity.StringEntity;
import org.json.JSONObject;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import org.apache.http.util.EntityUtils;

/**
 * Created by dackerman on 5/5/15.
 */
import java.util.ArrayList;

public class PostToServer extends AsyncTask<ArrayList<Song>,Void,String> {

    final String webURL = "http://10.0.2.2:8000/recommendation";
    final DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    final Calendar cal = Calendar.getInstance();

    HttpResponse response;

    @Override
    protected String doInBackground(ArrayList<Song>... in) {
        try {
            String s = "";
            ArrayList<Song> params = in[0];
            for (int i = 0; i < params.size(); i++) {
                Song song = params.get(i);
                HttpClient httpclient = new DefaultHttpClient();
                HttpPost post = new HttpPost(webURL);
                JSONObject jsonobj = new JSONObject();
                jsonobj.accumulate("songID", song.getID());
                jsonobj.accumulate("songTitle", song.getTitle());
                jsonobj.accumulate("songArtist", song.getArtist());
                jsonobj.accumulate("songAlbum", song.getAlbum());
                jsonobj.accumulate("userID", song.getAlbum());
                jsonobj.accumulate("timeStamp", (params.size() == 1 ? dateFormat.format(cal.getTime()) : "LISTINIT"));

                String json = jsonobj.toString();
                StringEntity se = new StringEntity(json);
                post.setEntity(se);
                post.setHeader("Accept", "application/json");
                post.setHeader("content-type", "application/json");
                HttpResponse httpResponse = httpclient.execute(post);
                Log.d("HTTPRESPONSE", EntityUtils.toString(httpResponse.getEntity(), "utf-8"));
            }
            return s;
        }
        catch(Exception e){ Log.e("HTTP PROBLEMS:",e.toString());}
        return null;
    }
}
