#!/bin/bash
# GCP Multi-Account Spot L4 GPU Provisioning Script
# This script provides the commands to spin up cheap Preemptible (Spot) L4 GPUs 
# for the Lumina AI training pipeline. 

echo "============================================================"
echo " LUMINA AI - GCP SPOT INSTANCE PROVISIONING HELPER"
echo "============================================================"

# Define parameters for a cost-effective G2 (L4 GPU) instance
ZONE="us-central1-a"
INSTANCE_NAME="lumina-training-node"
MACHINE_TYPE="g2-standard-4" # 4 vCPU, 16GB RAM, 1x L4 GPU (24GB VRAM)
IMAGE_FAMILY="common-cu121-debian-11"
IMAGE_PROJECT="deeplearning-platform-release"
DISK_SIZE="100GB"

echo "To provision the training node for Account 1, 2, or 3, run the following command:"
echo ""
echo "gcloud compute instances create $INSTANCE_NAME \\"
echo "  --project=YOUR_PROJECT_ID \\"
echo "  --zone=$ZONE \\"
echo "  --machine-type=$MACHINE_TYPE \\"
echo "  --provisioning-model=SPOT \\"
echo "  --instance-termination-action=STOP \\"
echo "  --maintenance-policy=TERMINATE \\"
echo "  --image-family=$IMAGE_FAMILY \\"
echo "  --image-project=$IMAGE_PROJECT \\"
echo "  --boot-disk-size=$DISK_SIZE \\"
echo "  --boot-disk-type=pd-balanced \\"
echo "  --accelerator=type=nvidia-l4,count=1 \\"
echo "  --metadata=\"install-nvidia-driver=True\""
echo ""
echo "Note: SPOT instances are up to 70% cheaper but can be preempted."
echo "Ensure your training scripts (train_plc_llm.py) are saving checkpoints frequently."
