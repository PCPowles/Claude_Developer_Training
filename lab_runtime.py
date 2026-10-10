def step_header(*args, **kwargs):
    print("\n" + "=" * 60)
    print(" ".join(str(a) for a in args))
    print("=" * 60)

def exam_note(*args, **kwargs):
    print("[EXAM NOTE]", *args)

def pitfall(*args, **kwargs):
    print("[PITFALL]", *args)

def checkpoint(*args, **kwargs):
    print("[CHECKPOINT]", *args)