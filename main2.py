import subprocess
import os
import requests
import json
import streamlit as st
import tempfile

# Constants
OLLAMA_SERVER_URL = "http://localhost:11434"  # Replace this with your actual Ollama server URL if different
WHISPER_MODEL_DIR = "D:/MALAV/America/LLms/AI-Powered-Audio-Summarizer-main/whisper.cpp/models"  # Directory where whisper models are stored

# Prompts for different audio types
prompts = {
    "Meeting Recording": """You are given a transcript from a meeting. Please provide a detailed summary of the discussion, including:
    1. The main topic or subject of the meeting.
    2. Key points and decisions made.
    3. Action items or next steps.
    4. The tone of the discussion (e.g., formal, casual, urgent).
    5. Participant interactions and engagement levels.
    6. Any challenges or disagreements discussed.
    7. Follow-up tasks or deadlines mentioned.""",

    "Song": """You are given a transcript from a song. Please provide a detailed summary, including:
    1. The main theme or message of the song.
    2. The emotional tone and mood (e.g., happy, sad, romantic, angry).
    3. The names of the singers, artists, or bands if mentioned.
    4. Notable lyrics or phrases and their significance.
    5. Musical style, genre, or instrumentation mentioned.
    6. Cultural or historical context if relevant.
    7. The overall impact or message of the song.""",

    "Lecture": """You are given a transcript from an educational lecture. Please provide a detailed summary, including:
    1. The main subject and key concepts covered.
    2. Important definitions, theories, or principles explained.
    3. Examples, case studies, or illustrations used.
    4. Key takeaways and learning points.
    5. Any assignments, exercises, or recommended further reading.
    6. The tone and teaching style of the lecturer (e.g., engaging, formal, interactive).
    7. Questions asked by students and answers provided.""",

    "Podcast": """You are given a transcript from a podcast. Please provide a detailed summary, including:
    1. The main topic and theme of the episode.
    2. Key discussions, insights, or arguments shared.
    3. Guest speakers and their contributions or expertise.
    4. Notable quotes or memorable moments.
    5. Resources, books, or references mentioned.
    6. The tone and style of the podcast (e.g., conversational, informative, humorous).
    7. Key takeaways or calls to action for the audience.""",

    "Interview": """You are given a transcript from an interview. Please provide a detailed summary, including:
    1. The background of the interviewee and interviewer.
    2. Main topics or themes discussed.
    3. Key insights, experiences, or stories shared.
    4. Notable quotes or memorable moments.
    5. Professional achievements or projects mentioned.
    6. The tone and style of the interview (e.g., formal, casual, confrontational).
    7. Future plans, goals, or advice shared by the interviewee.""",

    "Audiobook": """You are given a transcript from an audiobook. Please provide a detailed summary, including:
    1. The genre and style of the book (e.g., fiction, non-fiction, self-help).
    2. Main plot points or key concepts covered.
    3. Character descriptions or important figures.
    4. Notable quotes or passages and their significance.
    5. Themes, motifs, or underlying messages.
    6. The tone and narration style (e.g., dramatic, conversational).
    7. The overall impact or message of the book.""",

    "Voice Memo": """You are given a transcript from a voice memo. Please provide a detailed summary, including:
    1. The main purpose or subject of the memo.
    2. Key points, instructions, or reminders.
    3. Time-sensitive information or deadlines.
    4. Follow-up tasks or action items.
    5. Context or background information.
    6. The tone and urgency of the memo (e.g., urgent, casual, formal).
    7. Any additional details or clarifications provided.""",

    "Conference Talk": """You are given a transcript from a conference talk. Please provide a detailed summary, including:
    1. The main topic and field of discussion.
    2. Key innovations, findings, or ideas presented.
    3. Methodologies, approaches, or frameworks discussed.
    4. The impact and implications of the work.
    5. Questions from the audience and answers provided.
    6. The tone and style of the presentation (e.g., technical, inspirational).
    7. Key takeaways or recommendations for the audience."""
}

# prompts = {
#     "Meeting Recording": """You are given a transcript from a meeting. Please provide a detailed and structured summary of the discussion. Include only the points that are explicitly mentioned in the transcript. If a point is not mentioned, do not include it in the summary. The possible points to include are:
#     1. **Main Topic**: Identify the primary subject or agenda of the meeting.
#     2. **Key Points**: Summarize the main points discussed, including any data, facts, or figures mentioned.
#     3. **Decisions Made**: Highlight any decisions or resolutions reached during the meeting.
#     4. **Action Items**: List specific tasks, responsibilities, or next steps assigned to participants.
#     5. **Tone and Dynamics**: Describe the tone of the discussion (e.g., formal, casual, tense) and the level of participant engagement.
#     6. **Challenges or Disagreements**: Note any conflicts, disagreements, or challenges raised during the meeting.
#     7. **Follow-Up**: Mention any deadlines, follow-up meetings, or pending actions.
#     8. **Additional Insights**: Provide any other relevant observations or insights from the discussion.

