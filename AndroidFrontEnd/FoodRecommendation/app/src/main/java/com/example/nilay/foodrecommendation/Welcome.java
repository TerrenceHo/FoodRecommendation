package com.example.nilay.foodrecommendation;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.example.nilay.foodrecommendation.R;

import org.json.JSONException;
import org.json.JSONObject;

public class Welcome extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome);

        EditText m_firstName =(EditText)findViewById(R.id.editFirstName);
        EditText m_lastName =(EditText)findViewById(R.id.editLastName);
        String firstName = m_firstName.getText().toString();
        String lastName = m_lastName.getText().toString();

       /* JSONObject user_Name = new JSONObject();
        try {
            user_Name.put("firstname", firstName);
            user_Name.put("lastname", lastName);
        } catch (JSONException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }*/

        // Generate unique UserID


        // Instantiate the RequestQueue.
     //   RequestQueue queue = Volley.newRequestQueue(this);
     //   String base_url ="https://food-rec-staging.herokuapp.com";
     //   String user_url = base_url + "/api/v1/user";

        // Request a string response from the provided URL.
    //    StringRequest stringRequest = new StringRequest(Request.Method.POST, user_url,
    //            new Response.Listener<String>() {
     //               @Override
    //                public void onResponse(String response) {

    //                }
    //            });
        // Add the request to the RequestQueue.
   //     queue.add(stringRequest);

        Button btn = (Button)findViewById(R.id.continueButton);

        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(Welcome.this, Profile.class));
            }
        });
    }
}
