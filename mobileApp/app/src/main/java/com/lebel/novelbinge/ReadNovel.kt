package com.lebel.novelbinge

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import com.lebel.novelbinge.databinding.FragmentReadnovelBinding
import com.lebel.novelbinge.domain.NovelFileReader

class ReadNovel : Fragment() {

    private var _binding: FragmentReadnovelBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentReadnovelBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        val textView: TextView = this.view?.findViewById(R.id.textview) ?: return
        val folderName = arguments?.getString("folderName")

        if (folderName == null) {
            textView.text = "Argument 'folderName' not found"
            return
        }

        textView.text = NovelFileReader.ReadChapterData(requireContext(), folderName).chapters
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}