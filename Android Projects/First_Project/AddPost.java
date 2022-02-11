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
import android.widget.Button;
import android.widget.EditText;

import org.json.JSONObject;
import org.jsoup.Jsoup;

public class AddPost extends AppCompatActivity {
    EditText etAddTitle,etAddText;
    String message = "";
    JSONObject DataSource = new JSONObject();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_post);
        etAddTitle = findViewById(R.id.etAddTitle);
        etAddText = findViewById(R.id.etAddText);
    }

    public void doAddPost(View view) {
        if(!etAddText.getText().toString().isEmpty() && !etAddTitle.getText().toString().isEmpty())
            getData();
    }

    @SuppressLint("StaticFieldLeak")
    void getData() {
        AlertDialog.Builder notification = new AlertDialog.Builder(this);

        // Get Text Values From Edit Text Instances
        String Title = etAddTitle.getText().toString();
        String Text = etAddText.getText().toString();

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
                            .data("op", "add_post")
                            .data("shash", "1722326")
                            .data("title", Title)
                            .data("txt", Text)
                            .data("id","63")
                            .post().text();

                    DataSource = new JSONObject(action);
                    message = DataSource.getString("msg");

                    if(message.equals("Post Added")) {
                        Intent i = new Intent(AddPost.this, ListScreen.class);
                        startActivity(i);
                        finish();
                    }
                    else {
                        runOnUiThread(new Runnable() {
                            public void run() {
                                notification.setTitle("Wrong");
                                notification.setMessage(message);
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
                }
                catch (Exception e) {
                    Log.e("x", "Fetch err:" + e);
                    runOnUiThread(new Runnable() {
                        public void run() {
                            notification.setTitle("Error");
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