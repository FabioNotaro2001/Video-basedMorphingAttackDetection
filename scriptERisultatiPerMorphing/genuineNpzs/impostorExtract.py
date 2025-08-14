import os
import numpy as np
import tensorflow as tf
from pathlib import Path
from tqdm import tqdm
from deepface import DeepFace

# Disattiva log TensorFlow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

print("GPU disponibili: ", tf.config.list_physical_devices('GPU'))

def extract_features(image_path: str) -> np.ndarray:
    features = DeepFace.represent(
        img_path=image_path,
        model_name="ArcFace",
        detector_backend="retinaface",
        normalization="ArcFace",
        align=False,
        enforce_detection=False,
    )
    if not features or len(features) != 1 or features[0]["embedding"] is None:
        raise ValueError(f"Face could not be detected in {image_path}.")
    return np.array(features[0]["embedding"], dtype=np.float32)

def main():
    root = Path("./")
    morphed_dir = root / "morphed"
    impostor_output_dir = root / "impostorNpzs"
    impostor_output_dir.mkdir(exist_ok=True)

    morphed_images = list(morphed_dir.glob("*.*"))

    for morphed_image in tqdm(morphed_images, desc="Processing morphed images"):
        try:
            doc_features = extract_features(str(morphed_image))
        except Exception as e:
            print(f"Failed to extract from morphed image {morphed_image}: {e}")
            continue

        parts = morphed_image.stem.split("-")
        if len(parts) < 12:
            print(f"Filename format invalid for {morphed_image}")
            continue

        try:
            id1 = parts[0][2:]  # Es: 'ID001' -> '001'
            id2 = parts[11][4:]  # Es: 'toID002' -> '002'
        except Exception as e:
            print(f"Error parsing IDs from {morphed_image.name}: {e}")
            continue

        for current_id in [id1, id2]:
            subject_dir = root / f"ID{current_id}"
            if not subject_dir.exists():
                print(f"Missing directory for ID{current_id}")
                continue

            video_seq_dir = subject_dir / "video_sequences"
            for seq in ["sequence_01", "sequence_02"]:
                for subdir in ["frontal_gaze", "looking_around", "looking_around_with_occlusion"]:
                    rgb_dir = video_seq_dir / seq / subdir / "rgb"
                    if not rgb_dir.exists():
                        continue

                    for img_path in rgb_dir.glob("*.*"):
                        try:
                            live_features = extract_features(str(img_path))
                            img_parts = img_path.stem.split("-")
                            if len(img_parts) < 2:
                                continue

                            C = img_parts[0][:3]  # ID del soggetto da live image
                            D = seq[-2:]  # '01' o '02'
                            E = subdir
                            F = img_parts[-2]  # Penultimo campo

                            npz_name = f"{id1}-{id2}-{C}-{D}-{E}-{F}.npz"

                            np.savez_compressed(
                                impostor_output_dir / npz_name,
                                doc=str(morphed_image.relative_to(root)),
                                live=str(img_path.relative_to(root)),
                                cls=np.int32(1),
                                doc_features=doc_features,
                                live_features=live_features,
                            )
                        except Exception as e:
                            print(f"Error processing {img_path}: {e}")

if __name__ == "__main__":
    main()
