package prj_1.stu_1722326;


import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;


import org.json.JSONObject;
import org.jsoup.Jsoup;

public class MainActivity extends AppCompatActivity {
    EditText etUn, etPw;
    JSONObject DataSource = new JSONObject(), User = new JSONObject();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        SharedPreferences sp = getSharedPreferences("PRJ_1_1722326", MODE_PRIVATE);
        String user = sp.getString("user", "");
        if (!user.isEmpty() && user!=null){
            Intent i = new Intent(MainActivity.this,ListScreen.class);
            startActivity(i);
            finish();
        }

        etUn = findViewById(R.id.etUn);
        etPw = findViewById(R.id.etPw);
    }

    public void doLogin(View view) {
        getData();
    }

    @SuppressLint("StaticFieldLeak")
    void getData() {
        AlertDialog.Builder notification =new AlertDialog.Builder(this);

        // Get Text Values From Edit Text Instances
        String UserName = etUn.getText().toString();
        String Password = etPw.getText().toString();

        new AsyncTask<String, String, String>() {
            @Override
            protected void onPreExecute() {
            }

            @Override
            protected String doInBackground(String... p) {
                try {
                    String web= "https://tux.csicxt.com/index.php";
                    String action = Jsoup.connect(web)
                            .ignoreContentType(true)
                            .data("op", "login")
                            .data("un", UserName)
                            .data("pw", Password)
                            .data("shash", "1722326")
                            .post().text();

                    DataSource = new JSONObject(action);
                    User = DataSource.getJSONObject("user");
                    runOnUiThread(new Runnable() {
                        public void run() {
                            Toast.makeText(MainActivity.this,"Working"
                                    ,Toast.LENGTH_LONG).show();
                        }
                    });
                    SharedPreferences.Editor edit = getSharedPreferences("PRJ_1_1722326",
                            MODE_PRIVATE).edit();
                    edit.putString("user",User.toString());
                    edit.apply();
                    Intent i=new Intent(MainActivity.this,ListScreen.class);
                    startActivity(i);
                    finish();
                }
                catch (Exception e) {
                    Log.e("x","Fetch err:" + e);
                    runOnUiThread(new Runnable() {
                        public void run() {
                            notification.setTitle("Wrong");
                            notification.setMessage("There is Error");
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

    public void doGoToRegister(View view) {
        Intent i = new Intent(MainActivity.this, Registration.class);
        startActivity(i);
    }

}