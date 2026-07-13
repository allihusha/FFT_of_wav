import numpy as np
import torch
from df import enhance, init_df


def filter_noise(audio):
    model, df_state, *_ = init_df()
    audio_tensor = torch.tensor(audio, dtype=torch.float32).unsqueeze(0)
    enhanced = enhance(model, df_state, audio_tensor)
    return enhanced.squeeze(0).numpy()

def compute_snr(signal, noise):
    power_signal = np.mean(signal ** 2)
    power_noise = np.mean(noise ** 2)
    return 10 * np.log10(power_signal / power_noise)