#     **Instructions**:
#     - Only include points that are explicitly mentioned in the transcript.
#     - If a point is not mentioned, skip it entirely.
#     - Do not make up or assume any information.

#     **Transcript**:
#     {text}

#     **Summary**:
#     """,

#     "Song": """You are given a transcript from a song. Please provide a detailed and insightful summary. Include only the points that are explicitly mentioned in the transcript. If a point is not mentioned or not applicable, do not include it in the summary. The possible points to include are:
#     1. **Lyrics Analysis**:
#        - Identify the main theme or message of the song.
#        - Describe the emotional tone and mood (e.g., happy, sad, romantic, angry).
#     2. **Song and Artist Identification**:
#        - Based on the lyrics, make an educated guess about the likely song title and singer/artist. If the song title or artist is not explicitly mentioned, skip this point entirely.
#     3. **Notable Lyrics**:
#        - Highlight significant or memorable lines and explain their meaning and significance.
#     4. **Musical Style and Genre**:
#        - Infer the musical style, genre, or instrumentation based on the lyrics (e.g., rock, pop, hip-hop).
#     5. **Cultural or Historical Context**:
#        - Provide any relevant cultural, historical, or social context that enhances the understanding of the song. If no context is mentioned, skip this point entirely.
#     6. **Overall Impact**:
#        - Summarize the overall message or impact of the song and how it might resonate with listeners.
#     7. **Similar Songs or Artists**:
#        - Suggest similar songs or artists based on the style and theme of the lyrics. If no similar songs or artists are mentioned, skip this point entirely.

#     **Instructions**:
#     - Only include points that are explicitly mentioned or can be inferred from the transcript.
#     - If a point is not mentioned or not applicable, skip it entirely.
#     - Do not include phrases like "Not applicable" or "No information available" in the summary.
#     - Ensure the summary is concise and only includes relevant information.

#     **Transcript**:
#     {text}

#     **Summary**:
#     """,

#     "Lecture": """You are given a transcript from an educational lecture. Please provide a detailed and structured summary. Include only the points that are explicitly mentioned in the transcript. If a point is not mentioned, do not include it in the summary. The possible points to include are:
#     1. **Main Subject**: Identify the primary topic or subject of the lecture.
#     2. **Key Concepts**: Summarize the main ideas, theories, or principles discussed.
#     3. **Examples and Illustrations**: Highlight any examples, case studies, or practical applications mentioned.
#     4. **Key Takeaways**: List the most important points or lessons from the lecture.
#     5. **Assignments or Readings**: Mention any assignments, exercises, or recommended readings.
#     6. **Tone and Style**: Describe the lecturer's tone and teaching style (e.g., engaging, formal, interactive).
#     7. **Questions and Answers**: Summarize any questions asked by students and the lecturer's responses.
#     8. **Additional Insights**: Provide any other relevant observations or insights from the lecture.

#     **Instructions**:
#     - Only include points that are explicitly mentioned in the transcript.
#     - If a point is not mentioned, skip it entirely.
#     - Do not make up or assume any information.

#     **Transcript**:
#     {text}

#     **Summary**:
#     """,

#     "Podcast": """You are given a transcript from a podcast episode. Please provide a detailed and engaging summary. Include only the points that are explicitly mentioned in the transcript. If a point is not mentioned, do not include it in the summary. The possible points to include are:
#     1. **Main Topic**: Identify the primary theme or subject of the episode.
#     2. **Key Discussions**: Summarize the main discussions, insights, or arguments shared.
#     3. **Guest Speakers**: Highlight any guest speakers and their contributions or expertise.
#     4. **Notable Quotes**: Mention any memorable quotes or moments from the episode.
#     5. **Resources or References**: List any books, articles, or resources mentioned.
#     6. **Tone and Style**: Describe the tone and style of the podcast (e.g., conversational, informative, humorous).
#     7. **Key Takeaways**: Summarize the main lessons or calls to action for the audience.
#     8. **Additional Insights**: Provide any other relevant observations or insights from the episode.

#     **Instructions**:
#     - Only include points that are explicitly mentioned in the transcript.
#     - If a point is not mentioned, skip it entirely.
#     - Do not make up or assume any information.

