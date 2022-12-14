import torch
from dataset import FlowDataset
from config import DefaultConfig as Config
from torch.utils.data import DataLoader
from model import LSTM
from train import train
from infer import infer

if __name__ == "__main__":
    torch.use_deterministic_algorithms(True)

    flow_data = FlowDataset('train')
    infer_data = FlowDataset('infer')
    train_data, eval_data, test_data = flow_data.split_data(flow_data, [8, 1, 1])
    train_data_loader = DataLoader(train_data, batch_size=Config.batch_size, shuffle=True, drop_last=True)
    eval_data_loader = DataLoader(eval_data, batch_size=Config.batch_size, shuffle=False, drop_last=True)
    test_data_loader = DataLoader(test_data, batch_size=Config.batch_size, shuffle=False, drop_last=True)
    infer_data_loader = DataLoader(infer_data, batch_size=Config.batch_size, shuffle=False, drop_last=False)
    model = LSTM(
        Config.features_size,
        Config.hidden_size,
        Config.layers_count,
        Config.labels_size,
        Config.batch_size
    )
    train(Config, model, train_data_loader, eval_data_loader)
    infer(Config, model, infer_data_loader, flow_data.mean, flow_data.standard)
