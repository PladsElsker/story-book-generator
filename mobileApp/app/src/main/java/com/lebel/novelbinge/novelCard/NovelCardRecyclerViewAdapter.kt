package com.lebel.novelbinge.novelCard

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.FrameLayout
import android.widget.TextView
import androidx.core.os.bundleOf
import androidx.navigation.Navigation
import androidx.recyclerview.widget.RecyclerView
import com.lebel.novelbinge.R
import com.lebel.novelbinge.domain.NovelData

class NovelCardRecyclerViewAdapter(private val dataSet: List<NovelData>) :
    RecyclerView.Adapter<NovelCardRecyclerViewAdapter.ViewHolder>() {

    class ViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val textView: TextView
        val frameLayout: FrameLayout

        init {
            textView = view.findViewById(R.id.textView)
            frameLayout = view.findViewById(R.id.novelCard)
        }
    }

    override fun onCreateViewHolder(viewGroup: ViewGroup, viewType: Int): ViewHolder {
        val view = LayoutInflater.from(viewGroup.context)
            .inflate(R.layout.novel_card_recycler_view, viewGroup, false)

        return ViewHolder(view)
    }

    override fun onBindViewHolder(viewHolder: ViewHolder, position: Int) {
        viewHolder.textView.text = dataSet[position].title

        viewHolder.frameLayout.setOnClickListener {
            val bundle = bundleOf("folderName" to dataSet[position].folderName)
            Navigation.findNavController(viewHolder.itemView)
                .navigate(R.id.action_NovelList_to_ReadNovel, bundle)
        }
    }

    override fun getItemCount() = dataSet.size
}