#     **Transcript**:
#     {text}

#     **Summary**:
#     """,

#     "Interview": """You are given a transcript from an interview. Please provide a detailed and structured summary. Include only the points that are explicitly mentioned in the transcript. If a point is not mentioned, do not include it in the summary. The possible points to include are:
#     1. **Background**: Provide context about the interviewee and interviewer.
#     2. **Main Topics**: Summarize the primary topics or themes discussed.
#     3. **Key Insights**: Highlight the most important insights, experiences, or stories shared.
#     4. **Notable Quotes**: Mention any memorable quotes or moments from the interview.
#     5. **Professional Achievements**: Discuss any notable achievements or projects mentioned by the interviewee.
#     6. **Tone and Style**: Describe the tone and style of the interview (e.g., formal, casual, confrontational).
#     7. **Future Plans**: Mention any future plans, goals, or advice shared by the interviewee.
#     8. **Additional Insights**: Provide any other relevant observations or insights from the interview.

#     **Instructions**:
#     - Only include points that are explicitly mentioned in the transcript.
#     - If a point is not mentioned, skip it entirely.
#     - Do not make up or assume any information.

#     **Transcript**:
#     {text}

#     **Summary**:
#     """,

#     "Audiobook": """You are given a transcript from an audiobook. Please provide a detailed and insightful summary. Include only the points that are explicitly mentioned in the transcript. If a point is not mentioned, do not include it in the summary. The possible points to include are:
#     1. **Genre and Style**: Identify the genre and style of the book (e.g., fiction, non-fiction, self-help).
#     2. **Main Plot or Concepts**: Summarize the main plot points or key concepts covered.
#     3. **Characters or Figures**: Describe the main characters or important figures in the book.
#     4. **Notable Quotes**: Highlight any significant quotes or passages and explain their meaning.
#     5. **Themes and Messages**: Discuss the main themes, motifs, or underlying messages of the book.
#     6. **Tone and Narration**: Describe the tone and narration style (e.g., dramatic, conversational).
#     7. **Overall Impact**: Summarize the overall impact or message of the book.
#     8. **Additional Insights**: Provide any other relevant observations or insights from the book.

#     **Instructions**:
#     - Only include points that are explicitly mentioned in the transcript.
#     - If a point is not mentioned, skip it entirely.
#     - Do not make up or assume any information.

#     **Transcript**:
#     {text}

#     **Summary**:
#     """,

#     "Voice Memo": """You are given a transcript from a voice memo. Please provide a detailed and actionable summary. Include only the points that are explicitly mentioned in the transcript. If a point is not mentioned, do not include it in the summary. The possible points to include are:
#     1. **Purpose**: Identify the main purpose or subject of the memo.
#     2. **Key Points**: Summarize the main points, instructions, or reminders mentioned.
#     3. **Time-Sensitive Information**: Highlight any deadlines or time-sensitive details.
#     4. **Action Items**: List any follow-up tasks or action items.
#     5. **Context**: Provide any relevant background or context for the memo.
#     6. **Tone and Urgency**: Describe the tone and urgency of the memo (e.g., urgent, casual, formal).
#     7. **Additional Details**: Mention any other important details or clarifications provided.
#     8. **Additional Insights**: Provide any other relevant observations or insights from the memo.

#     **Instructions**:
#     - Only include points that are explicitly mentioned in the transcript.
#     - If a point is not mentioned, skip it entirely.
#     - Do not make up or assume any information.

#     **Transcript**:
#     {text}

#     **Summary**:
#     """,

#     "Conference Talk": """You are given a transcript from a conference talk. Please provide a detailed and structured summary. Include only the points that are explicitly mentioned in the transcript. If a point is not mentioned, do not include it in the summary. The possible points to include are:
#     1. **Main Topic**: Identify the primary topic and field of discussion.
#     2. **Key Innovations or Findings**: Summarize the main innovations, findings, or ideas presented.
#     3. **Methodologies**: Highlight any methodologies, approaches, or frameworks discussed.
#     4. **Impact and Implications**: Discuss the potential impact and implications of the work.
#     5. **Questions and Answers**: Summarize any questions from the audience and the speaker's responses.
#     6. **Tone and Style**: Describe the tone and style of the presentation (e.g., technical, inspirational).
#     7. **Key Takeaways**: List the main lessons or recommendations for the audience.
#     8. **Additional Insights**: Provide any other relevant observations or insights from the talk.

#     **Instructions**:
#     - Only include points that are explicitly mentioned in the transcript.
#     - If a point is not mentioned, skip it entirely.
#     - Do not make up or assume any information.

