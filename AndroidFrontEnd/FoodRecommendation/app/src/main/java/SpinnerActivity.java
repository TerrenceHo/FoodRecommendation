import android.app.Activity;
import android.view.View;
import android.widget.AdapterView;

/**
 * Created by nilay on 9/16/2017.
 */

public class SpinnerActivity extends Activity implements AdapterView.OnItemSelectedListener {

    @Override
    public void onItemSelected(AdapterView<?> parent, View view,
                               int pos, long id) {
        // An item was selected. You can retrieve the selected item using
        // parent.getItemAtPosition(pos)
    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {
        // Another interface callback
    }
}

