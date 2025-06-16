import wave
import numpy as np

def encode_image_to_audio(audio_in, image_in, audio_out):
    # Buka file audio
    with wave.open(audio_in, 'rb') as wav_in:
        params = wav_in.getparams()
        frames = wav_in.readframes(wav_in.getnframes())

    audio_data = np.frombuffer(frames, dtype=np.uint8).copy()

    # Baca file gambar dan ubah ke bentuk bitstream
    with open(image_in, 'rb') as f:
        image_bytes = f.read()
    image_bits = ''.join(format(byte, '08b') for byte in image_bytes)

    # Simpan panjang data (32-bit header)
    image_len = len(image_bits)
    if image_len > (len(audio_data) - 32):
        raise ValueError("Audio file too small to hide the image.")

    header = format(image_len, '032b')
    full_bits = header + image_bits

    # Sisipkan bit ke LSB
    for i in range(len(full_bits)):
        audio_data[i] = (audio_data[i] & 0xFE) | int(full_bits[i])

    # Simpan audio baru
    with wave.open(audio_out, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(audio_data.tobytes())

    print("✅ Image successfully encoded into audio.")

# Contoh pemakaian
encode_image_to_audio('input.wav', 'secret.jpg', 'output_stego.wav')
