import torch
import time
import numpy as np
import matplotlib

matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt

from torch.nn import Module
from models.FM_Base import FM_Base

Tensor_type = torch.DoubleTensor



class SFTRL_CCFM(FM_Base):

    def __init__(self, inputs_matrix, outputs,  task, learning_rate, num_feature):
        super(SFTRL_CCFM, self).__init__(inputs_matrix, outputs, task, learning_rate, num_feature)

        self.model_name = "SFTRL_CCFM"
        self.row_count_p = 0
        self.row_count_n = 0
        self.BT_P = Tensor_type(np.zeros([self.num_feature, 2*self.m]))
        self.BT_N = Tensor_type(np.zeros([self.num_feature, 2*self.m]))


    def online_learning(self,logger):
        start = time.time()
        logger.info("==" * 20)
        logger.info(self.model_name + '_' + str(self.eta) + '_' + str(self.m)  + '_start')

        pred_list = []
        real_list = []

        for idx in range(self.num_data):


            alpha = self.At[:, idx].unsqueeze(1)
            BP_alpha = self.BT_P.t().matmul(alpha)
            BN_alpha = self.BT_N.t().matmul(alpha)
            scalar,pred  = self._predict( (BP_alpha.t().matmul(BP_alpha) - BN_alpha.t().matmul(BN_alpha)).squeeze() )


            if torch.isnan(scalar):
                logger.info('Nan contained')
                raise ValueError('Nan contained')

            if self.task == 'cls':
                #sign_idx = self._grad_loss(scalar * self.b[idx])*(self.b[idx])
                sign_idx = self._grad_loss(scalar * self.b[idx]).mul(self.b[idx])
            elif self.task == 'reg':
                sign_idx = self._grad_loss(scalar - self.b[idx])
            else:
                raise NotImplementedError

            self._GFD(sign_idx, alpha)


            pred_list.append(pred)
            real_list.append(self.b[idx])

            if idx % 1000 == 0:
                logger.info(' %d th : pred %f , real %f ' % (idx, pred, self.b[idx]))
                print(' %d th : pred %f , real %f ' % (idx, pred, self.b[idx] ))


        # return torch.tensor(pred_list).reshape([-1,1]).double(),\
        #        torch.tensor(np.asarray(real_list).reshape[-1,1]).double()
        end = time.time()
        logger.info('learning time : %f ' % (end-start))


        return np.asarray(pred_list),np.asarray(real_list),(end-start)


    def _GFD(self, sign, alpha):
        # alpha : num_feature x 1
        # sign : scalar value

        if sign <= 0:
            self.row_count_p += 1
            self.BT_P[:,self.row_count_p] = np.sqrt(-self.eta*sign)*alpha.squeeze()

            if self.row_count_p == 2*self.m - 1  :
                U, Sigma, _ = (self.BT_P.t().matmul(self.BT_P)).svd()
                Sigma[Sigma.data <= self._thres] = 0.0
                nnz = Sigma.nonzero().numel()
                V = self.BT_P.matmul(U[:, :nnz]).matmul(  (1/Sigma[:nnz].sqrt()).diag()   )

                if nnz >= self.m:
                    self.BT_P = V[:, :self.m - 1].matmul((Sigma[:self.m - 1] - Sigma[self.m]).sqrt().diag())
                    self.BT_P = torch.cat([self.BT_P, torch.zeros([self.num_feature, self.m + 1]).double() ], 1)
                    self.row_count_p = self.m - 1

                else:
                    self.BT_P = V[:, :nnz].matmul((Sigma[:nnz]).sqrt().diag())
                    self.BT_P= torch.cat([self.BT_P, torch.zeros([self.num_feature, (2 * self.m) - nnz]).double() ], 1)
                    self.row_count_p = nnz

        else:
            self.row_count_n += 1
            self.BT_N[:, self.row_count_n] = np.sqrt(self.eta * sign) * alpha.squeeze()

            if self.row_count_n == 2*self.m - 1:
                U, Sigma, _ = (self.BT_N.t().matmul(self.BT_N)).svd()
                Sigma[Sigma.data <= self._thres] = 0.0
                nnz = Sigma.nonzero().numel()
                V = self.BT_N.matmul(U[:, :nnz]).matmul(  (1/Sigma[:nnz].sqrt()).diag()    )

                if nnz >= self.m:
                    self.BT_N = V[:, :self.m - 1].matmul((Sigma[:self.m - 1] - Sigma[self.m]).sqrt().diag())
                    self.BT_N = torch.cat([self.BT_N, torch.zeros([self.num_feature, self.m + 1 ]).double() ], 1)
                    self.row_count_n = self.m - 1

                else:
                    self.BT_N = V[:, :nnz].matmul((Sigma[:nnz]).sqrt().diag())
                    self.BT_N = torch.cat([self.BT_N, torch.zeros([self.num_feature, (2 * self.m) - nnz] ).double()] , 1)
                    self.row_count_n = nnz

        return




if __name__ == "__main__" :

    nbUsers = 943
    nbMovies = 1682
    nbFeatures = nbUsers + nbMovies
    nbRatingsTrain = 90570
    nbRatingsTest = 9430

    data_dir = '../data/ml-100k/'
    #filename1, filename2 = 'ub.base', './ub.test'
    filename1, filename2 = 'ua.base', './ua.test'

    # load dataset
    _, x_train, y_train, rate_train, timestamp_train = load_dataset_movielens(data_dir + filename1,
                                                                              nbRatingsTrain,
                                                                              nbFeatures,
                                                                              nbUsers)
    # sort dataset in time
    #x_train_s, rate_train_s, _ = sort_dataset(x_train, rate_train, timestamp_train)
    x_train_s, rate_train_s, _ = sort_dataset_movielens(x_train, rate_train, timestamp_train)

    want_permute = True
    if want_permute :
        idx = np.random.permutation(x_train_s.shape[0])
        x_train_s = x_train_s[idx]
        rate_train_s = rate_train_s[idx]
    else:
        pass



    #model setup
    m = 5
    lr_FM = 0.005
    task = 'reg'

    logger = logging.getLogger('Result_log')
    logger.setLevel(logging.INFO)
    path_log = './FM_FTRL,txt'
    file_handler = logging.FileHandler(path_log)
    logger.addHandler(file_handler)

    logger.info("==" * 20)
    logger.info("FM_FTRL stat")
    print("==" * 20)

    #task, learning_rate, feature_m
    Model_SFTRL_C = SFTRL_CCFM(Tensor_type(x_train_s.todense()),Tensor_type(rate_train_s) , task,lr_FM,m )
    pred_F, _ , time = Model_SFTRL_C.online_learning(logger)