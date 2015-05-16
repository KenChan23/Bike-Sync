package com.example.musicplayer;

import android.util.Log;

import android.os.AsyncTask;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.entity.StringEntity;
import java.util.Iterator;
import org.json.simple.*;
import org.json.simple.parser.*;
import java.io.BufferedReader;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import org.apache.http.util.EntityUtils;
import java.io.InputStreamReader;
import java.util.Arrays;

/**
 * Created by dackerman on 5/5/15.
 */
import java.util.ArrayList;

public class PostToServer extends AsyncTask<ArrayList<Song>,Void,ArrayList<Long> > {

    final String webURL = "http://10.0.2.2:8000/recommendation";
    final DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    final Calendar cal = Calendar.getInstance();
    private MusicService serv;

    HttpResponse response;


    @Override
    protected ArrayList<Long> doInBackground(ArrayList<Song>... in) {
        try {

            ArrayList<Long> alist = new ArrayList<Long>();
            ArrayList<Song> params = in[0];
            JSONArray array = new JSONArray();
            for (int i = 0; i < params.size(); i++) {
                Song song = params.get(i);
                JSONObject jsonobj = new JSONObject();
                jsonobj.put("songID", song.getID());
                jsonobj.put("songTitle", song.getTitle());
                jsonobj.put("songArtist", song.getArtist());
                jsonobj.put("songAlbum", song.getAlbum());
                jsonobj.put("userID", song.getAlbum());
                jsonobj.put("timeStamp", (params.size() == 1 ? dateFormat.format(cal.getTime()) : "LISTINIT"));
                array.add(jsonobj);
            }
            HttpClient httpclient = new DefaultHttpClient();
            HttpPost post = new HttpPost(webURL);
                String json = array.toString();
                StringEntity se = new StringEntity(json);
                post.setEntity(se);
                post.setHeader("Accept", "application/json");
                post.setHeader("content-type", "application/json");
                HttpResponse httpResponse = httpclient.execute(post);
                StringBuilder content = new StringBuilder();
                BufferedReader br = new BufferedReader(new InputStreamReader(httpResponse.getEntity().getContent()));
                String line;
                while (null != (line = br.readLine())) {
                    content.append(line);
                }
                Log.d("CONTENT",content.toString());
                Object obj=JSONValue.parse(content.toString());
                array = (JSONArray) obj;
            if(array != null)
            for(int i = 0; i < array.size(); i++)
            {
                alist.add((long)array.get(i));
            }
           /* if(array != null)
                for(Object o : array)
                {
                    try{Log.d("OBJECT", "" + (long)o);} catch (Exception e){}
                }/*
                JSONObject jsonobj = (JSONObject) obj;
                if (jsonobj != null) {
                    int c = 0;
                    for (Object key: jsonobj.keySet()) {
                        try {
                            long temp = (long) jsonobj.get((String) key);
                            c++;
                        } catch (Exception e) {
                        }
                    }
                    a = new long [c];
                    c--;
                    for (Object key: jsonobj.keySet()) {
                        try {
                            try {Log.d((String)key, (String)jsonobj.get((String)key)); } catch (Exception e) {}
                            a[c] = (long) jsonobj.get((String) key);
                            Log.d("KEY " + c + ": ","" + a[c]);
                            c--;
                        } catch (Exception e) {
                            Log.d("ERROR",e.toString());
                        }
                    }
                } */
            Log.d("LISTINTPOST", alist.toString());
            if (serv != null) {
                Log.d("LISTINTPOSTSUB", alist.toString());
                serv.setQueue(alist);
            }
            return alist;
        }
        catch(Exception e){ Log.e("HTTP PROBLEMS:",e.toString());}
        return null;
    }
}
