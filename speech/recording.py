import pyaudio
import wave
from pydub import AudioSegment


def record_audio(output_file, duration=5, sample_rate=44100, channels=2, chunk_size=1024):
    audio_format = pyaudio.paInt16
    audio = pyaudio.PyAudio()

    print("recording...")

    # open stream
    stream = audio.open(format=audio_format,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    frames = []

    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("recording finished")

    # Zatrzymaj i zamknij strumień
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Zapisz nagranie do pliku WAV
    wav_file = output_file.replace('.mp3', '.wav')
    wf = wave.open(wav_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(audio_format))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Konwertuj plik WAV do MP3
    audio_segment = AudioSegment.from_wav(wav_file)
    audio_segment.export(output_file, format="mp3")

    print(f"file save as {output_file}")


if __name__ == "__main__":
    record_audio("output.mp3", duration=5)
