package prj_2.stu_1722326.Fragments;

import android.content.Context;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentPagerAdapter;


public class FragmentAdapter extends FragmentPagerAdapter {
    Context context;

    public FragmentAdapter(FragmentManager fm, Context context) {
        super(fm);
        this.context = context;
    }

    @Override
    public Fragment getItem(int position) {
        if (position == 0)
            return FirstFragment.getINSTANCE();
        else if (position == 1)
            return SecondFragment.getINSTANCE();
        return null;
    }

    @Override
    public int getCount() {
        return 2;
    }

    @Nullable
    @Override
    public CharSequence getPageTitle(int position) {
        switch (position) {
            case 0:
            return "First Fragment";
            case 1:
            return "Second Fragment";
        }
        return "";
    }
}
