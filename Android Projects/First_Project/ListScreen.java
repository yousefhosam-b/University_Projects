package prj_1.stu_1722326;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.service.voice.AlwaysOnHotwordDetector;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.BaseAdapter;
import android.widget.EditText;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;

import org.json.JSONArray;
import org.jsoup.Jsoup;

import java.util.ArrayList;

public class ListScreen extends AppCompatActivity {
    ListView lv;
    ListScreenAdapter ListScreenAdapter = new ListScreenAdapter();
    JSONArray DataSource = new JSONArray();
    ArrayList<String> List =new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_list_screen);
        lv=findViewById(R.id.lv);
        getData();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        menu.add("Add Post").setIcon(R.drawable.ic_add_post)
                .setShowAsAction(MenuItem.SHOW_AS_ACTION_ALWAYS);

        menu.add("Log Out").setIcon(R.drawable.ic_log_out)
                .setShowAsAction(MenuItem.SHOW_AS_ACTION_ALWAYS);

        menu.add("Account Info").setIcon(R.drawable.ic_account_info)
                .setShowAsAction(MenuItem.SHOW_AS_ACTION_ALWAYS);

        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {

        if(item.getTitle().toString().equals("Add Post"))
        {
            Intent i=new Intent(ListScreen.this,AddPost.class);
            startActivity(i);
        }

        else if (item.getTitle().toString().equals("Log Out")) {
            Log.e("x","message:");
            SharedPreferences.Editor edit = getSharedPreferences
                    ("PRJ_1_1722326", MODE_PRIVATE).edit();
            edit.putString("user","");
            edit.apply();
            Intent i=new Intent(ListScreen.this,MainActivity.class);
            startActivity(i);
        }

        else if (item.getTitle().toString().equals("Account Info"))
        {
            Intent i=new Intent(ListScreen.this,AccountInfo.class);
            startActivity(i);
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressLint("StaticFieldLeak")
    void getData() {
        AlertDialog.Builder notification = new AlertDialog.Builder(this);
        new AsyncTask<String, String, String>() {

            @Override
            protected void onPreExecute() {
            }

            @Override
            protected String doInBackground(String... strings) {
                try {
                    String web = "https://tux.csicxt.com/index.php";
                    String action = Jsoup.connect(web) //to get json data
                            .ignoreContentType(true)
                            .data("op", "list_posts")
                            .data("id","63")
                            .data("shash", "1722326")
                            .post().text();

                    DataSource = new JSONArray(action.toString());

                    for (int i=0; i<DataSource.length(); i++) {
                        List.add(DataSource.get(i).toString());
                    }

                    runOnUiThread(new Runnable() {
                        public void run() {
                            ListScreenAdapter=new ListScreenAdapter(ListScreen.this,List);
                            lv.setAdapter(ListScreenAdapter);
                        }
                    });

                }
                catch (Exception e) {
                    Log.e("x", "Fetch err:" + e);

                    runOnUiThread(new Runnable() {
                        public void run() {
                            notification.setTitle("Wrong");
                            notification.setMessage("There is Error!");
                            notification.setNeutralButton(
                                    "Okay",
                                    new DialogInterface.OnClickListener() {
                                        public void onClick(DialogInterface dialog, int ID) {
                                            dialog.dismiss();
                                        }
                                    });
                            notification.show();
                        }
                    });

                }
                return null;
            }

            @Override
            protected void onPostExecute(String s) {
            }
        }.execute();
    }
}