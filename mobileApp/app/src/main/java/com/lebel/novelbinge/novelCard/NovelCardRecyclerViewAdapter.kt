import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.FrameLayout
import android.widget.TextView
import androidx.core.os.bundleOf
import androidx.navigation.Navigation
import androidx.recyclerview.widget.RecyclerView
import com.lebel.novelbinge.domain.NovelData
import com.lebel.novelbinge.R

class NovelCardRecyclerViewAdapter(private val dataSet: List<NovelData>) :
    RecyclerView.Adapter<NovelCardRecyclerViewAdapter.ViewHolder>() {

    /**
     * Provide a reference to the type of views that you are using
     * (custom ViewHolder)
     */
    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val textView: TextView
        val frameLayout: FrameLayout

        init {
            // Define click listener for the ViewHolder's View
            textView = view.findViewById(R.id.textView)
            frameLayout = view.findViewById(R.id.novelCard)
        }
    }

    // Create new views (invoked by the layout manager)
    override fun onCreateViewHolder(viewGroup: ViewGroup, viewType: Int): ViewHolder {
        // Create a new view, which defines the UI of the list item
        val view = LayoutInflater.from(viewGroup.context)
            .inflate(R.layout.novel_card_recycler_view, viewGroup, false)

        return ViewHolder(view)
    }

    // Replace the contents of a view (invoked by the layout manager)
    override fun onBindViewHolder(viewHolder: ViewHolder, position: Int) {

        // Get element from your dataset at this position and replace the
        // contents of the view with that element
        viewHolder.textView.text = dataSet[position].title

        viewHolder.frameLayout.setOnClickListener {
            val bundle = bundleOf("folderName" to dataSet[position].folderName)
            Navigation.findNavController(viewHolder.itemView).navigate(R.id.action_NovelList_to_ReadNovel, bundle)
        }
    }

    // Return the size of your dataset (invoked by the layout manager)
    override fun getItemCount() = dataSet.size

}
