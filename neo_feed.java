package com.example.neoapp;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MainActivity extends AppCompatActivity {

    private final String API_KEY = "lr86Sx6eyQXbNm32gmmPAuHzzJeXTIfUdzcTjiGB";
    private final String BASE_URL = "https://api.nasa.gov/neo/rest/v1/";
    private TextView textView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        textView = findViewById(R.id.textView);

        getNeoFeed("2025-10-04", "2025-10-06");
    }

    private void getNeoFeed(String startDate, String endDate) {
        ExecutorService executor = Executors.newSingleThreadExecutor();
        Handler handler = new Handler(Looper.getMainLooper());

        executor.execute(() -> {
            try {
                String fullUrl = BASE_URL + "feed?start_date=" + startDate + "&end_date=" + endDate + "&api_key=" + API_KEY;
                URL url = new URL(fullUrl);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");

                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder responseBuilder = new StringBuilder();
                String line;

                while ((line = reader.readLine()) != null) {
                    responseBuilder.append(line);
                }
                reader.close();

                String response = responseBuilder.toString();

                // Parse JSON
                JSONObject json = new JSONObject(response);
                JSONObject meteors = json.getJSONObject("near_earth_objects");

                StringBuilder resultBuilder = new StringBuilder();
                for (String date : meteors.keySet()) {
                    JSONArray neos = meteors.getJSONArray(date);
                    for (int i = 0; i < neos.length(); i++) {
                        JSONObject neo = neos.getJSONObject(i);
                        String name = neo.optString("name", "no name");
                        boolean isDangerous = neo.optBoolean("is_potentially_hazardous_asteroid", false);
                        double size = neo
                                .getJSONObject("estimated_diameter")
                                .getJSONObject("kilometers")
                                .optDouble("estimated_diameter_max", -1);

                        String lineResult = name + " | Hazardous: " + isDangerous + " | Max Size (km): " + size + "\n";
                        resultBuilder.append(lineResult);
                        Log.d("NEO", lineResult); // Debug log
                    }
                }

                // Update UI
                handler.post(() -> textView.setText(resultBuilder.toString()));

            } catch (Exception e) {
                e.printStackTrace();
                handler.post(() -> textView.setText("Error: " + e.getMessage()));
            }
        });
    }
}
