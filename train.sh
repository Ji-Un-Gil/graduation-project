#!/bin/bash

#SBATCH --job-name train_gju_cd
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-gpu=8
#SBATCH --mem-per-gpu=32G
#SBATCH --time 1-0
#SBATCH --partition batch_ce_ugrad
#SBATCH -o slurm/logs/slurm-%A_%x.out

. /data/opt/anaconda3/etc/profile.d/conda.sh
conda activate pytorch1.12.1_p38

pip uninstall -y -r requirements.txt
pip install loguru
pip install lightning
pip install -U 'wandb>=0.12.10'
pip install torch torchvision torchaudio

python train.py --gradient_clip_val 1.0 --batch_size 4 --num_workers 4

exit 0
