package com.lebel.novelbinge

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.RecyclerView
import com.lebel.novelbinge.databinding.FragmentNovelListBinding
import com.lebel.novelbinge.domain.NovelFileReader
import com.lebel.novelbinge.novelCard.NovelCardRecyclerViewAdapter

class NovelList : Fragment() {
    private var _binding: FragmentNovelListBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentNovelListBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        createNovelList()
    }

    private fun createNovelList() {
        val customAdapter =
            NovelCardRecyclerViewAdapter(NovelFileReader.readAllTitles(requireContext()))
        val recyclerView: RecyclerView? = view?.findViewById(R.id.novels)
        recyclerView?.adapter = customAdapter
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
