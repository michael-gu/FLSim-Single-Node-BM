import sys
from examples.database_helper import get_completed_model
sys.path.insert(0, '../flsim')

from flsim.utils.example_utils import FLModel, SimpleConvNet
import torch
from PIL import Image
from torchvision import transforms

IMAGE_SIZE = 32

if (len(sys.argv) < 3):
    print("Usage: python3 identify_example_image.py model_timestamp <path_to_image>")
    exit(1)

model_timestamp = sys.argv[1]
path_to_image = sys.argv[2]

cuda_enabled = torch.cuda.is_available()
device = torch.device(f"cuda:{0}" if cuda_enabled else "cpu")
model = SimpleConvNet(in_channels=3, num_classes=10)

# creates global model for federated learning passing in model and device
global_model = FLModel(model, device)
if cuda_enabled:
    global_model.fl_cuda()

global_model.fl_get_module().load_state_dict(get_completed_model('model_databases/flsim_single_node_models.db', 'cifar10_models_completed', model_timestamp))

# image load/preprocessing
image = Image.open(path_to_image)

image = Image.open(path_to_image)
if image is None:
    print("Error opening/loading image")
    exit(1)

transform = transforms.Compose(
    [
        transforms.Resize(IMAGE_SIZE),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ]
)

input_tensor = transform(image)
input_batch = input_tensor.unsqueeze(0)

if torch.cuda.is_available():
    input_batch = input_batch.to('cuda')
    model = model.to('cuda')

model.eval()

with torch.no_grad():
    output = model(input_batch)

# The output has unnormalized probabilities. To get probabilities, you can run a softmax on it.
probabilities = torch.nn.functional.softmax(output[0], dim=0)

# You can get the category with the highest probability with:
_, predicted_category = torch.max(output, 1)

# Sort the probabilities in descending order and get the corresponding indices
sorted_probabilities, indices = torch.sort(probabilities, descending=True)

cifar10_class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

# Print the probabilities for each category, ranked from most likely to least likely
for i in range(len(sorted_probabilities)):
    print(f"Category: {cifar10_class_names[indices[i]]}, Probability: {sorted_probabilities[i]}")


 
