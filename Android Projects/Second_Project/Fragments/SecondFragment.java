package prj_2.stu_1722326.Fragments;

import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.google.android.gms.maps.model.LatLng;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import prj_2.stu_1722326.R;

public class SecondFragment extends Fragment {

    JSONArray dS = new JSONArray();
    ListView lv;
    BaseAdapter ba;

    public List<List<HashMap<String, String>>> parse(JSONObject jObject) {

        List<List<HashMap<String, String>>> routes = new ArrayList<>();
        JSONArray jRoutes;
        JSONArray jLegs;
        JSONArray jSteps;
        try {
            jRoutes = jObject.getJSONArray("routes");
            // Traversing all routes
            for (int i = 0; i < jRoutes.length(); i++) {
                jLegs = ((JSONObject) jRoutes.get(i)).getJSONArray("legs");
                List path = new ArrayList<>();
                // Traversing all legs
                for (int j = 0; j < jLegs.length(); j++) {
                    jSteps = ((JSONObject) jLegs.get(j)).getJSONArray("steps");

                    // Traversing all steps
                    for (int k = 0; k < jSteps.length(); k++) {
                        String polyline = "";
                        polyline = (String) ((JSONObject) ((JSONObject) jSteps.get(k)).get("polyline")).get("points");
                        List<LatLng> list = decodePoly(polyline);

                        // Traversing all points
                        for (int l = 0; l < list.size(); l++) {
                            HashMap<String, String> hm = new HashMap<>();
                            hm.put("lat", Double.toString((list.get(l)).latitude));
                            hm.put("lng", Double.toString((list.get(l)).longitude));
                            path.add(hm);
                        }
                    }
                    routes.add(path);
                }
            }

        } catch (JSONException e) {
            e.printStackTrace();
        } catch (Exception e) {
        }
        return routes;
    }

    private List<LatLng> decodePoly(String encoded) {

        List<LatLng> poly = new ArrayList<>();
        int index = 0, len = encoded.length();
        int lat = 0, lng = 0;

        while (index < len) {
            int b, shift = 0, result = 0;
            do {
                b = encoded.charAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            int dlat = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            lat += dlat;

            shift = 0;
            result = 0;
            do {
                b = encoded.charAt(index++) - 63;
                result |= (b & 0x1f) << shift;
                shift += 5;
            } while (b >= 0x20);
            int dlng = ((result & 1) != 0 ? ~(result >> 1) : (result >> 1));
            lng += dlng;

            LatLng p = new LatLng((((double) lat / 1E5)),
                    (((double) lng / 1E5)));
            poly.add(p);
        }

        return poly;
    }

    private static SecondFragment INSTANCE = null;
    View view;

    public SecondFragment() {
    }

    public static SecondFragment getINSTANCE() {
        if (INSTANCE == null)
            INSTANCE = new SecondFragment();
        return INSTANCE;
    }

    // The application will crash if I uncommented these lines, I don't know where the error
    // is, the codes seems correct to me, and also I took it from BCTurk example you gave us.

//    @Override
//    public void onCreate(@Nullable Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//        lv = view.findViewById(R.id.lv);
//        ba = new BaseAdapter()
//        {
//            @Override
//            public int getCount()
//            {
//                return dS.length();
//            }
//
//            @Override
//            public Object getItem(int position)
//            {
//                return null;
//            }
//
//            @Override
//            public long getItemId(int position)
//            {
//                return 0;
//            }
//
//            @Override
//            public View getView(int position, View convertView, ViewGroup parent)
//            {
//                if (convertView == null)
//                {
//                    convertView = getLayoutInflater().inflate(R.layout.item, null);
//                }
//
//                TextView Routes = convertView.findViewById(R.id.routes);
//                TextView Legs = convertView.findViewById(R.id.legs);
//                TextView Steps = convertView.findViewById(R.id.steps);
//
//                try
//                {
//                    JSONObject jo = dS.getJSONObject(position);
//                    Routes.setText( jo.getString("routes"));
//                    Legs.setText( jo.getString("legs"));
//                    Steps.setText(jo.getInt("steps"));
//                } catch (Exception e)
//                {
//                    Log.e("x","JSON PARSE EX : "+e);
//                }
//
//                return convertView;
//            }
//        };
//
//        lv.setAdapter(ba);
//
//        // I should get the data now but I couldn't do it, but I get all data with JSON in the
//        // codes above but I couldn't call the function.
//    }

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.second_fragment, container, false);
        return view;
    }
}
