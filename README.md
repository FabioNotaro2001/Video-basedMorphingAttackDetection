Video-based Morphing Attack Detection (V-MAD)

This repository contains the code, datasets and experiments developed as part of my Master's thesis at the University of Bologna:
"Video-based Morphing Attack Detection" (Academic Year 2024/2025, Supervisor: Prof.ssa Annalisa Franco).

The thesis explores a novel approach to Morphing Attack Detection (MAD) by leveraging video sequences instead of traditional single-image or differential-image methods.

📜 Abstract

Face morphing attacks represent a significant threat to biometric security systems such as those deployed at airport border controls. By blending facial images of two individuals, an attacker can create a synthetic image capable of fooling both automated and human verification.

In this work, we:

Review existing MAD approaches: S-MAD (Single-image MAD) and D-MAD (Differential-image MAD).

Propose V-MAD (Video-based Morphing Attack Detection), which processes multiple frames from a video to improve detection accuracy.

Introduce a new dataset — GazeWay — meeting ICAO standards, containing ICAO and non-ICAO compliant frontal photos, and multiple video sequences under varying conditions.

Explore score fusion strategies and integrate Face Image Quality Assessment (FIQA) metrics to enhance performance.

Demonstrate that V-MAD can outperform traditional D-MAD methods, especially when combined with quality-aware frame selection.

📂 Repository Structure

.
├── datasets/          # Scripts and instructions for dataset handling (e.g., GazeWay)
├── preprocessing/     # Face detection, alignment, and embedding extraction
├── dmads/             # Differential Morphing Attack Detection implementations
├── vmads/             # Video-based MAD aggregation and quality integration
├── experiments/       # Experimental scripts and evaluation protocols
├── results/           # DET curves, metrics, and comparative results
└── utils/             # Helper functions for data loading, plotting, etc.


📊 GazeWay Dataset

Collected specifically for this thesis at the University of Bologna, GazeWay contains:

65 subjects

ICAO-compliant and non-ICAO-compliant frontal photos (3024×5376)

6 videos per subject at 30 FPS (RGB + depth), captured in:

Two environments (office with mixed lighting, underground parking with artificial lighting)

Three poses: frontal gaze, looking around, looking around with partial occlusion

Note: Due to privacy constraints, the GazeWay dataset is not publicly available. Contact the authors for research collaboration.

⚙️ Requirements

Python ≥ 3.8

PyTorch ≥ 1.10

OpenCV ≥ 4.5

InsightFace (for ArcFace)

NumPy, Matplotlib, Pandas, Scikit-learn

Intel RealSense SDK (for depth data handling)

Install dependencies:

pip install -r requirements.txt


🚀 Usage
1️⃣ Preprocessing

Detect faces, align them, and extract embeddings using ArcFace:

python preprocessing/face_preprocess.py --input_path <dataset_path>


2️⃣ Differential MAD

Run a D-MAD model on ICAO photo + video frame pairs:

python dmads/run_dmad.py --doc_photo <path> --frames <frames_dir>


3️⃣ Video-based MAD

Aggregate D-MAD scores over video frames (average, median, voting, or quality-weighted):

python vmads/run_vmad.py --doc_photo <path> --video <video_path> --aggregation average


📈 Evaluation

Metrics follow ISO standards for MAD:

APCER (Attack Presentation Classification Error Rate)

BPCER (Bona Fide Presentation Classification Error Rate)

EER (Equal Error Rate)

DET curves can be generated:

python experiments/draw_det.py --results_dir results/


🔍 Key Findings

Even simple score aggregation across frames improves morph detection.

Quality-based frame selection (using FIQA methods such as MagFace, CR-FIQA, SER-FIQ) yields further gains.

V-MAD outperforms traditional D-MAD, especially in challenging conditions like poor lighting or partial occlusions.

📚 References

The full methodology, experiments, and results are described in the thesis:

Fabio Notaro, "Video-based Morphing Attack Detection", Master's Thesis, University of Bologna, 2025.

📝 License

This project is for academic and research use only.
For commercial applications, please contact the author.
