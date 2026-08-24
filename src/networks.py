import numpy

numpy.random.seed(42)

class Linear:
    def __init__(self, in_features: int, out_features: int, activation_function: str = "s"):
        self.weights = numpy.random.uniform(-1, 1, (in_features, out_features))
        self.bias = numpy.zeros((out_features))

    def forward(self, x):

        output = x @ self.weights + self.bias
        return output

    def __call__(self, x):
        self.forward(x)
        
class Base:
    def __init__(self, input_dim, hidden_dim, output_dim, hidden_count: int = 2):
        self.layers = [Linear(input_dim, hidden_dim)] + [Linear(hidden_dim, hidden_dim) for _ in range(hidden_count)] + [Linear(hidden_dim, output_dim)]

    def forward(self, x):

        current_input = x

        for layer in self.layers:

            current_input = layer(current_input)

        logits = current_input
        return logits

    def __call__(self, x):
        self.forward(x)