try:
    with open("training_log_debug.txt", "r", encoding="utf-16") as f:
        for line in f:
            if "predict_latent" in line or "Network" in line or "failed" in line or "type" in line:
                print(line.strip())
except Exception as e:
    print(e)
