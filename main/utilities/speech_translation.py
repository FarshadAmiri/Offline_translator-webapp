import os
import whisper
import torch
from main.utilities.pre_post_text_processing import modify_translation, preprocess_text, analyse_text, postprocess_text
from main.utilities.argos import translate
from TTS.api import TTS
import tempfile
import torchaudio
from pydub import AudioSegment
from main.models import *


temp_dir = r"D:\Projects\Offline_translator-webapp\documents_repo\temp"


def speech_to_text(file_path, lang):
    model = whisper.load_model("medium")
    result = model.transcribe(file_path, language=lang)
    transcription = result["text"]
    return transcription


import re

def split_text_for_tts(text, max_length=250):
    # Split by sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(sentence) > max_length:
            # If a single sentence is too long, split further by commas or other punctuation
            sub_sentences = re.split(r'[,;:"\'()]', sentence)
            for sub in sub_sentences:
                if len(current_chunk) + len(sub) + 1 <= max_length:
                    current_chunk += " " + sub
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = sub
        else:
            if len(current_chunk) + len(sentence) + 1 <= max_length:
                current_chunk += " " + sentence
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def generate_speech(text, lang, output_path, translation_object_id, temp_dir):
    translation_object = FileTranslationTask.objects.get(task_id=translation_object_id)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    if lang in ["en", "ar"]:
        reference_speaker = r"D:\Projects\Offline_translator-webapp\main\utilities\obama.ogg"
        tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        
        text_chunks = split_text_for_tts(text)
        print("\ntext_chunks:\n", text_chunks, "\n\n")
        n_chunks = len(text_chunks)
        temp_files = []

        for i, chunk in enumerate(text_chunks):
            temp_file = os.path.join(temp_dir, f"chunk_{i}.wav")
            tts.tts_to_file(chunk, file_path=temp_file, speaker_wav=reference_speaker, language=lang)
            temp_files.append(temp_file)

            progress = int((i + 1) * 100 / n_chunks)
            translation_object.progress = progress
            translation_object.save()

        # Concatenate audio files
        combined_audio = AudioSegment.empty()
        for temp_file in temp_files:
            combined_audio += AudioSegment.from_wav(temp_file)

        # Save final combined audio
        combined_audio.export(output_path, format="wav")

        # Clean up temp files
        for temp_file in temp_files:
            os.remove(temp_file)

    elif lang == "fa":
        print("\nFarsi TTS not yet supported.\n")

    return


def speech_translator(input_path, output_path, source_lang, target_lang, translation_object_id):
    global temp_dir
    translation_object = FileTranslationTask.objects.get(task_id=translation_object_id)

    translation_object.progress = "transcripting"
    translation_object.save()

    transcription = speech_to_text(input_path, source_lang)

    translation_object.progress = "translating"
    translation_object.save()

    source_text_preprocessed = preprocess_text(transcription)
    source_text_analysis = analyse_text(transcription)
    translation = translate(source_text_preprocessed, source_lang, target_lang)
    translation = postprocess_text(translation, source_text_analysis)

    translation_object.progress = "generating speech"
    translation_object.save()

    generate_speech(translation, target_lang, output_path, translation_object_id, temp_dir)

    translation_object.progress = "100"
    translation_object.save()
    return