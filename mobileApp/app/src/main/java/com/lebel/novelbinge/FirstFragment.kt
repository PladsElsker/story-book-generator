package com.lebel.novelbinge

import NovelCardRecyclerViewAdapter
import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.lebel.novelbinge.databinding.FragmentFirstBinding
import java.io.File
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive

/**
 * A simple [Fragment] subclass as the default destination in the navigation.
 */
class FirstFragment : Fragment() {

    private var _binding: FragmentFirstBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentFirstBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        val novelsFolder = File(requireContext().getExternalFilesDir(null), "novels")
        novelsFolder.mkdirs()
        val novelFolders = novelsFolder.listFiles()?.filter { it.isDirectory } ?: emptyList()
        val chapterFiles = novelFolders.map { File(it, "novel.json") }
        val chapterJsonObjects = chapterFiles.map { Json.parseToJsonElement(it.readText()) }
        val chapterTitles =
            chapterJsonObjects.mapNotNull { it.jsonObject["title"]?.jsonPrimitive?.content }

        val customAdapter = NovelCardRecyclerViewAdapter(chapterTitles)

        val recyclerView: RecyclerView? = getView()?.findViewById(R.id.novels)
        recyclerView?.adapter = customAdapter
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}