#!/bin/bash
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=16
#SBATCH --time=100:00:00
#SBATCH --job-name=MASS_pre1
#SBATCH --partition=devel
#SBATCH --mail-type=ALL
#SBATCH --mail-user=rachitbansal2500@gmail.com
#SBATCH --gres=gpu:M40:1 --constraint='gpu_mem:24GB'

sh pre_training.sh
