import wave
import numpy as np

def decode_image_from_audio(stego_audio, output_image):
    with wave.open(stego_audio, 'rb') as wav_in:
        frames = wav_in.readframes(wav_in.getnframes())

    audio_data = np.frombuffer(frames, dtype=np.uint8)

    # Baca header 32-bit (panjang image dalam bit)
    header_bits = ''.join(str(audio_data[i] & 1) for i in range(32))
    image_len = int(header_bits, 2)

    # Baca bit-bit gambar
    image_bits = ''.join(str(audio_data[i + 32] & 1) for i in range(image_len))

    # Ubah ke byte array
    image_bytes = bytes(int(image_bits[i:i+8], 2) for i in range(0, len(image_bits), 8))

    # Simpan sebagai file gambar
    with open(output_image, 'wb') as f:
        f.write(image_bytes)

    print("✅ Image successfully extracted from audio.")

decode_image_from_audio('output_stego.wav', 'recovered.png')
