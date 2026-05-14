# 🔄 Training Checkpoint & Resume Guide

## ✅ Your Training is Protected!

YOLO automatically saves checkpoints, so you can safely stop and resume training.

## 📁 Where Checkpoints Are Saved

After starting training, checkpoints are saved in:
```
runs/train/<experiment_name>/weights/
├── best.pt     # Best performing model (highest validation mAP)
├── last.pt     # Most recent checkpoint (updated every epoch)
└── best_epoch_X.pt  # Milestone checkpoints (if using train_with_milestones.py)
```

## 🛑 If Training Is Interrupted

**Don't panic!** Your progress is saved. Here's what to do:

### **Option 1: Resume with train.py**

```powershell
# Resume from the last checkpoint
python sds_yolo11\train.py --config cfgs/SOTA Comparison/ours.yaml --data seadrones_data.yaml --resume
```

The `--resume` flag will:
- Look for `last.pt` in your previous run
- Continue training from that epoch
- Keep all training history and metrics

### **Option 2: Resume with train_with_milestones.py**

```powershell
# Resume with the same project and name
python sds_yolo11\train_with_milestones.py --config cfgs/Ablation Study/yolo11.yaml --data surf_swimming_data.yaml --name yolo11-baseline-100ep --resume
```

**Important:** Use the same `--name` as your original training run!

## 💡 How It Works

1. **During Training:**
   - Every epoch: `last.pt` is updated
   - When validation improves: `best.pt` is updated
   - At milestones (10, 29, 100): `best_epoch_X.pt` is saved

2. **When Resuming:**
   - Training loads `last.pt`
   - Continues from the next epoch
   - All optimizer states and metrics are preserved

## 📊 Check Your Training Progress

To see how far your training got before interruption:

```powershell
# Look for the last saved checkpoint
Get-ChildItem -Recurse -Filter "last.pt" runs\train\
```

Or check the training log in the run directory:
```
runs/train/<experiment_name>/results.csv
```

## 🔍 Finding Your Last Run

If you forgot your experiment name:

```powershell
# List all training runs
Get-ChildItem runs\train\ | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

## ⚡ Quick Resume Commands

### Resume Last Training (train.py)
```powershell
python sds_yolo11\train.py --resume
```

### Resume Specific Experiment
```powershell
python sds_yolo11\train.py --config <your_config> --data <your_data> --name <experiment_name> --resume
```

## 🚨 Common Issues

### "No checkpoint found"
- Make sure you're using the same `--name` as your original run
- Check that `runs/train/<name>/weights/last.pt` exists

### "Training starts from epoch 0"
- You didn't use the `--resume` flag
- Or the checkpoint file doesn't exist at the expected location

### "Out of memory after resume"
- Try reducing batch size: `--batch <smaller_number>`
- Clear CUDA cache before resuming

## 💾 Backup Best Practices

Before long training sessions:

1. **Run prevent sleep script:**
   ```powershell
   .\sds_yolo11\prevent_sleep.ps1
   ```

2. **Note your exact command:**
   - Copy your training command to a text file
   - You'll need the same parameters to resume

3. **Check disk space:**
   - Checkpoints can be large (100-500MB each)
   - Ensure you have enough free space

## ⏰ Long Training Sessions

For training that takes hours/days:

- ✅ Keep laptop plugged in
- ✅ Run `prevent_sleep.ps1` first
- ✅ Ensure good ventilation (GPU will be hot)
- ✅ Consider using a cloud GPU if laptop stability is a concern

## 🎯 Manual Checkpoint Loading

If you want to start from a specific checkpoint:

```python
from ultralytics import YOLO

# Load a specific checkpoint
model = YOLO('runs/train/exp/weights/best_epoch_29.pt')

# Continue training
model.train(
    data='seadrones_data.yaml',
    epochs=100,  # Total epochs (it will continue from where checkpoint left off)
    ...
)
```

---

## 📞 Need Help?

If training fails to resume, check:
1. The checkpoint file exists
2. You're using the same `--name` parameter
3. The config and data paths are correct
4. You have the `--resume` flag
