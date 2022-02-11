package prj_2.stu_1722326;

import androidx.appcompat.app.AppCompatActivity;
import androidx.viewpager.widget.ViewPager;

import android.os.Bundle;

import com.google.android.material.tabs.TabLayout;

import prj_2.stu_1722326.Fragments.FragmentAdapter;

public class NavigationActivity extends AppCompatActivity {

    String p1 = "";
    String p2 = "";
    ViewPager viewPager;
    TabLayout tabLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_navigation);

        viewPager = findViewById(R.id.viewPager);
        tabLayout = findViewById(R.id.tabLayout);

        FragmentAdapter fragmentAdapter = new FragmentAdapter(getSupportFragmentManager(),this);
        viewPager.setAdapter(fragmentAdapter);
        tabLayout.setupWithViewPager(viewPager);

        // To Get Values Which Are Sent By The Previous Activity
        // We Should Access The Intent Which Starts This Class
        // And By Using Key Values, We Should Get Parameters That Are Sent By
        // The Previous Activity
        p1 = (getIntent().getExtras().getString("p1"));
        p2 = (getIntent().getExtras().getString("p2"));

    }
}