#     **Transcript**:
#     {text}

#     **Summary**:
#     """
# }
def get_available_models() -> list[str]:
    """
    Retrieves a list of all available models from the Ollama server and extracts the model names.

    Returns:
        A list of model names available on the Ollama server.
    """
    response = requests.get(f"{OLLAMA_SERVER_URL}/api/tags")
    if response.status_code == 200:
        models = response.json()["models"]
        llm_model_names = [model["model"] for model in models]  # Extract model names
        return llm_model_names
    else:
        raise Exception(
            f"Failed to retrieve models from Ollama server: {response.text}"
        )

def get_available_whisper_models() -> list[str]:
    """
    Retrieves a list of available Whisper models based on downloaded .bin files in the whisper.cpp/models directory.
    Filters out test models and only includes official Whisper models (e.g., base, small, medium, large).

    Returns:
        A list of available Whisper model names (e.g., 'base', 'small', 'medium', 'large-V3').
    """
    # List of acceptable official Whisper models
    valid_models = ["base", "small", "medium", "large", "large-V3"]

    # Get the list of model files in the models directory
    model_files = [f for f in os.listdir(WHISPER_MODEL_DIR) if f.endswith(".bin")]

    # Filter out test models and models that aren't in the valid list
    whisper_models = [
        os.path.splitext(f)[0].replace("ggml-", "")
        for f in model_files
        if any(valid_model in f for valid_model in valid_models) and "test" not in f
    ]

    # Remove any potential duplicates
    whisper_models = list(set(whisper_models))

    return whisper_models

def summarize_with_model(llm_model_name: str, context: str, text: str, audio_type: str) -> str:
    """
    Uses a specified model on the Ollama server to generate a detailed and impactful summary.
    Handles streaming responses by processing each line of the response.

    Args:
        llm_model_name (str): The name of the model to use for summarization.
        context (str): Optional context for the summary, provided by the user.
        text (str): The transcript text to summarize.
        audio_type (str): The type of audio (e.g., "Meeting Recording", "Song").

    Returns:
        str: The generated summary text from the model.
    """
    prompt = prompts.get(audio_type, "No prompt available for this audio type.")
    prompt = f"{prompt}\n\nContext: {context if context else 'No additional context provided.'}\n\nTranscript:\n{text}\n\nSummary:"

    headers = {"Content-Type": "application/json"}
    data = {"model": llm_model_name, "prompt": prompt}

    response = requests.post(
        f"{OLLAMA_SERVER_URL}/api/generate", json=data, headers=headers, stream=True
    )

    if response.status_code == 200:
        full_response = ""
        try:
            # Process the streaming response line by line
            for line in response.iter_lines():
                if line:
                    # Decode each line and parse it as a JSON object
                    decoded_line = line.decode("utf-8")
                    json_line = json.loads(decoded_line)
                    # Extract the "response" part from each JSON object
                    full_response += json_line.get("response", "")
                    # If "done" is True, break the loop
                    if json_line.get("done", False):
                        break
            return full_response
        except json.JSONDecodeError:
            print("Error: Response contains invalid JSON data.")
            return f"Failed to parse the response from the server. Raw response: {response.text}"
    else:
        raise Exception(
            f"Failed to summarize with model {llm_model_name}: {response.text}"
        )

def preprocess_audio_file(audio_file_path: str) -> str:
    """
    Converts the input audio file to a WAV format with 16kHz sample rate and mono channel.
    The input audio is converted into  WAV format (16kHz, mono) as whisper model works best with mono channel
    Here we will be using ffmeg to 

    Args:
        audio_file_path (str): Path to the input audio file.

    Returns:
        str: The path to the preprocessed WAV file.
    """
    output_wav_file = f"{os.path.splitext(audio_file_path)[0]}_converted.wav"
    ffmpeg_path = "C:\\ffmpeg-7.1-full_build\\bin\\ffmpeg.exe"  # Replace with the actual path to ffmpeg.exe
    cmd = f'"{ffmpeg_path}" -y -i "{audio_file_path}" -ar 16000 -ac 1 "{output_wav_file}"'
    
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    
    print("FFmpeg output:", stdout)
    print("FFmpeg error (if any):", stderr)
    
    if process.returncode != 0:
        raise Exception(f"FFmpeg failed with error: {stderr}")
    
    return output_wav_file

