#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""In this tutorial, we will train an image classifier with FLSim to simulate a federated learning training environment.

With this tutorial, you will learn the following key components of FLSim:
1. Data loading
2. Model construction
3. Trainer construction

    Typical usage example:
    python3 cifar10_example.py --config-file configs/cifar10_config.json
"""
from datetime import datetime
import argparse
import sys

sys.path.insert(0, '../examples')
from celeba_example import Resnet18
sys.path.insert(0, '../flsim')
import json
from flsim.mysql_database_helper import get_table_size

import flsim.configs  # noqa
import hydra
import torch
from flsim.data.data_sharder import SequentialSharder
from flsim.interfaces.metrics_reporter import Channel
from flsim.utils.config_utils import maybe_parse_json_config
from flsim.utils.example_utils import (
    DataLoader,
    DataProvider,
    FLModel,
    MetricsReporter,
    SimpleConvNet,
)
from hydra.utils import instantiate
from omegaconf import DictConfig, OmegaConf
from torchvision import transforms
from torchvision.datasets.cifar import CIFAR10

IMAGE_SIZE = 32

# builds data provider using local_batch_size and examples_per_user params
def build_data_provider(local_batch_size, examples_per_user, drop_last: bool = False):

    # defines a transform object to be applied to each image
    # resizes image, center crops, converts to pytorch tensor, and normalizes
    transform = transforms.Compose(
        [
            transforms.Resize(IMAGE_SIZE),
            transforms.CenterCrop(IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ]
    )

    # creates dataset object using CIFAR10 class, downloads dataset and transforms each image
    train_dataset = CIFAR10(
        root="../cifar10", train=True, download=True, transform=transform
    )

    # creates dataset object using CIFAR10 class, but sets for test purposes only
    test_dataset = CIFAR10(
        root="../cifar10", train=False, download=True, transform=transform
    )

    # creates sharder and indicates number of examples per user (in fl context)
    sharder = SequentialSharder(examples_per_shard=examples_per_user)

    # creates object responsible for loading data in batches during training/testing
    fl_data_loader = DataLoader(
        train_dataset, test_dataset, test_dataset, sharder, local_batch_size, drop_last
    )
    data_provider = DataProvider(fl_data_loader)
    print(f"Clients in total: {data_provider.num_train_users()}")
    return data_provider

def main(trainer_config, data_config, use_cuda_if_available: bool = True,) -> None:
    cuda_enabled = torch.cuda.is_available() and use_cuda_if_available
    device = torch.device(f"cuda:{0j}" if cuda_enabled else "cpu")
    model = Resnet18(num_classes=10)
    # model = SimpleConvNet(in_channels=3, num_classes=10)


    # Create the parser
    parser = argparse.ArgumentParser()

    # Add an argument for the config file
    parser.add_argument('--config-file', type=str, required=True)

    # Parse the arguments
    args = parser.parse_args()


    with open(args.config_file, 'r') as f:
        data = json.load(f)
    keep_intermediate = data['config']['trainer']['always_keep_trained_model']
    if keep_intermediate:
        store_intermediate_models = True
    else:
        store_intermediate_models = False

    # creates global model for federated learning passing in model and device
    global_model = FLModel(model, device)
    if cuda_enabled:
        global_model.fl_cuda()
    # creates trainer with trainer object (specified by trainer_config), global model and cuda_enabled
    trainer = instantiate(trainer_config, model=global_model, cuda_enabled=cuda_enabled)
    print(f"Created {trainer_config._target_}")
    
    print("Tracking data provenance: " + str(store_intermediate_models))
    # creates data provider with local_batch_size, examples_per_user and drop_last params
    data_provider = build_data_provider(
        local_batch_size=data_config.local_batch_size,
        examples_per_user=data_config.examples_per_user,
        drop_last=False,
    )

    # created metric reporter
    metrics_reporter = MetricsReporter([Channel.TENSORBOARD, Channel.STDOUT])

    # Get the current date and time
    startTime = datetime.now()

    # trains the fl model
    final_model, eval_score = trainer.train(
        data_provider=data_provider,
        metrics_reporter=metrics_reporter,
        num_total_users=data_provider.num_train_users(),
        distributed_world_size=1,
        store_intermediate_models=store_intermediate_models,
    )

    endTime = datetime.now()

    totalTime = (endTime - startTime).total_seconds()

    # if store_intermediate_models:
    #     print("Elapsed Training Time (tracking data lineage): " + str(totalTime) + "s")
    # else:
    #     print("Elapsed Training Time: (without tracking data lineage)" + str(totalTime) + "s")

    # Save the model to the 'trained_models' folder
    # os.makedirs('trained_models', exist_ok=True)

    # Get the current date and time
    # now = datetime.now()
    # timestamp = now.strftime("%m-%d-%Y_%H-%M-%S")

    # saves model to db
    # insert_completed_model('model_databases/flsim_single_node_models.db', 'cifar10_models_completed', final_model.fl_get_module().state_dict(), timestamp)
    # print("saved fully trained global model to db")

    # evaluates the fl model performance on test dataset
    trainer.test(
        data_provider=data_provider,
        metrics_reporter=MetricsReporter([Channel.STDOUT]),
    )

    # if store_intermediate_models:
    #     print("SQLite Database Size: " +str(get_db_size('model_databases/flsim_single_node_models.db')) + " bytes")
    
    global_num_epochs = data['config']['trainer']['epochs']
    client_num_epochs = data['config']['trainer']['client']['epochs']
    users_per_round = data['config']['trainer']['users_per_round']

    print("inserting benchmarks")
    # save stats to benchmarkdb
    if store_intermediate_models:
        # flsim.database_helper.insert_benchmark_stats('benchmark_databases/cifar10_benchmarks.db', 'benchmarks_yes_tracking', global_num_epochs, client_num_epochs, data_provider.num_train_users(), users_per_round, store_intermediate_models, totalTime, flsim.database_helper.get_db_size('model_databases/flsim_single_node_models.db'))
        flsim.mysql_database_helper.insert_benchmark_stats('localhost', 'michgu', 'Dolphin#1', 'benchmarks', 'cifar_yes_tracking', global_num_epochs, client_num_epochs, data_provider.num_train_users(), users_per_round, store_intermediate_models, totalTime, get_table_size('localhost', 'michgu', 'Dolphin#1', 'benchmarks', 'models'))
    else:
        # flsim.database_helper.insert_benchmark_stats('benchmark_databases/cifar10_benchmarks.db', 'benchmarks_no_tracking', global_num_epochs, client_num_epochs, data_provider.num_train_users(), users_per_round, store_intermediate_models, totalTime, 0)
        flsim.mysql_database_helper.insert_benchmark_stats('localhost', 'michgu', 'Dolphin#1', 'benchmarks', 'cifar_no_tracking', global_num_epochs, client_num_epochs, data_provider.num_train_users(), users_per_round, store_intermediate_models, totalTime, 0)
        
# entry point to script when run from console
@hydra.main(config_path=None, config_name="cifar10_tutorial")
def run(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

    trainer_config = cfg.trainer
    data_config = cfg.data

    # call main function
    main(
        trainer_config,
        data_config,
    )


def invoke_main() -> None:
    cfg = maybe_parse_json_config()
    run(cfg)


if __name__ == "__main__":
    invoke_main()  # pragma: no cover
