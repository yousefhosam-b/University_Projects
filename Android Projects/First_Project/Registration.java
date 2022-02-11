package prj_1.stu_1722326;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import org.json.JSONObject;
import org.jsoup.Jsoup;

public class Registration extends AppCompatActivity {
    EditText etNewUn, etNewPw, etPn, etC, etDn;
    JSONObject DataSource = new JSONObject();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_registration);
        Log.e("TAG4435", "onCreate");
        etNewUn = findViewById(R.id.etNewUn);
        etNewPw = findViewById(R.id.etNewPw);
        etPn = findViewById(R.id.etPn);
        etC = findViewById(R.id.etC);
        etDn = findViewById(R.id.etDn);

    }

    public void doRegister(View view) {
        getData();

    }

    @SuppressLint("StaticFieldLeak")
    void getData() {
        AlertDialog.Builder notification =new AlertDialog.Builder(this);

        // Get Text Values From Edit Text Instances
        String NewUserName = etNewUn.getText().toString();
        String NewPassWord = etNewPw.getText().toString();
        String PhoneNumber = etPn.getText().toString();
        String Country = etC.getText().toString();
        String DisplayName = etDn.getText().toString();

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
                            .data("op", "register")
                            .data("shash", "1722326")
                            .data("un", NewUserName)
                            .data("pw", NewPassWord)
                            .data("phone", PhoneNumber)
                            .data("country", Country)
                            .data("dn", DisplayName)
                            .post().text();

                    DataSource = new JSONObject(action);
                    runOnUiThread(new Runnable() {
                        public void run() {
                            notification.setTitle("Info");
                            notification.setMessage("Registration is Complete");
                            notification.setNeutralButton(
                                    "Okay",
                                    new DialogInterface.OnClickListener() {
                                        public void onClick(DialogInterface dialog, int ID) {
                                            Intent intent=new Intent(Registration
                                                    .this,MainActivity.class);
                                            startActivity(intent);
                                            dialog.dismiss();
                                        }
                                    });
                            notification.show();
                        }
                    });

                }
                catch (Exception e) {
                    Log.e("x","Fetch err:"+e);
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
}