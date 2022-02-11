package prj_1.stu_1722326;


import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;
import org.jsoup.Jsoup;

import java.util.ArrayList;

public class ListScreenAdapter extends BaseAdapter {
    AlertDialog.Builder notification;
    JSONObject DataSource = new JSONObject();
    ArrayList<String> List = new ArrayList<>();
    Context context;

    public ListScreenAdapter(Context c,ArrayList<String> l){
        context = c;
        List = l;
        notification = new AlertDialog.Builder(context);
    }

    public ListScreenAdapter(){
    }

    @Override
    public int getCount() {
        return List.size();
    }

    @Override
    public Object getItem(int position) {
        return List.get(position);
    }

    @Override
    public long getItemId(int position) {
        return position;
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        if (convertView == null) {
            convertView = LayoutInflater.from(context).inflate(R.layout.list_screen_item,
                    parent, false);
        }
        TextView tvTitle,tvText;
        tvTitle = convertView.findViewById(R.id.title);
        tvText = convertView.findViewById(R.id.text);

        try {
            JSONObject JSON=new JSONObject(List.get(position));
            tvTitle.setText(JSON.getString("title"));
            tvText.setText(JSON.getString("txt"));
            convertView.setOnLongClickListener(new View.OnLongClickListener() {

                @Override
                public boolean onLongClick(View v) {
                    notification.setTitle("Delete Post");
                    notification.setMessage("Delete This Post?");
                    notification.setPositiveButton(
                            "Yes",
                            new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int ID) {
                                    try {
                                        getData(JSON.getString("id"));
                                        List.remove(position);
                                        notifyDataSetChanged();
                                    }
                                    catch (JSONException e) {
                                        e.printStackTrace();
                                    }
                                    dialog.dismiss();
                                }
                            });

                    notification.setNegativeButton(
                            "No",
                            new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int id) {
                                    dialog.dismiss();
                                }
                            });
                    notification.show();
                    return true;
                }
            });

        }
        catch (JSONException e) {
            e.printStackTrace();
        }
        return convertView;
    }

    @SuppressLint("StaticFieldLeak")
    void getData(String id) {
        new AsyncTask<String, String, String>() {

            @Override
            protected void onPreExecute() {
            }

            @Override
            protected String doInBackground(String... strings) {
                try {
                    String web= "https://tux.csicxt.com/index.php";
                    String action= Jsoup.connect(web)
                            .ignoreContentType(true)
                            .data("op","del_post")
                            .data("account_id","63")
                            .data("shash","1722326")
                            .data("post_id",id)
                            .post().text();

                    DataSource = new JSONObject(action);
                }
                catch (Exception e) {
                    Log.e("x","Fetch err:"+e);
                }

                return null;
            }

            @Override
            protected void onPostExecute(String s) {
            }
        }.execute();
    }
}