import torch.nn as nn
from torch.nn.init import xavier_uniform_


class MLP_3hl_d2bn(nn.Module):
    '''
    An MLP Neural Network with three hidden layers, with dropout and
    batch normalisation
    '''

    def __init__(self, dims=[256, 200, 250, 50, 1], drop_rates=[0.5, 0.2]):
        '''
        Initialise the NN, model and parameters

        Parameters
        ----------
        dims: List
            The dimensions for the different layers: Input, Hidden_1, Hidden_2
            and Output

        drop_rate: float
            The rate for the dropout layer
        '''
        super(MLP_3hl_d2bn, self).__init__()

        D_in, D_h1, D_h2, D_h3, D_out = dims
        dropout_r1, dropout_r2 = drop_rates

        self.fc1 = nn.Linear(D_in, D_h1)
        self.fc2 = nn.Linear(D_h1, D_h2)
        self.fc3 = nn.Linear(D_h2, D_h3)
        self.out = nn.Linear(D_h3, D_out)
        self.relu1 = nn.ReLU()
        self.relu2 = nn.ReLU()
        self.relu3 = nn.ReLU()
        self.drop1 = nn.Dropout(p=dropout_r1)
        self.drop2 = nn.Dropout(p=dropout_r2)
        self.batchNorm1 = nn.BatchNorm1d(D_h1)
        self.batchNorm2 = nn.BatchNorm1d(D_h2)

        # initialise linear layers with a 'Glorot initialization'
        xavier_uniform_(self.fc1.weight)
        xavier_uniform_(self.fc2.weight)
        xavier_uniform_(self.fc3.weight)
        xavier_uniform_(self.out.weight)

    def forward(self, X):
        '''
        Execute the forward pass

        Parameters
        ----------
        X: Torch tensor
            The features variables to feed to the Neural Network
        Return
        ------
        out: Torch tensor
            The output value
        '''
        h1 = self.drop1(self.relu1(self.batchNorm1(self.fc1(X))))
        h2 = self.drop2(self.relu2(self.batchNorm2(self.fc2(h1))))
        h3 = self.relu3(self.fc3(h2))
        out = self.out(h3)
        return(out)

    def predict(self, X):
        '''
        Predict !

        Parameters
        ----------
        X: Torch tensor
            The features variables from which to predict
        Return
        ------
        out: numpy array
            The output predictions
        '''
        self.eval()
        yp = self(X).squeeze().detach().numpy().tolist()
        return(yp)
        self.eval()
