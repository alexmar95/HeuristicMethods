import os
import random
import json

dataset_dir = 'data'
def build_random_dataset(N):
    max_value = N * 100
    k = 10
    ret = {}
    ret["N"] = N
    ret["G"] = random.randint(N, k * N)
    ret["g"] = [random.randint(1, round(ret["G"]/3)) for _ in range(N)]
    ret["v"] = [random.randint(1, max_value) for _ in range(N)]
    return ret

def write_dataset(dataset, file_name):
    with open(os.path.join(dataset_dir, file_name), "w") as f:
        f.write(json.dumps(dataset))

def main():
    print("Incepe meciu")
    d8 = build_random_dataset(8)
    write_dataset(d8, 'd8.json')

    d10 = build_random_dataset(10)
    write_dataset(d10, 'd10.json')

    d50 = build_random_dataset(50)
    write_dataset(d50, 'd50.json')

    d100 = build_random_dataset(100)
    write_dataset(d100, 'd100.json')

if __name__ == '__main__':
    main()