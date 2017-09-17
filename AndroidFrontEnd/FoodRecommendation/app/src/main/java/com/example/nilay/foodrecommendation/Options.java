package com.example.nilay.foodrecommendation;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

public class Options extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_options);

        // Set options for preferred price spinner
        Spinner pSpinner = (Spinner) findViewById(R.id.priceSpinner);
        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> pAdapter = ArrayAdapter.createFromResource(this,
                R.array.price_array, android.R.layout.simple_spinner_item);
        // Specify the layout to use when the list of choices appears
        pAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // Apply the adapter to the spinner
        pSpinner.setAdapter(pAdapter);

        // Set options for preferred distance spinner
        Spinner dSpinner = (Spinner) findViewById(R.id.distanceSpinner);
        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> dAdapter = ArrayAdapter.createFromResource(this,
                R.array.distance_array, android.R.layout.simple_spinner_item);
        // Specify the layout to use when the list of choices appears
        dAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // Apply the adapter to the spinner
        dSpinner.setAdapter(dAdapter);

        // Set options for preferred time spinner
        Spinner tSpinner = (Spinner) findViewById(R.id.timeSpinner);
        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> tAdapter = ArrayAdapter.createFromResource(this,
                R.array.time_array, android.R.layout.simple_spinner_item);
        // Specify the layout to use when the list of choices appears
        tAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // Apply the adapter to the spinner
        tSpinner.setAdapter(tAdapter);

        // Set options for feels spinner
        Spinner fSpinner = (Spinner) findViewById(R.id.feelsSpinner);
        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> fAdapter = ArrayAdapter.createFromResource(this,
                R.array.feels_array, android.R.layout.simple_spinner_item);
        // Specify the layout to use when the list of choices appears
        fAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // Apply the adapter to the spinner
        fSpinner.setAdapter(fAdapter);

        Button btn = (Button)findViewById(R.id.findButton);

        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int price;
                int distance;
                int time;
                String cuisine;

                // int for price
                Spinner p = (Spinner) findViewById(R.id.priceSpinner);
                price = p.getSelectedItem().toString().length();
                // int for distance
                Spinner d = (Spinner) findViewById(R.id.distanceSpinner);
                String sDistance = d.getSelectedItem().toString();
                if(sDistance.length() == 9)
                    distance = 24;
                else {
                    String ssDistance = sDistance.substring(0,2);
                    if(ssDistance.equals("1 "))
                        distance = 1;
                    else if(ssDistance.equals("5 "))
                        distance = 5;
                    else
                        distance = Integer.parseInt(ssDistance);
                }
                // int for time
                Spinner t = (Spinner) findViewById(R.id.timeSpinner);
                String sTime = t.getSelectedItem().toString();
                if(sTime.equals("1 hr from now"))
                    time = 1;
                else if(sTime.equals("2 hrs from now"))
                    time = 2;
                else if(sTime.equals("3 hrs from now"))
                    time = 3;
                // string for cuisine
                Spinner f = (Spinner) findViewById(R.id.feelsSpinner);
                cuisine = f.getSelectedItem().toString();

                startActivity(new Intent(Options.this, Dashboard.class));
            }
        });
    }


}