def translate_and_summarize(audio_file_path: str, context: str, whisper_model_name: str, llm_model_name: str, audio_type: str) -> tuple[str, str]:
    """
    Translates the audio file to text using Whisper and summarizes it using the specified LLM model.

    Args:
        audio_file_path (str): Path to the input audio file.
        context (str): Optional context for the summary.
        whisper_model_name (str): The Whisper model to use for transcription.
        llm_model_name (str): The LLM model to use for summarization.
        audio_type (str): The type of audio (e.g., "Meeting Recording", "Song").

    Returns:
        tuple[str, str]: The summary and the path to the transcript file.
    """
    temp_dir = tempfile.gettempdir()
    output_file = os.path.join(temp_dir, f"output_{os.path.basename(audio_file_path)}.txt")

    print("Processing audio file:", audio_file_path)

    # Convert the input file to WAV format if necessary
    audio_file_wav = preprocess_audio_file(audio_file_path)

    print("Audio preprocessed:", audio_file_wav)

    # Set the path to the Whisper binary
    whisper_binary_path = r"D:\\MALAV\\America\\LLms\\AI-Powered-Audio-Summarizer-main\\whisper.cpp\\build\\bin\\whisper-cli.exe"
    print("Whisper binary path:", whisper_binary_path)

    if not os.path.exists(whisper_binary_path):
        raise FileNotFoundError("Whisper binary not found.")
    
    model_path = os.path.abspath(f"D:\\MALAV\\America\\LLms\\AI-Powered-Audio-Summarizer-main\\whisper.cpp\\models\\ggml-{whisper_model_name}.bin")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    # Construct the Whisper command
    whisper_command = f'"{whisper_binary_path}" -m "{model_path}" -f "{os.path.abspath(audio_file_wav)}" > "{output_file}"'
    print("Running command:", whisper_command)

    try:
        # Run the command and redirect output to a file
        subprocess.run(whisper_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Whisper command failed with error: {e.stderr}")
        raise

    # Read the output from the transcript
    with open(output_file, "r", encoding="utf-8") as f:
        transcript = f.read()

    # Format the transcript for better readability
    formatted_transcript = format_transcript(transcript)

    # Save the formatted transcript to a downloadable file
    final_transcript_file = "transcript.txt"
    with open(final_transcript_file, "w", encoding="utf-8") as transcript_f:
        transcript_f.write(formatted_transcript)

    # Generate summary from the transcript using Ollama's model
    summary = summarize_with_model(llm_model_name, context, transcript, audio_type)

    # Clean up temporary files
    os.remove(audio_file_wav)
    os.remove(output_file)

    # Return the downloadable link for the transcript and the summary text
    return summary, final_transcript_file

def format_transcript(transcript: str) -> str:
    """
    Formats the transcript to make it more readable and structured.

    Args:
        transcript (str): The raw transcript text.

    Returns:
        str: The formatted transcript.
    """
    # Split the transcript into lines
    lines = transcript.strip().split("\n")

    # Format each line
    formatted_lines = []
    for line in lines:
        if line.strip():  # Skip empty lines
            # Remove timestamps if present
            if "-->" in line:
                line = line.split("-->")[1].strip()
            formatted_lines.append(line)

    # Join the formatted lines into a single string
    formatted_transcript = "\n".join(formatted_lines)
    return formatted_transcript

def main():
    st.title("🎙️    Audio Summarizer")
    st.write("Upload an audio file and get a detailed summary tailored to your needs.")

    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        audio_type = st.radio(
            "Select the type of audio:",
            ["Meeting Recording", "Song", "Lecture", "Podcast", "Interview", 
             "Audiobook", "Voice Memo", "Conference Talk"]
        )
        whisper_model_name = st.selectbox(
            "Select a Whisper model for audio-to-text conversion",
            get_available_whisper_models(),
            index=0
        )
        llm_model_name = st.selectbox(
            "Select a model for summarization",
            get_available_models(),
            index=0
        )
        context = st.text_input("Context (optional)", placeholder="Provide any additional context for the summary")

    # Main content
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

    if audio_file is not None:
        with st.spinner("Processing your audio file..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_file.write(audio_file.getbuffer())
                tmp_file_path = tmp_file.name

            summary, transcript_file = translate_and_summarize(
                tmp_file_path, context, whisper_model_name, llm_model_name, audio_type
            )

            st.success("Processing complete!")
            st.subheader("Summary")
            st.write(summary)

            st.subheader("Download Transcript")
            with open(transcript_file, "rb") as f:
                st.download_button(
                    label="Download Transcript",
                    data=f,
                    file_name="transcript.txt",
                    mime="text/plain"
                )

            os.remove(tmp_file_path)

if __name__ == "__main__":
    main()