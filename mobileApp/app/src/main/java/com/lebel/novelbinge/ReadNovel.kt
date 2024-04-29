package com.lebel.novelbinge

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.lebel.novelbinge.databinding.FragmentReadnovelBinding

/**
 * A simple [Fragment] subclass as the second destination in the navigation.
 */
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

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}