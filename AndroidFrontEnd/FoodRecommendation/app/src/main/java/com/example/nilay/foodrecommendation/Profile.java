package com.example.nilay.foodrecommendation;

import android.app.Activity;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.Toast;

public class Profile extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        // Set options for preferred price range spinner
        final Spinner pRangeSpinner = (Spinner) findViewById(R.id.priceRangeSpinner);
        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> pRangeAdapter = ArrayAdapter.createFromResource(this,
                R.array.priceRange_array, android.R.layout.simple_spinner_item);
        // Specify the layout to use when the list of choices appears
        pRangeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // Apply the adapter to the spinner
        pRangeSpinner.setAdapter(pRangeAdapter);

        // Set options for maximum distance spinner
        Spinner maxDistanceSpinner = (Spinner) findViewById(R.id.rangeSpinner);
        ArrayAdapter<CharSequence> maxDistanceAdapter = ArrayAdapter.createFromResource(this, R.array.range_array,
                android.R.layout.simple_spinner_item);
        maxDistanceAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        maxDistanceSpinner.setAdapter(maxDistanceAdapter);

        // Set options for cuisine spinner
        Spinner cuisineSpinner = (Spinner) findViewById(R.id.cuisineSpinner);
        ArrayAdapter<CharSequence> cuisineAdapter = ArrayAdapter.createFromResource(this, R.array.cuisine_array,
                android.R.layout.simple_spinner_item);
        cuisineAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        cuisineSpinner.setAdapter(cuisineAdapter);

        Button btn = (Button)findViewById(R.id.finishButton);

        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int price;
                int distance;
                String cuisine;

                // int for price
                Spinner p = (Spinner) findViewById(R.id.priceRangeSpinner);
                price = p.getSelectedItem().toString().length();
                // int for distance
                Spinner d = (Spinner) findViewById(R.id.rangeSpinner);
                String sDistance = d.getSelectedItem().toString();
                if(sDistance.length() == 3)
                    distance = 24;
                else {
                    String ssDistance = sDistance.substring(0, 2);
                    if (ssDistance.equals("1 "))
                        distance = 1;
                    else if (ssDistance.equals("5 "))
                        distance = 5;
                    else
                        distance = Integer.parseInt(ssDistance);
                }
                // string for cuisine
                Spinner f = (Spinner) findViewById(R.id.cuisineSpinner);
                cuisine = f.getSelectedItem().toString();
                startActivity(new Intent(Profile.this, Dashboard.class));
            }
        });
    }
}



