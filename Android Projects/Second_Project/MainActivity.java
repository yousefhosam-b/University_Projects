package prj_2.stu_1722326;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;

import android.view.View;
import android.widget.EditText;


public class MainActivity extends AppCompatActivity {
    EditText etStartingAddress, etDestinationAddress;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        etStartingAddress = findViewById(R.id.etStartingAddress);
        etDestinationAddress = findViewById(R.id.etDestinationAddress);

    }

    public void doNavigation(View view) {
        Intent i = new Intent(MainActivity.this, NavigationActivity.class);
        // Get Values From EditTexts And Attach Them To Intent Object
        // With Some Key Values
        i.putExtra("p1", etStartingAddress.getText().toString());
        i.putExtra("p2", etDestinationAddress.getText().toString());
        startActivity(i);
    }

}