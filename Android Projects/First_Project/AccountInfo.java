package prj_1.stu_1722326;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;
import org.jsoup.Jsoup;

public class AccountInfo extends AppCompatActivity {
    TextView Username,Phone,Country,DisplayName;
    EditText OldPw,NewPw;
    JSONObject DataSource = new JSONObject();
    String User = "";
    String ID = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_account_info);
        Username = findViewById(R.id.Username);
        Phone = findViewById(R.id.Phone);
        Country = findViewById(R.id.Country);
        DisplayName = findViewById(R.id.DisplayName);
        OldPw = findViewById(R.id.OldPw);
        NewPw = findViewById(R.id.NewPw);

        SharedPreferences sp = getSharedPreferences("PRJ_1_1722326", MODE_PRIVATE);
        User = sp.getString("user", "");
        if (!User.isEmpty() && User!=null){
            try {
                JSONObject JSON =new JSONObject(User);
                Username.setText(JSON.getString("un"));
                Phone.setText(JSON.getString("phone"));
                Country.setText(JSON.getString("country"));
                DisplayName.setText(JSON.getString("display_name"));
                ID = JSON.getString("id");
            }
            catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    public void doChangePw(View view) {
        if(!OldPw.getText().toString().equals("") && !NewPw.getText().toString().equals("")){
            getData();
        }
        else
        {
            Log.e("x","Please Fill Both Of Them");
        }
    }

    @SuppressLint("StaticFieldLeak")
    void getData() {
        AlertDialog.Builder notification =new AlertDialog.Builder(this);

        // Get Text Values From Edit Text Instances
        String OldPassword = OldPw.getText().toString();
        String NewPassword = NewPw.getText().toString();

        new AsyncTask<String, String, String>() {
            @Override
            protected void onPreExecute() {
            }

            @Override
            protected String doInBackground(String... strings) {
                try {
                    String web = "https://tux.csicxt.com/index.php";
                    String action = Jsoup.connect(web)
                            .ignoreContentType(true)
                            .data("op", "change_password")
                            .data("id", ID)
                            .data("opw",OldPassword)
                            .data("npw",NewPassword)
                            .data("shash", "1722326")
                            .post().text();
                    DataSource = new JSONObject(action);
                    runOnUiThread(new Runnable() {
                        public void run() {
                            notification.setTitle("Update!");
                            notification.setMessage("Password Has Changed");
                            notification.setNeutralButton(
                                    "Okay",
                                    new DialogInterface.OnClickListener() {
                                        public void onClick(DialogInterface dialog, int id) {
                                            dialog.dismiss();
                                        }
                                    });
                            notification.show();
                        }
                    });
                }
                catch (Exception e) {
                    Log.e("x", "Fetch err:" + e);
                }

                return null;
            }

            @Override
            protected void onPostExecute(String s) {
            }
        }.execute();
    }
}