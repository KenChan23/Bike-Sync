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

/**
 * Created by dackerman on 5/5/15.
 */

public class PostToServer extends AsyncTask<Song,Void,HttpResponse> {

    final String webURL = "http://10.0.2.2:8000/recommendation";
    final DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    final Calendar cal = Calendar.getInstance();

    HttpResponse response;

    @Override
    protected HttpResponse doInBackground(Song... params) {
        try {
            Song song = params[0];
            HttpClient httpclient= new DefaultHttpClient();
            HttpPost post = new HttpPost(webURL);
            JSONObject jsonobj = new JSONObject();
            jsonobj.accumulate("songID", song.getID());
            jsonobj.accumulate("songTitle", song.getTitle());
            jsonobj.accumulate("songArtist", song.getArtist());
            jsonobj.accumulate("songAlbum", song.getAlbum());
            jsonobj.accumulate("userID", song.getAlbum());
            jsonobj.accumulate("timeStamp", dateFormat.format(cal.getTime()));

            String json = jsonobj.toString();
            StringEntity se = new StringEntity(json);
            post.setEntity(se);
            post.setHeader("Accept","application/json");
            post.setHeader("content-type", "application/json");
            HttpResponse httpResponse = httpclient.execute(post);
            Log.d("HTTPRESPONSE", httpResponse.toString());
            return httpResponse;
        }
        catch(Exception e){ Log.e("HTTP PROBLEMS:",e.toString());}
        return null;
    }
}
