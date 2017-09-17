package com.example.nilay.foodrecommendation;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.Spinner;

public class Profile extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        // Set options for preferred price range spinner
        Spinner pRangeSpinner = (Spinner) findViewById(R.id.priceRangeSpinner);
        // Create an ArrayAdapter using the string array and a default spinner layout
        ArrayAdapter<CharSequence> pRangeAdapter = ArrayAdapter.createFromResource(this,
                R.array.priceRange_array, android.R.layout.simple_spinner_item);
        // Specify the layout to use when the list of choices appears
        pRangeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        // Apply the adapter to the spinner
        pRangeSpinner.setAdapter(pRangeAdapter);

        // Set options for maximum range spinner
        Spinner maxRangeSpinner = (Spinner) findViewById(R.id.rangeSpinner);
        ArrayAdapter<CharSequence> maxRangeAdapter = ArrayAdapter.createFromResource(this, R.array.range_array,
                android.R.layout.simple_spinner_item);
        maxRangeAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        maxRangeSpinner.setAdapter(maxRangeAdapter);

        // Set options for favorite meal spinner
        Spinner favMealSpinner = (Spinner) findViewById(R.id.favoriteMealSpinner);
        ArrayAdapter<CharSequence> favMealAdapter = ArrayAdapter.createFromResource(this, R.array.mealType_array,
                android.R.layout.simple_spinner_item);
        favMealAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        favMealSpinner.setAdapter(favMealAdapter);

        Button btn = (Button)findViewById(R.id.finishButton);

        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Profile.this, Dashboard.class));
            }
        });
    }
}
