package prj_2.stu_1722326.Fragments;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;

import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.MapsInitializer;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.Polyline;
import com.google.android.gms.maps.model.PolylineOptions;

import prj_2.stu_1722326.FetchURL;
import prj_2.stu_1722326.R;
import prj_2.stu_1722326.TaskLoadedCallback;

public class FirstFragment extends Fragment implements OnMapReadyCallback, TaskLoadedCallback {


    private static FirstFragment INSTANCE = null;
    MarkerOptions p1, p2;
    View view;
    GoogleMap map;
    MapView mapView;
    Button getDirection;
    Polyline currentPolyline;


    public FirstFragment() {
    }

    public static FirstFragment getINSTANCE() {
        if (INSTANCE == null)
            INSTANCE = new FirstFragment();
        return INSTANCE;
    }

    @Override
    public void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Allow menu options to appear
        setHasOptionsMenu(true);
    }

    @Override
    public void onCreateOptionsMenu(@NonNull Menu menu, @NonNull MenuInflater inflater) {
        // xml menu was created because I want to show the options in the fragment
        // but I don't want to show them in the main activity
        inflater.inflate(R.menu.menu_main, menu);
        super.onCreateOptionsMenu(menu, inflater);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item)
    {
        String in = item.getTitle().toString();
        if (in.equals("Normal"))
        {
            map.setMapType(GoogleMap.MAP_TYPE_NORMAL);
        }
        if (in.equals("Satellite"))
        {
            map.setMapType(GoogleMap.MAP_TYPE_SATELLITE);
        }
        if (in.equals("Hybrid"))
        {
            map.setMapType(GoogleMap.MAP_TYPE_HYBRID);
        }
        if (in.equals("Terrain"))
        {
            map.setMapType(GoogleMap.MAP_TYPE_TERRAIN);
        }
        return super.onOptionsItemSelected(item);
    }


    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        // Initialize view
       View view = inflater.inflate(R.layout.first_fragment, container, false);

       // I don't know why getDirection button here is not working, I tried in other different
       // ways to implement the button but they all didn't work
        getDirection = view.findViewById(R.id.btnGetDirection);
        getDirection.setOnClickListener(view1 -> new FetchURL(FirstFragment.this)
                .execute(getUrl(p1.getPosition(), p2.getPosition(), "driving"),
                        "driving"));
        return view;

    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        mapView = view.findViewById(R.id.mapView);

        if (mapView != null) {
            mapView.onCreate(null);
            mapView.onResume();
            //Async map
            mapView.getMapAsync(this);
        }
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        MapsInitializer.initialize(getContext());
        map = googleMap;
        Log.d("mylog", "Added Markers");

        // Add a markers in both places and move the camera
        LatLng p1 = new LatLng(41.0505547,29.0057057);
        LatLng p2 = new LatLng(41.0423983,29.0087527);

        // Set position and title of markers
        map.addMarker(new MarkerOptions().position(p1).title("Location 1"));
        map.addMarker(new MarkerOptions().position(p2).title("Location 2"));

        // Move the camera to first location
        map.moveCamera(CameraUpdateFactory.newLatLng(p1));

        // Animating to zoom the map
        map.animateCamera(CameraUpdateFactory.newLatLngZoom(p1, 15));
    }

    private String getUrl(LatLng origin, LatLng dest, String directionMode) {
        // Origin of route
        String str_origin = "origin=" + origin.latitude + "," + origin.longitude;
        // Destination of route
        String str_dest = "destination=" + dest.latitude + "," + dest.longitude;
        // Mode
        String mode = "mode=" + directionMode;
        // Building the parameters to the web service
        String parameters = str_origin + "&" + str_dest + "&" + mode;
        // Output format
        String output = "json";
        // Building the url to the web service
        String url = "https://maps.googleapis.com/maps/api/directions/"
                + output + "?" + parameters + "&key=" + getString(R.string.google_maps_key);
        return url;
    }

    @Override
    public void onTaskDone(Object... values) {
        if (currentPolyline != null)
            currentPolyline.remove();
        currentPolyline = map.addPolyline((PolylineOptions) values[0]);
    }
}
