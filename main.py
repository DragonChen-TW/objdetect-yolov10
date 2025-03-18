import torch

def main():
    print("Hello from objdetect-yolov10!")
    a = torch.rand(3, 3)
    print(a)
    device = torch.device('cuda')
    a = a.to(device)
    print(a)


if __name__ == "__main__":
    main()
