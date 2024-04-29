package com.lebel.novelbinge.domain

import android.content.Context
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import java.io.File

class NovelFileReader {
    companion object {
        fun ReadAllTitles(context: Context): List<NovelData> {
            val novelsFolder = File(context.getExternalFilesDir(null), "novels")

            // Make sure the folder exists
            novelsFolder.mkdirs()

            val novelFolders = novelsFolder.listFiles()?.filter { it.isDirectory } ?: emptyList()

            return novelFolders.map { novelFolder: File ->
                val jsonObject = Json.parseToJsonElement(File(novelFolder, "novel.json").readText())
                val title = jsonObject.jsonObject["title"]?.jsonPrimitive?.content ?: "No title"
                NovelData(novelFolder.name, title)
            }
        }

        fun ReadChapterData(context: Context, folderName: String): NovelChapterData {
            val novelFile = File(context.getExternalFilesDir(null), "novels/$folderName/novel.json")
            val jsonObject = Json.parseToJsonElement(novelFile.readText())
            val title = jsonObject.jsonObject["title"]?.jsonPrimitive?.content ?: "No title"
            val chapters = jsonObject.jsonObject["chapters"]?.jsonArray?.joinToString {
                it.jsonObject["content"]?.jsonPrimitive?.content ?: "No Chapter"
            } ?: "No Chapters"

            return NovelChapterData(folderName, title, chapters)
        }
    }
}